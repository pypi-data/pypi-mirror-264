from pathlib import Path

from ml_dronebase_data_utils.geo.convert_geojson import geo_to_voc
from ml_dronebase_data_utils.s3 import list_prefix


def run_geojson_conversion(**kwargs):
    """Convert geojson format to pascal voc format

    Args:
        ortho_path (???): The ortho path, can be local/s3
        geojson (???): The geojson path
        save_path (???): The save path
        class_attribute (???): The class attribute to use from the geojson for class
            labels. Must be a list.
        class_mapping (???): A plain txt file containing class mappings
        skip_classes (???): Classes to skip, specify multiple
        rotated (???): Use rotated bounding box, defaults to false

    """
    ortho_path = kwargs.get("ortho_path", None)
    geojson = kwargs.get("geojson", None)
    save_path = kwargs.get("save_path", None)

    if ortho_path is None or geojson is None or save_path is None:
        print("You must specify ortho_path, anno_path and save_path")
        return 1

    batch = kwargs.get("batch", False)

    orthos = []
    geojsons = []
    save_paths = []
    if batch:
        if "s3://" in ortho_path:
            for prefix in list_prefix(ortho_path, filter_files=True):
                orthos.append(prefix)
        else:
            for path in Path(ortho_path).iterdir():
                if path.is_file():
                    orthos.append(str(path))
        if "s3://" in geojson:
            for prefix in list_prefix(geojson, filter_files=True):
                geojsons.append(prefix)
        else:
            for path in Path(geojson).iterdir():
                if path.is_file():
                    geojsons.append(str(path))
        if len(orthos) != len(geojsons):
            print("All orthos don't have geojsons")
            return 2
        for g in geojsons:
            save_paths.append(
                str(Path(save_path).joinpath(f"{Path(g).stem}.xml")).replace(
                    "s3:/", "s3://"
                )
            )
    else:
        orthos.append(ortho_path)
        geojsons.append(geojson)
        save_paths.append(save_path)

    class_attribute = kwargs.get("class_attribute", None)
    class_mapping = kwargs.get("class_mapping", None)
    default_class = kwargs.get("default_class", "panel")
    skip_classes = kwargs.get("skip_classes", [])
    rotated = kwargs.get("rotated", False)
    prefix = kwargs.get("prefix", "")

    total_count = len(orthos)
    for idx, (op, gjson, sp) in enumerate(zip(orthos, geojsons, save_paths)):
        print(f"Processing file {idx+1}/{total_count}, {op}", end="\r")
        # Call the function
        geo_to_voc(
            op,
            gjson,
            sp,
            class_attribute,
            class_mapping,
            default_class,
            skip_classes,
            rotated,
            prefix,
        )
    return None


def convert_geojson_cli():
    import argparse

    parser = argparse.ArgumentParser(description="Convert geojson to voc format data")

    parser.add_argument(
        "--ortho-path", required=True, help="The ortho path, can be local/s3"
    )
    parser.add_argument("--geojson", required=True, help="The geojson path")
    parser.add_argument("--save-path", required=True, help="The save path")
    parser.add_argument(
        "--class-attribute",
        nargs="+",
        help="The class attribute to use from the geojson for class labels",
    )
    parser.add_argument(
        "--class-mapping", help="A plain txt file containing class mappings"
    )
    parser.add_argument(
        "--skip-classes", type=int, nargs="+", help="Classes to skip, specify multiple"
    )
    parser.add_argument(
        "--rotated",
        action="store_true",
        default=False,
        help="Use rotated bounding box, defaults to false",
    )
    parser.add_argument(
        "--batch", action="store_true", default=False, help="Process a batch of orthos"
    )
    parser.add_argument(
        "--prefix", default="", help="The prefix to use when saving the annotation"
    )

    args = vars(parser.parse_args())

    # Read class mapping if provided
    class_mapping = args.get("class_mapping", None)
    if class_mapping is not None:
        mapping = {}
        with open(class_mapping) as cm:
            for line in cm:
                line = line.strip("\n")
                if len(line) < 1:
                    continue
                key, value = line.split("=", maxsplit=1)
                # Currently only supports int, tweak this if required
                key = int(key.strip())
                value = value.strip()
                mapping[key] = value
        args["class_mapping"] = mapping

    run_geojson_conversion(**args)


if __name__ == "__main__":
    convert_geojson_cli()
