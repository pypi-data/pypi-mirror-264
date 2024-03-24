import argparse
import os
import tempfile
from pathlib import Path
from xml.dom import minidom

from PIL import Image

from ml_dronebase_data_utils.bbox.visualize import draw_rotated_boxes
from ml_dronebase_data_utils.s3 import download_file, list_prefix, upload_file


def visualize(**kwargs):
    """Visualize converted xml annotations

    Args:
        ortho_path (???): The path to the ortho
        anno_path (???): The path to the annotation
        save_path (???): The save path
        draw_labels (???): Draw the labels or not, defaults to False
    """
    ortho_path = kwargs.get("ortho_path", None)
    anno_path = kwargs.get("anno_path", None)
    save_path = kwargs.get("save_path", None)
    draw_labels = kwargs.get("draw_labels", False)

    if ortho_path is None or anno_path is None or save_path is None:
        print("You must specify ortho_path, anno_path and save_path")
        return 1

    batch = kwargs.get("batch", False)

    orthos = []
    anno_paths = []
    save_paths = []
    if batch:
        if "s3://" in ortho_path:
            for prefix in list_prefix(ortho_path, filter_files=True):
                orthos.append(prefix)
        else:
            for path in Path(ortho_path).iterdir():
                if path.is_file():
                    orthos.append(str(path))
        if "s3://" in anno_path:
            for prefix in list_prefix(anno_path, filter_files=True):
                anno_paths.append(prefix)
        else:
            for path in Path(anno_path).iterdir():
                if path.is_file():
                    anno_paths.append(str(path))
        if len(orthos) != len(anno_paths):
            print("All orthos don't have geojsons")
            return 2
        for g in anno_paths:
            save_paths.append(
                str(Path(save_path).joinpath(f"{Path(g).stem}_annotated.png")).replace(
                    "s3:/", "s3://"
                )
            )
    else:
        orthos.append(ortho_path)
        anno_paths.append(anno_path)
        save_paths.append(save_path)

    total_count = len(orthos)
    for idx, (op, ap, sp) in enumerate(zip(orthos, anno_paths, save_paths)):
        print(f"Processing file {idx+1}/{total_count}, {op}", end="\r")
        # Create a temporary directory which is cleaned up after use
        with tempfile.TemporaryDirectory() as tmpdir:
            if "s3://" in op:
                # Download
                path = os.path.join(tmpdir, os.path.basename(op))
                download_file(op, path)
                op = path

            if "s3://" in anno_path:
                # Download
                path = os.path.join(tmpdir, os.path.basename(ap))
                download_file(ap, path)
                ap = path

            # Ideally find size height and width and use that limit for reading in PIL,
            # see https://github.com/python-pillow/Pillow/issues/515
            # But currently skip if we encounter error
            try:
                img = Image.open(op)
            except Image.DecompressionBombError:
                print(f"Skipping {op} as it exceeds {Image.MAX_IMAGE_PIXELS} pixels")
                continue

            parser = minidom.parse(ap)

            annotations = parser.getElementsByTagName("object")

            boxes = []
            classes = []

            for a in annotations:
                xmin = float(a.getElementsByTagName("xmin")[0].firstChild.data)
                xmax = float(a.getElementsByTagName("xmax")[0].firstChild.data)
                ymin = float(a.getElementsByTagName("ymin")[0].firstChild.data)
                ymax = float(a.getElementsByTagName("ymax")[0].firstChild.data)
                try:
                    angle = float(a.getElementsByTagName("angle")[0].firstChild.data)
                except ValueError:
                    angle = 0.0
                boxes.append([xmin, ymin, xmax, ymax, angle])
                if draw_labels:
                    class_name = a.getElementsByTagName("name")[0].firstChild.data
                    classes.append(class_name)

            if len(boxes):
                # img_drawn = draw_ (img,boxes,classes)
                img_drawn = draw_rotated_boxes(
                    img, boxes, classes=classes, box_mode="XYXYA_ABS"
                )
            else:
                img_drawn = img

            upload = False
            if "s3://" in sp:
                orig_save_path = sp
                sp = os.path.join(tmpdir, os.path.basename(sp))
                upload = True

            img_drawn.save(sp)

            if upload:
                upload_file(sp, orig_save_path, exist_ok=False)
    return None


def visualize_converted_geojson():
    parser = argparse.ArgumentParser(
        description="Visualize converted geojson for quick visual inspection"
    )

    parser.add_argument(
        "--ortho-path", "-o", required=True, help="The ortho path, can be local/s3"
    )
    parser.add_argument(
        "--anno-path", "-a", required=True, help="The ortho path, can be local/s3"
    )
    parser.add_argument(
        "--save-path", "-s", required=True, help="The ortho path, can be local/s3"
    )
    parser.add_argument(
        "--draw-labels",
        "-d",
        action="store_true",
        default=False,
        help="Draw the class labels",
    )
    parser.add_argument(
        "--batch", "-b", action="store_true", default=False, help="Run in batched mode"
    )

    args = vars(parser.parse_args())

    visualize(**args)


if __name__ == "__main__":
    visualize_converted_geojson()
