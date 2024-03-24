import json
import logging
import math
import os
import pathlib
import subprocess
import threading
from glob import glob
from itertools import islice
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Any, Iterable, Iterator, List, Optional, Tuple
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
from sklearn.model_selection import train_test_split
from tqdm import tqdm

logger = logging.getLogger(__name__)

# Common session for entire run, much efficient
session = boto3.session.Session()
global_client = session.client("s3")


def chunk(it: Iterable, size: int) -> Iterator:
    """
    Chunk a iterator into specific sizes

    Args:
        it (Iterable): The iterable to chunk
        size (int): The size of the chunk

    Returns:
        Iterator: An chunked iterator

    Example:
    >>> a = [1,2,3,4,5]
    >>> i = chunk(a,3)
    >>> next(i)
    (1,2,3)
    >>> next(i)
    (4,5)
    """
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def is_json(myjson: str) -> bool:
    """Checks if the string is a json file.

    Args:
        myjson (str): Filename or path to potential json file.

    Returns:
        bool: Whether myjson was a json file.
    """
    try:
        json.loads(myjson)
    except ValueError:
        return False

    return True


def prefix_exists(url: str, client: Any = None) -> bool:
    """Check whether the prefix exists or not.

    Args:
        url (str): s3 url
        client (Any): The s3 client to use. This allows re-use of an existing client.
            By default, uses the global client.

    Returns:
        bool: Whether the prefix exists or not.
    """
    bucket_name, prefix = _parse_url(url)

    if client is None:
        client = global_client

    objects = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=1)
    return len(objects.get("Contents", ())) == 1


def list_prefixes(bucket_name, prefix, client=None):
    """
    This function is internally used by list_prefix. Use list_prefix instead.
    """
    if client is None:
        client = global_client
    paginator = client.get_paginator("list_objects")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix, Delimiter="/")

    objects = []
    for page in page_iterator:
        for key in page.get("CommonPrefixes", []):
            keyString = key["Prefix"]
            objects.append(keyString)
    return objects


def list_files(bucket_name, prefix, client=None):
    """
    This function is internally used by list_prefix. Use list_prefix instead.
    """
    if client is None:
        client = global_client
    paginator = client.get_paginator("list_objects")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    objects = []
    for page in page_iterator:
        for key in page.get("Contents", []):
            keyString = key["Key"]
            objects.append(keyString)
    return objects


def list_prefix(
    s3_url: str,
    filter_files: Optional[bool] = False,
    filter_prefixes: Optional[bool] = False,
    client: Any = None,
) -> List[str]:
    """List urls to all files and prefixes within the path of the given url.

    Args:
        s3_url (str): The s3 url to list from.
        filter_files (Optional[bool]): If true, output will only contain urls
        to the files within the given url. Defaults to False.
        filter_prefixes (Optional[bool]): If true, output will only contain urls
        to the prefixes within the given url. Defaults to False.
        client (Optional[Any]): Provide a s3 client to use. By default creates a new
            one.

    Raises:
        ValueError: filter_files or filter_prefixes must be provided

    Returns:
        List[str]: The files and/or prefixes within the given url.
    """

    assert not (filter_files and filter_prefixes), "Can't filter files and prefixes"

    bucket_name, prefix = _parse_url(s3_url)
    if filter_files:
        objects = list_files(bucket_name, prefix, client)
    elif filter_prefixes:
        objects = list_prefixes(bucket_name, prefix, client)
    else:
        raise ValueError("Either filter_files or filter_prefixes must be provided")

    files = [
        os.path.join("s3://", bucket_name, obj) for obj in objects if obj != prefix
    ]

    if filter_files:
        files = [f for f in files if f[-1] != "/"]
    elif filter_prefixes:
        files = [f for f in files if f[-1] == "/"]
    return files


def upload_file(
    local_path: str,
    s3_url: str,
    exist_ok: bool = True,
    client=None,
    same_suffix: bool = True,
):
    """Upload file to s3 bucket.

    Args:
        local_path (str): Path to the file to upload.
        s3_url (str): s3 url to upload file to.
        exist_ok (bool, optional): Decides whether or not to ignore existing file.
            Defaults to True.
        client (Any): Provide a s3 client to use. By default, uses the global client.
        same_suffix (bool, optional): Make sure that the suffix of src and dest are same
    """
    bucket_name, prefix = _parse_url(s3_url)
    if client is None:
        client = global_client

    filename = os.path.basename(local_path)

    if not pathlib.Path(prefix).suffix:
        new_prefix = os.path.join(prefix, filename)
    else:
        prefix_p = pathlib.Path(prefix)
        filename_p = pathlib.Path(filename)
        if (prefix_p.suffix == filename_p.suffix) or (not same_suffix):
            new_prefix = prefix
        else:
            logger.warning(
                f"Mismatched file extensions for src: {prefix_p.name} and dst: "
                f"{filename_p.name}, converting prefix to local file format."
            )
            new_prefix = os.path.join(os.path.dirname(prefix), filename)

    if exist_ok:
        try:
            client.head_object(Bucket=bucket_name, Key=new_prefix)
        except ClientError:
            client.upload_file(local_path, bucket_name, new_prefix)
    else:
        client.upload_file(local_path, bucket_name, new_prefix)


def upload_dir(
    local_path: str, s3_url: str, exist_ok: bool = True, recursive: bool = False
):
    """Upload data from a local directory to an S3 bucket.

    Args:
        local_path (str): Local directory to upload from.
        s3_url (str): S3 url to upload files in directory to.
        exist_ok (bool): Decides whether or not to ignore existing files. Default True.
        recursive (bool): Upload recurively. Default False
    """
    nthreads = cpu_count()

    # Allow recursive uploads and handle IsDirectoryError
    files = glob(f"{local_path}/**", recursive=recursive)
    files_filtered = []
    for f in files:
        if os.path.isfile(f):
            files_filtered.append(os.path.relpath(f, local_path))
    files = files_filtered
    num_files = len(files)

    lock = threading.Lock()

    with tqdm(total=num_files) as pbar:
        pbar.set_description(f"Upload {os.path.basename(local_path)}")

        def upload_file_local(filenames):
            # New session for thread safety
            client = global_client
            for filename in filenames:
                file_path = os.path.join(local_path, filename)
                s3_path = os.path.join(s3_url, filename)
                with lock:
                    print(file_path)
                    print(s3_path)
                upload_file(file_path, s3_path, exist_ok=exist_ok, client=client)

                with lock:
                    pbar.update(1)

        # Chunk files into nthreads, a lot faster due to minimal https overhead
        # Multi-Threaded download of dir
        nthreads = min(nthreads, num_files)
        with ThreadPool(processes=nthreads) as pool:
            pool.map(upload_file_local, chunk(files, math.ceil(num_files / nthreads)))


def download_file(
    s3_url: str, local_path: str, size_limit: Optional[int] = None, client=None
):
    """Download file from S3 bucket to local directory.

    Args:
        s3_url (str): S3 url to the file to download.
        local_path (str): Local path to store file.
        size_limit (int, optional): Limits the file size accepted to size_limit bytes.
        Default None.
        client (Any): Provide a s3 client to use. By default, uses the global client.
    """
    bucket_name, prefix = _parse_url(s3_url)
    if client is None:
        client = global_client
    if size_limit is not None:
        response = client.head_object(Bucket=bucket_name, Key=prefix)
        file_size = int(response["ContentLength"])
        if file_size > size_limit:
            raise ValueError(
                "image size {} exceeds size_limit {}".format(file_size, size_limit)
            )

    client.download_file(bucket_name, prefix, local_path)


def download_dir(
    s3_url: str, local_path: Optional[str] = None, size_limit: Optional[int] = None
):
    """Download the contents of a folder directory.

    Args:
        s3_url (str): S3 url to bucket directory to download.
        local_path (str, optional): Local directory to store files in.
        size_limit (int, optional): Limits the file size accepted to size_limit bytes.
        Default None.
    """
    nthreads = cpu_count()
    objects = list_prefix(s3_url, filter_files=True)
    num_objects = len(objects)
    local_path_p = Path(local_path)

    if num_objects > 0:
        local_path_p.mkdir(exist_ok=True, parents=True)

    lock = threading.Lock()

    with tqdm(total=num_objects) as pbar:
        pbar.set_description(f"Download {os.path.basename(s3_url.strip('/'))}")

        def download_file_local(objects):
            # Local s3 client for thread-safety
            client = global_client
            for obj in objects:
                file_path = local_path_p.joinpath(Path(obj).relative_to(s3_url))
                file_path.parent.mkdir(exist_ok=True, parents=True)
                download_file(obj, str(file_path), size_limit=size_limit, client=client)
                with lock:
                    pbar.update(1)

        # Multi-Threaded download of dir
        nthreads = min(nthreads, num_objects)
        with ThreadPool(processes=nthreads) as pool:
            pool.map(
                download_file_local, chunk(objects, math.ceil(num_objects / nthreads))
            )


def sync_dir(from_dir: str, to_dir: str, quiet: Optional[bool] = True) -> None:
    """Sync two directories using `aws s3 sync` command.

    Command Description,
    Syncs directories and S3 prefixes. Recursively copies new and updated files
    from the source directory to the destination. Only creates folders in the
    destination if they contain one or more files.

    Args:
        from_dir (str): S3 url or local url to sync from
        to_dir (str): S3 url or local url to sync to
        quiet (bool): Run the command in quiet mode. Defaults to True

    Raises:
        subprocess.CalledProcessError: Raised when the sync command returns non-zero
            exit code
    """
    logger.debug(f"Sync from url {from_dir} to url {to_dir}")
    command = ["aws", "s3", "sync", from_dir, to_dir]
    if quiet:
        command.append("--quiet")
    subprocess.check_call(command)
    logger.debug("Directory synced successfully")


def split_dataset(
    data_url: str,
    train_split: Optional[float] = 0.8,
    labels_url: Optional[str] = None,
    val_split: Optional[float] = None,
):
    """train_test_split for files hosted in s3

    Args:
        data_url (str): s3 url location of data to be split
        train_split (Optional[float], optional): percentage of the dataset reserved for
            training. Defaults to 0.8.
        labels_url (Optional[str], optional): s3 url location of data labels to be
            split. Defaults to None.
        val_split (Optional[float], optional): percentage of remaining dataset split
            into val and test (e.g., if train_split = 0.6, val_split = 0.5, the splits
            will be 60% train, 20% val, and 20% test). Defaults to None.
    """
    if labels_url is not None:
        _split_labeled_dataset(data_url, labels_url, train_split, val_split)
    else:
        _split_unlabeled_dataset(data_url, train_split, val_split)


def move_file(bucket: str, prefix: str, file: str, client: Any = None):
    """Move file from within s3.

    Args:
        bucket (str): bucket name from within which to move file.
        prefix (str): prefix to move the file to.
        file (str): file being moved.
        client (Any): Provide a s3 client to use. By default, uses the global client.
    """
    # Create a new resource everytime to ensure thread-safety
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html#multithreading-or-multiprocessing-with-resources # noqa: E501
    if client is None:
        client = global_client
    copy_source = {"Bucket": bucket, "Key": file}
    new_prefix = os.path.join(prefix, os.path.basename(file))
    client.copy(copy_source, bucket, new_prefix)


def move_file_2(src: str, dst: str, copy: bool = True, client: Any = None):
    """Move file from within s3. Destination is a file instead of directory.

    It optionally provides the capacity to copy file as well

    Args:
        src (str): source s3 location
        dst (str): destination s3 location
        copy (bool) : Copy files instead of move operation. Defaults to a copy
            operation.
        client (Any): Provide a s3 client to use. By default, uses the global client.
    """
    # Use a custom session everytime to ensure thread-safety
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html#multithreading-or-multiprocessing-with-resources # noqa: E501
    if client is None:
        client = global_client
    src_bucket, src_key = _parse_url(src)
    copy_source = {"Bucket": src_bucket, "Key": src_key}
    dst_bucket, dst_key = _parse_url(dst)
    # Copy source to destination
    client.copy(copy_source, dst_bucket, dst_key)
    if not copy:
        # Delete the source
        client.delete_object(Bucket=src_bucket, Key=src_key)


def move_files(bucket: str, prefix: str, files: List[str]):
    """Move files from within s3.

    Args:
        bucket (str): bucket name from within which to move files.
        prefix (str): prefix to move the files to.
        files (List[str]): list of files being moved.
    """
    nthreads = cpu_count()
    num_files = len(files)

    def _move_files(files_to_move):
        client = global_client
        for f in files_to_move:
            move_file(bucket, prefix, f, client=client)

    # Multi-threaded move for faster operations
    nthreads = min(nthreads, num_files)
    with ThreadPool(processes=nthreads) as pool:
        pool.map(_move_files, chunk(files, math.ceil(num_files / nthreads)))


def _parse_url(url: str) -> Tuple[str, str]:
    url_parsed = urlparse(url, allow_fragments=False)
    bucket = url_parsed.netloc
    prefix = url_parsed.path.lstrip("/")
    return bucket, prefix


def _make_split_prefix(prefix: str, split: str) -> str:
    if prefix[-1] == "/":
        prefix = prefix[:-1]
    child_prefix = os.path.basename(prefix)
    parent_prefix = os.path.dirname(prefix)
    split_prefix = os.path.join(parent_prefix, split, child_prefix)
    return split_prefix


def delete_missing_pairs(input_data, pair_data):
    """Delete items from input data that does not have a corresponding item in pair
    data.

    This assumes that the filenames without extensions to be the same in both input
    lists.

    Args:
        input_data (list): list of file paths to check
        pair_data (list): list of file paths to find a match

    Returns:
        list: list of files with missing pairs deleted
    """
    to_del = []
    for idx, pth in enumerate(input_data):
        name = pathlib.Path(pth).stem
        combined = "\t".join(pair_data)
        if name not in combined:
            to_del.append(idx)
    for index in sorted(to_del, reverse=True):
        del input_data[index]
    return input_data


def _split_labeled_dataset(
    data_url: str,
    labels_url: str,
    train_split: int = 0.8,
    val_split: Optional[float] = None,
    delete_missing_pairs: Optional[
        bool
    ] = False,  # Assumes filenames without extension to be the same
):
    data_bucket_name, data_prefix = _parse_url(data_url)
    labels_bucket_name, labels_prefix = _parse_url(labels_url)

    s3 = session.resource("s3")
    data_bucket = s3.Bucket(data_bucket_name)
    labels_bucket = s3.Bucket(labels_bucket_name)
    data = [
        x.key
        for x in data_bucket.objects.filter(Prefix=data_prefix)
        if x.key[-1] != "/"
    ]
    labels = [
        x.key
        for x in labels_bucket.objects.filter(Prefix=labels_prefix)
        if x.key[-1] != "/"
    ]

    if delete_missing_pairs:
        # Delete images without labels
        data = delete_missing_pairs(data, labels)

        # Delete labels without images
        labels = delete_missing_pairs(labels, data)

    x_train, x_val, y_train, y_val = train_test_split(
        data, labels, train_size=train_split
    )
    split_prefix = _make_split_prefix(data_prefix, "train")
    move_files(data_bucket_name, split_prefix, x_train)
    split_prefix = _make_split_prefix(labels_prefix, "train")
    move_files(labels_bucket_name, split_prefix, y_train)

    if val_split is not None:
        x_val, x_test, y_val, y_test = train_test_split(
            x_val, y_val, train_size=val_split
        )
        split_prefix = _make_split_prefix(data_prefix, "val")
        move_files(data_bucket_name, split_prefix, x_val)
        split_prefix = _make_split_prefix(labels_prefix, "val")
        move_files(labels_bucket_name, split_prefix, y_val)

        split_prefix = _make_split_prefix(data_prefix, "test")
        move_files(data_bucket_name, split_prefix, x_test)
        split_prefix = _make_split_prefix(labels_prefix, "test")
        move_files(labels_bucket_name, split_prefix, y_test)
    else:
        split_prefix = _make_split_prefix(data_prefix, "val")
        move_files(data_bucket_name, split_prefix, x_val)
        split_prefix = _make_split_prefix(labels_prefix, "val")
        move_files(labels_bucket_name, split_prefix, y_val)


def _split_unlabeled_dataset(
    data_url: str, train_split: int = 0.8, val_split: Optional[float] = None
):
    data_bucket_name, data_prefix = _parse_url(data_url)

    s3 = session.resource("s3")
    data_bucket = s3.Bucket(data_bucket_name)
    data = [
        x.key
        for x in data_bucket.objects.filter(Prefix=data_prefix)
        if x.key[-1] != "/"
    ]

    x_train, x_val = train_test_split(data, train_size=train_split)
    split_prefix = _make_split_prefix(data_prefix, "train")
    move_files(data_bucket_name, split_prefix, x_train)

    if val_split is not None:
        x_val, x_test = train_test_split(x_val, train_size=val_split)
        split_prefix = _make_split_prefix(data_prefix, "val")
        move_files(data_bucket_name, split_prefix, x_val)

        split_prefix = _make_split_prefix(data_prefix, "test")
        move_files(data_bucket_name, split_prefix, x_test)
    else:
        split_prefix = _make_split_prefix(data_prefix, "val")
        move_files(data_bucket_name, split_prefix, x_val)
