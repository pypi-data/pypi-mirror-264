from typing import Any, List

import numpy as np
import rasterio
from shapely.geometry import Polygon


def georeference_boxes(image_path: str, boxes: np.ndarray) -> List[Any]:
    """Georeference panels to ortho, (x, y) in pixels -> (x, y) in meters (EPSG: 3857)
    Args:
        image_path (str): path/url to georeferenced image
        boxes (np.ndarray): Nx4x2 array of bounding box vertices in image coordinates
    Returns:
        N georeferenced polygons in geo coordinates
    """
    if boxes is None:
        return []

    with rasterio.open(image_path) as image:
        geoms = []
        for box in boxes:
            polygon = Polygon(
                [
                    image.xy(box[0][1], box[0][0]),
                    image.xy(box[1][1], box[1][0]),
                    image.xy(box[2][1], box[2][0]),
                    image.xy(box[3][1], box[3][0]),
                    image.xy(box[0][1], box[0][0]),
                ]
            )
            geoms.append(polygon)

    return geoms
