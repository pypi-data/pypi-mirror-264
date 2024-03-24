"""Modified from https://github.com/AndrewCarterUK/pascal-voc-writer
"""

import os

from jinja2 import Environment, PackageLoader


class PascalVOCWriter:
    def __init__(
        self,
        path: str,
        width: int,
        height: int,
        depth: int = 3,
        database: str = "Unknown",
        segmented: int = 0,
        prefix: str = "",
    ) -> None:
        environment = Environment(
            loader=PackageLoader(
                package_name="ml_dronebase_data_utils", package_path="voc/templates"
            ),
            keep_trailing_newline=True,
        )
        self.annotation_template = environment.get_template("annotation.xml")
        abspath = os.path.abspath(path)
        if "s3" in path:
            file_path = path
        else:
            file_path = abspath
        if len(prefix) > 0:
            file_path = os.path.join(prefix, os.path.basename(file_path))
        self.template_parameters = {
            "path": file_path,
            "filename": os.path.basename(abspath),
            "folder": os.path.basename(os.path.dirname(abspath)),
            "width": width,
            "height": height,
            "depth": depth,
            "database": database,
            "segmented": segmented,
            "objects": [],
        }

    def addObject(
        self,
        name: str,
        xmin: int,
        ymin: int,
        xmax: int,
        ymax: int,
        angle: str = "Unspecified",
        pose: str = "Unspecified",
        truncated: int = 0,
        difficult: int = 0,
    ) -> None:
        self.template_parameters["objects"].append(
            {
                "name": name,
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax,
                "angle": angle,
                "pose": pose,
                "truncated": truncated,
                "difficult": difficult,
            }
        )

    def save(self, annotation_path: str) -> None:
        with open(annotation_path, "w") as file:
            content = self.annotation_template.render(**self.template_parameters)
            file.write(content)
