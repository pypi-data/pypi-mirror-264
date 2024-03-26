from typing import Tuple

import torchvision.transforms.functional as tvf
from PIL.Image import Image
from torch import FloatTensor


def horizontal_flip(
        image: Image,
        bboxes: FloatTensor,
        labels: FloatTensor,
) -> Tuple[Image, FloatTensor, FloatTensor]:
    """
    left-right flip

    Args:
        image: PIL Image
        bboxes: tensor, shape(N,5), absolute x,y,w,h, angle in degree
        labels: tensor, shape(N), bounding box labels
    """
    image: Image = tvf.hflip(image)
    bboxes[:, 0] = image.width - bboxes[:, 0]  # x,y,w,h,(angle)
    bboxes[:, 4] = -bboxes[:, 4]
    return image, bboxes, labels


def vertical_flip(
        image: Image,
        bboxes: FloatTensor,
        labels: FloatTensor
) -> Tuple[Image, FloatTensor, FloatTensor]:
    """
    up-down flip

    Args:
        image: PIL.Image
        bboxes: tensor, shape(N,5), absolute x,y,w,h, angle in degree
        labels: tensor, shape(N), bounding box labels
    """

    image: Image = tvf.vflip(image)
    bboxes[:, 1] = image.height - bboxes[:, 1]  # x,y,w,h,(angle)
    bboxes[:, 4] = -bboxes[:, 4]
    return image, bboxes, labels
