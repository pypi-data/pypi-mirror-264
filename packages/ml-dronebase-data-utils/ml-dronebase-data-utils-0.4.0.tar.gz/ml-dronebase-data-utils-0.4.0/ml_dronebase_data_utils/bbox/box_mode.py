"""Modified from:
https://github.com/facebookresearch/detectron2/blob/main/detectron2/structures/boxes.py
"""

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Union

import numpy as np
import torch

_RawBoxType = Union[List[float], Tuple[float, ...], torch.Tensor, np.ndarray]


@unique
class BoxMode(IntEnum):
    """
    Enum of different ways to represent a box.
    """

    XYXY_ABS = 0
    """
    (x0, y0, x1, y1) in absolute floating points coordinates.
    The coordinates in range [0, width or height].
    """
    XYWH_ABS = 1
    """
    (x0, y0, w, h) in absolute floating points coordinates.
    """
    XYXY_REL = 2
    """
    Not yet supported!
    (x0, y0, x1, y1) in range [0, 1]. They are relative to the size of the image.
    """
    XYWH_REL = 3
    """
    Not yet supported!
    (x0, y0, w, h) in range [0, 1]. They are relative to the size of the image.
    """
    XYXYA_ABS = 4
    """
    (x0, y0, x1, y1, a) in absolute floating points coordinates.
    (x0, y0, x1, y1) are in range [0, width or height] of the non-rotated box.
    (a) is the angle in degrees ccw to obtain the rotated box.
    """
    XYWHA_ABS = 5
    """
    (xc, yc, w, h, a) in absolute floating points coordinates.
    (xc, yc) is the center of the rotated box, and the angle a is in degrees ccw.
    """

    @staticmethod
    def convert(
        box: _RawBoxType,
        from_mode: "BoxMode",
        to_mode: "BoxMode",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> _RawBoxType:
        """
        Args:
            box: can be a k-tuple, k-list or an Nxk array/tensor, where k = 4 or 5
            from_mode, to_mode (BoxMode)
            width: image width, only required when converting to/from relative modes
            height: image height, only required when converting to/from relative modes
        Returns:
            The converted box of the same type.
        """
        if from_mode == to_mode:
            return box

        original_type = type(box)
        is_numpy = isinstance(box, np.ndarray)
        single_box = isinstance(box, (list, tuple))
        if single_box:
            assert len(box) == 4 or len(box) == 5, (
                "BoxMode.convert takes either a k-tuple/list or an Nxk array/tensor,"
                " where k == 4 or 5"
            )
            arr = torch.tensor(box)[None, :]
        else:
            # avoid modifying the input box
            if is_numpy:
                arr = torch.from_numpy(np.asarray(box)).clone()
            else:
                arr = box.clone()

        # if xyxy to xywh
        xyxy_modes = [BoxMode.XYXY_ABS, BoxMode.XYXY_REL, BoxMode.XYXYA_ABS]
        xywh_modes = [BoxMode.XYWH_ABS, BoxMode.XYWH_REL, BoxMode.XYWHA_ABS]
        if from_mode in xyxy_modes and to_mode in xywh_modes:
            arr = BoxMode._convert_xyxy_to_xywh(arr, from_mode, to_mode, width, height)
        elif from_mode in xywh_modes and to_mode in xyxy_modes:
            arr = BoxMode._convert_xywh_to_xyxy(arr, from_mode, to_mode, width, height)
        else:
            # edge cases
            if (from_mode == BoxMode.XYXY_ABS and to_mode == BoxMode.XYXY_REL) or (
                from_mode == BoxMode.XYWH_ABS and to_mode == BoxMode.XYWH_REL
            ):
                arr = BoxMode._convert_abs_to_rel(arr, width, height)
            elif (from_mode == BoxMode.XYXY_REL and to_mode == BoxMode.XYXY_ABS) or (
                from_mode == BoxMode.XYWH_REL and to_mode == BoxMode.XYWH_ABS
            ):
                arr = BoxMode._convert_rel_to_abs(arr, width, height)
            else:
                raise NotImplementedError(
                    "Conversion from BoxMode {} to {} is not supported yet".format(
                        from_mode, to_mode
                    )
                )

        if single_box:
            return original_type(arr.flatten().tolist())
        if is_numpy:
            return arr.numpy()
        else:
            return arr

    @staticmethod
    def _convert_xyxy_to_xywh(
        box: torch.Tensor,
        from_mode: "BoxMode",
        to_mode: "BoxMode",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> torch.Tensor:
        # 1. xyxy_abs to xywh_abs
        # 2. xyxya_abs to xywha_abs
        # 3. xyxy_abs to xywh_rel
        # 4. xyxy_rel to xywh_rel
        # 5. xyxy_rel to xywh_abs
        original_dtype = box.dtype
        box = box.double()

        # only operate on absolute coordinates
        if from_mode == BoxMode.XYXY_REL:
            box = BoxMode._convert_rel_to_abs(box, width, height)

        x = (box[:, 0] + box[:, 2]) / 2.0
        y = (box[:, 1] + box[:, 3]) / 2.0
        w = box[:, 2] - box[:, 0]
        h = box[:, 3] - box[:, 1]

        box[:, 0] = x
        box[:, 1] = y
        box[:, 2] = w
        box[:, 3] = h

        if to_mode == BoxMode.XYWH_REL:
            box = BoxMode._convert_abs_to_rel(box, width, height)

        return box.to(dtype=original_dtype)

    @staticmethod
    def _convert_xywh_to_xyxy(
        box: torch.Tensor,
        from_mode: "BoxMode",
        to_mode: "BoxMode",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> torch.Tensor:
        # 1. xywh_abs to xyxy_abs
        # 2. xywha_abs to xyxya_abs
        # 3. xywh_abs to xyxy_rel
        # 4. xywh_rel to xyxy_rel
        # 5. xywh_rel to xyxy_abs
        original_dtype = box.dtype
        box = box.double()

        # only operate on absolute coordinates
        if from_mode == BoxMode.XYWH_REL:
            box = BoxMode._convert_rel_to_abs(box, width, height)

        w = box[:, 2]
        h = box[:, 3]

        # convert center to top-left corner
        box[:, 0] -= w / 2.0
        box[:, 1] -= h / 2.0
        # bottom-right corner
        box[:, 2] = box[:, 0] + w
        box[:, 3] = box[:, 1] + h

        if to_mode == BoxMode.XYXY_REL:
            box = BoxMode._convert_abs_to_rel(box, width, height)

        return box.to(dtype=original_dtype)

    @staticmethod
    def _convert_abs_to_rel(box: torch.Tensor, width: int, height: int) -> torch.Tensor:
        assert (
            isinstance(width, int) and width > 0
        ), "Image width must be an integer greater than zero"
        assert (
            isinstance(height, int) and width > 0
        ), "Image height must be an integer greater than zero"

        box[:, [0, 2]] /= width
        box[:, [1, 3]] /= height
        return box

    @staticmethod
    def _convert_rel_to_abs(box: torch.Tensor, width: int, height: int) -> torch.Tensor:
        assert (
            isinstance(width, int) and width > 0
        ), "Image width must be an integer greater than zero"
        assert (
            isinstance(height, int) and width > 0
        ), "Image height must be an integer greater than zero"

        box[:, [0, 2]] *= width
        box[:, [1, 3]] *= height
        return box
