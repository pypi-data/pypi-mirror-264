from copy import deepcopy
from typing import Optional

import torch
from PIL import Image
from torch import FloatTensor

from cvd.datasets.augumentation.utils import intersection_line, four_point2centerxy, centerxy2four_point


def fix_outside_side(bboxes4point, bboxes, out_index, side: str, rectangle_points_coordinate, mode: str):
    """
    Args:
        bboxes4point:
        bboxes:
        out_index:
        side:
        rectangle_points_coordinate:
        mode:

    Returns:

    """
    if side == 'bottom':
        side_line = rectangle_points_coordinate[2:4, :]
    elif side == 'top':
        side_line = rectangle_points_coordinate[0:2, :]
    elif side == 'left':
        side_line = rectangle_points_coordinate[[0,3], :]
    elif side == 'right':
        side_line = rectangle_points_coordinate[1:3, :]
    else:
        raise Exception("Incorrect side")

    _out_points_boxes = bboxes4point[out_index]
    _out_bboxes = bboxes[out_index]
    line_tile: FloatTensor = torch.stack(_out_points_boxes.shape[0] * [side_line])
    line1_point: FloatTensor = torch.stack([_out_points_boxes[:, 1, :], _out_points_boxes[:, 2, :]], dim=1)
    line2_point: FloatTensor = torch.stack([_out_points_boxes[:, 0, :], _out_points_boxes[:, 3, :]], dim=1)
    right_side = intersection_line(line1_point, line_tile)
    left_side = intersection_line(line2_point, line_tile)
    delta_shift = torch.zeros_like(left_side)
    positive_angle = _out_bboxes[:, 4] > 0
    negative_angle = _out_bboxes[:, 4] <= 0
    # print('_out_bboxes=', _out_bboxes)
    if mode == 'inside':
        if side == 'top':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 0, :] - left_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 1, :] - right_side[negative_angle]
        if side == 'bottom':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 2, :] - right_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 3, :] - left_side[negative_angle]
        if side == 'left':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 3, :] - left_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 0, :] - left_side[negative_angle]
        if side == 'right':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 1, :] - right_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 2, :] - right_side[negative_angle]
    elif mode == 'outside':
        if side == 'top':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 1, :] - right_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 0, :] - left_side[negative_angle]
        if side == 'bottom':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 3, :] - left_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 2, :] - right_side[negative_angle]
        if side == 'left':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 2, :] - right_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 1, :] - right_side[negative_angle]
        if side == 'right':
            delta_shift[positive_angle] = _out_points_boxes[positive_angle, 0, :] - left_side[positive_angle]
            delta_shift[negative_angle] = _out_points_boxes[negative_angle, 3, :] - left_side[negative_angle]

    res_point_bboxes = deepcopy(_out_points_boxes)

    if side == 'top':
        res_point_bboxes[:, 0:2, :] -= torch.stack([delta_shift, delta_shift], dim=1)
    elif side == 'bottom':
        res_point_bboxes[:, 2:4, :] -= torch.stack([delta_shift, delta_shift], dim=1)
    elif side == 'left':
        res_point_bboxes[positive_angle, 2:4, :] -= torch.stack([delta_shift, delta_shift], dim=1)[positive_angle]
        res_point_bboxes[negative_angle, 0:2, :] -= torch.stack([delta_shift, delta_shift], dim=1)[negative_angle]
    elif side == 'right':
        res_point_bboxes[positive_angle, 0:2, :] -= torch.stack([delta_shift, delta_shift], dim=1)[positive_angle]
        res_point_bboxes[negative_angle, 2:4, :] -= torch.stack([delta_shift, delta_shift], dim=1)[negative_angle]
    new_bbox = four_point2centerxy(res_point_bboxes)
    bboxes[out_index] = new_bbox
    bboxes4point[out_index] = res_point_bboxes
    return bboxes4point, bboxes


def filter_bboxes(
        image: Image,
        bboxes,
        labels,
        min_area: Optional[int] = None,
        fix_mode: str = 'inside'
):
    """
    Remove bounding boxes that either lie outside of the visible area of image,
    crop bounding boxes that partial lie outside of the visible area of image
    or remove bounding boxes whose area in pixels is under the threshold set by min_area.
    Args:
        image: PIL.Image
        bboxes:
        labels:
        min_area: threshold of bounding boxes minimal area in pixels

    Returns:

    """
    rectangle_points_coordinate = torch.Tensor(
        [
            [0, 0],
            [image.width, 0],
            [image.width, image.height],
            [0, image.height]
        ]
    )
    bboxes4point = centerxy2four_point(bboxes)
    if fix_mode == 'inside':
        out_top = (bboxes4point[:, :, 1] < rectangle_points_coordinate[0][1]).any(dim=1)
    else:
        out_top = (bboxes4point[:, [0, 1], 1] < rectangle_points_coordinate[0][1]).all(dim=1)
    if out_top.any():
        # print("fix top")
        bboxes4point, bboxes = fix_outside_side(
            bboxes4point=bboxes4point,
            bboxes=bboxes,
            out_index=out_top,
            side='top',
            rectangle_points_coordinate=rectangle_points_coordinate,
            mode=fix_mode
        )
    if fix_mode == 'inside':
        out_bottom = (bboxes4point[:, :, 1] > rectangle_points_coordinate[2][1]).any(dim=1)
    else:
        out_bottom = (bboxes4point[:, [2, 3], 1] > rectangle_points_coordinate[2][1]).all(dim=1)
    if out_bottom.any():
        # print("fix bottom")
        bboxes4point, bboxes = fix_outside_side(
            bboxes4point=bboxes4point,
            bboxes=bboxes,
            out_index=out_bottom,
            side='bottom',
            rectangle_points_coordinate=rectangle_points_coordinate,
            mode=fix_mode
        )
    positive_angle = bboxes[:, 4] > 0
    negative_angle = bboxes[:, 4] <= 0
    if fix_mode == 'inside':
        out_left = (bboxes4point[:, :, 0] < rectangle_points_coordinate[0][0]).any(dim=1)
    else:
        out_left = (positive_angle & (bboxes4point[:, [2, 3], 0] < rectangle_points_coordinate[0][0]).all(dim=1)) | \
                   (negative_angle & (bboxes4point[:, [0, 1], 0] < rectangle_points_coordinate[0][0]).all(dim=1))

    if out_left.any():
        # print("fix left")
        bboxes4point, bboxes = fix_outside_side(
            bboxes4point=bboxes4point,
            bboxes=bboxes,
            out_index=out_left,
            side='left',
            rectangle_points_coordinate=rectangle_points_coordinate,
            mode=fix_mode
        )
    if fix_mode == 'indide':
        out_right = (bboxes4point[:, :, 0] > rectangle_points_coordinate[2][0]).any(dim=1)
    else:
        out_right = positive_angle & (bboxes4point[:, [0, 1], 0] > rectangle_points_coordinate[2][0]).all(dim=1) | \
                    negative_angle & (bboxes4point[:, [2, 3], 0] > rectangle_points_coordinate[2][0]).all(dim=1)
    if out_right.any():
        # print("fix right")
        bboxes4point, bboxes = fix_outside_side(
            bboxes4point=bboxes4point,
            bboxes=bboxes,
            out_index=out_right,
            side='right',
            rectangle_points_coordinate=rectangle_points_coordinate,
            mode=fix_mode
        )
    res_bboxes = bboxes[(bboxes[:, 0] > 0) & (bboxes[:, 1] > 0) &
                        (bboxes[:, 0]/image.width < 0.9999) & (bboxes[:, 1] / image.height < 0.9999)]
    res_labels = labels[(bboxes[:, 0] > 0) & (bboxes[:, 1] > 0) &
                        (bboxes[:, 0]/image.width < 0.9999) & (bboxes[:, 1] / image.height < 0.9999)]

    if min_area is not None:
        bboxes_area = res_bboxes[:, 2] * res_bboxes[:, 3]
        res_bboxes = res_bboxes[bboxes_area > min_area]
        res_labels = res_labels[bboxes_area > min_area]

    return image, res_bboxes, res_labels