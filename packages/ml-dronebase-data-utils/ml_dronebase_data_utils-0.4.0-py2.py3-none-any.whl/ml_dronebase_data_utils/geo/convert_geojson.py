import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

import geopandas as gpd
import numpy as np
import rasterio
from geopandas import GeoDataFrame
from rasterio.io import DatasetReader
from tqdm import tqdm

from ml_dronebase_data_utils.bbox.box_utils import (
    vertices_to_boxes,
    vertices_to_rotated_boxes,
)
from ml_dronebase_data_utils.s3 import upload_file
from ml_dronebase_data_utils.voc.pascal_voc import PascalVOCWriter

module_log = logging.getLogger(__name__)


def geo_to_voc(
    ortho_path: str,
    geo_path: str,
    save_path: str,
    class_attribute: Optional[List[str]] = None,
    class_mapping: Optional[Dict[int, str]] = None,
    default_class: str = "panel",
    skip_classes: List[int] = None,
    rotated: bool = False,
    prefix: str = "",
):
    """Convert data on geojson format to pascal voc data.

    Args:
        ortho_path: Path to the ortho. Can be a local/s3 location
        geo_path: Path to the geojson. Can be a local/s3 location
        save_path: Path where the xml file would be saved. Can be a local/s3 location.
        class_attribute: The geojson attribute to be used as the class, e.g. id
            represents the defect id for current panel
        class_mapping: The class mapping to use. This would map the value of
            class_attribute to some class
        default_class: The default class to use. Useful when only a single class is
            being used. Defaults to panel for backwards compatibility.
        skip_classes: The classes to be skipped while the conversion. This should be
            values from the class_attribute field in the geojson.
        rotated: Specify if to use rotated bounding boxes, defaults to false.
        prefix: Specify a prefix to use for path while writing the xml file. Useful for
            local conversion for final path is s3.
    """
    ortho = rasterio.open(ortho_path)
    gdf = gpd.read_file(geo_path)

    writer = PascalVOCWriter(ortho_path, ortho.width, ortho.height, prefix=prefix)

    boxes = []
    names = []
    if not gdf.empty:
        vertices = get_pixel_vertices(ortho, gdf)
        if rotated:
            boxes = vertices_to_rotated_boxes(vertices)
        else:
            boxes = vertices_to_boxes(vertices)

        if class_attribute is not None:
            for attr in class_attribute:
                names = gdf.get(attr, [])
                if len(names) > 0:
                    break
            if not len(names):
                raise ValueError(
                    "Class attribute key(s) not present in geojson files, attribute"
                    f" keys are {class_attribute} gdf keys are {gdf.columns}"
                )
        else:
            names = [default_class] * len(boxes)
    for box, name in zip(boxes, names):
        # Skip boxes with None or empty/no information, assumption is that they don't
        # have any information
        if name is None or (isinstance(name, str) and len(name) == 0):
            continue
        # Dumb Logic
        try:
            # int(name) might be too restrictive in some scenarios, adapt if required
            name = int(name)
        except ValueError:
            pass
        if skip_classes is not None and name in skip_classes:
            continue
        if class_mapping is not None:
            # If mapping is found, use the default name instead of default.
            name = class_mapping.get(name, name)
        if rotated:
            xmin, ymin, xmax, ymax, angle = box
            writer.addObject(name, xmin, ymin, xmax, ymax, angle)
        else:
            xmin, ymin, xmax, ymax = box
            writer.addObject(name, xmin, ymin, xmax, ymax)

    if "s3://" in save_path:
        anno_path = os.path.basename(save_path)
        anno_path = str(Path(anno_path).with_suffix(".xml"))
        writer.save(anno_path)
        upload_file(anno_path, save_path, exist_ok=False)
        os.remove(anno_path)
    else:
        writer.save(save_path)


def geo_to_rotated_voc(
    ortho_path: str,
    geo_path: str,
    save_path: str,
    class_attribute: Optional[str] = None,
    class_mapping: Optional[Dict[int, str]] = None,
    default_class: str = "panel",
    skip_classes: List[int] = None,
    prefix: str = "",
):
    # Migrated rotated logic to geo_to_voc and only keeping it for compatibility
    geo_to_voc(
        ortho_path,
        geo_path,
        save_path,
        class_attribute,
        class_mapping,
        default_class,
        skip_classes,
        rotated=True,
        prefix=prefix,
    )


def get_pixel_vertices(ortho: DatasetReader, gdf: GeoDataFrame) -> np.ndarray:
    """Convert the set of geographical vertices to image vertices.

    Args:
        ortho (DatasetReader): The orthomosaic file used to index geographical
            coordinates to image coordinates.
        gdf (GeoDataFrame): The dataframe containing the set of geographical vertices.
            The `geometry` field is assumed to contain Multipolygons.

    Returns:
        np.ndarray: A matrix of vertices in image coordinates with shape Nx4x2.
    """
    gdf = gdf.to_crs(ortho.crs)
    polys = gdf.geometry.explode(index_parts=True).tolist()
    geo_vertices = [p.exterior.coords for p in polys]

    pxl_vertices = []
    for geo_v in tqdm(
        geo_vertices, total=len(geo_vertices), desc="Extracting Pixel Vertices"
    ):
        geo_v_ = [[c[0], c[1]] for c in geo_v]
        geo_v_ = np.asarray(geo_v_)
        geo_v_[:, [1, 0]] = geo_v_[:, [0, 1]]
        module_log.info(f"get_pixel_vertices:: geo vertices = {geo_v_}")
        pxl_v = [ortho.index(c[0], c[1]) for c in geo_v]
        pxl_v = np.asarray(pxl_v)
        # swap axes (y, x) -> (x, y)
        pxl_v[:, [1, 0]] = pxl_v[:, [0, 1]]
        module_log.info(f"get_pixel_vertices:: pixel vertices = {pxl_v}")
        pxl_vertices.append(pxl_v[:4])

    return np.asarray(pxl_vertices)
