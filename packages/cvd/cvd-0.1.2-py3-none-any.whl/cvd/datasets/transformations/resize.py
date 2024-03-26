from typing import Tuple, Optional

import torch
from PIL.Image import Image
from torch import FloatTensor, IntTensor
from torchvision import transforms

from cvd.datasets.augumentation.utils import centerxy2four_point, four_point2centerxy


def resize(
        image: Image,
        bboxes: Optional[FloatTensor] = None,
        labels: Optional[IntTensor] = None,
        target_size: Tuple[int, int] = (704, 704),
        pad_value=0,
        save_proportion=True
):
    """Resize image

    1. Resize img such that the longer side of the image = target_size if save_proportion is True;
    2. Pad the img it to square

    Arguments:
        image: PIL image
        bboxes: torch.tensor, shape(N,5), [cx, cy, w, h, angle], not normalized
        labels:
        target_size: Tuple[int, int], [width, height]
        pad_value: int
        save_proportion:
    """
    assert isinstance(image, Image)
    # print("target_size=", target_size)
    target_width, target_height = target_size
    ori_h, ori_w = image.height, image.width

    # resize to target input size (usually smaller)
    # print(min(target_width/ori_w, target_height / ori_h))
    if save_proportion:
        resize_scale_w = resize_scale_h = min(target_width/ori_w, target_height / ori_h)
        # unpad_w, unpad_h = target_size * w / max(w,h), target_size * h / max(w,h)
        unpad_w, unpad_h = int(ori_w * resize_scale_w), int(ori_h * resize_scale_h)
        # print("unpad_w=", unpad_w)
        # print("unpad_h=", unpad_h)
        image = image.resize((unpad_h, unpad_w))
    else:
        resize_scale_w = target_width / ori_w
        resize_scale_h = target_height / ori_h
        image = image.resize(target_size)
        unpad_w, unpad_h = target_size
        # pad to square

    # print(image.size)
    left = (target_width - unpad_w) // 2
    top = (target_height - unpad_h) // 2
    right = target_width - unpad_w - left
    bottom = target_height - unpad_h - top

    # print("left=", left)
    # print("top=", top)
    # print("right=", right)
    # print("bottom=", bottom)

    image = transforms.functional.pad(image, padding=(top, right, bottom, left), fill=pad_value)
    # record the padding info
    # print("image.size", image.size)
    img_tl = (left, top)  # start of the true image
    img_wh = (unpad_w, unpad_h)

    # modify labels
    if bboxes is not None and bboxes.shape[0] > 0:
        if save_proportion:
            bboxes[:, [0, 2]] *= resize_scale_w
            bboxes[:, [1, 3]] *= resize_scale_h
            bboxes[:, 0] += left
            bboxes[:, 1] += top
        else:
            point_boxes = centerxy2four_point(bboxes)
            point_boxes[:, :, 0] *= resize_scale_w
            point_boxes[:, :, 1] *= resize_scale_h
            bboxes = four_point2centerxy(point_boxes)
    pad_info = torch.Tensor((ori_w, ori_h) + img_tl + img_wh)
    if bboxes is None and labels is None:
        return image, pad_info
    return image, bboxes, labels, pad_info
