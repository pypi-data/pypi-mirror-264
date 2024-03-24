import os
from pathlib import Path
from typing import Any, Dict, Optional
from xml.etree import ElementTree as ET

from ml_dronebase_data_utils.bbox.box_mode import BoxMode


def parse_voc_xml(
    path: str, box_mode: Optional[BoxMode] = BoxMode.XYXY_ABS
) -> Dict[str, Any]:
    """Generalized VOC XML Parser.

    Args:
        path (str, optional): Local path to the xml file. Defaults to None.
        box_mode (Optional[BoxMode], optional): Detectron2 box mode. Defaults to
            BoxMode.XYXY_ABS.

    Returns:
        Dict[str, Any]: Dictionary containing metadata for the image and image
            annotations.
    """
    tree = ET.parse(path).getroot()
    if tree.find("path") is not None:
        image_path = tree.find("path").text
    else:
        split = Path(path).parents[1]
        image_file = tree.find("filename").text
        image_path = os.path.join(split.stem, "images", image_file)

    sample = {
        "file_path": image_path,
        "height": int(tree.findall("./size/height")[0].text),
        "width": int(tree.findall("./size/width")[0].text),
    }

    annotations = []
    for obj in tree.findall("object"):
        label = obj.find("name").text

        bbox = obj.find("bndbox")
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)

        if bbox.find("angle") is not None and bbox.find("angle").text != "Unspecified":
            angle = float(bbox.find("angle").text)

            box = [xmin, ymin, xmax, ymax, angle]
            box = BoxMode.convert(box, from_mode=BoxMode.XYXYA_ABS, to_mode=box_mode)
        else:
            box = [xmin, ymin, xmax, ymax]
            box = BoxMode.convert(box, from_mode=BoxMode.XYXY_ABS, to_mode=box_mode)

        annotation = {"box": box, "label": label}
        annotations.append(annotation)

    sample["annotations"] = annotations
    return sample
