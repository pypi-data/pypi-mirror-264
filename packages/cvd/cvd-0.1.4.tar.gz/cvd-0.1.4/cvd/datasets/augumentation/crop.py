from typing import Tuple

from PIL.Image import Image
from torch import FloatTensor
import numpy as np
from numpy.random import randint


def random_crop(
        image: Image,
        bboxes: FloatTensor,
        labels: FloatTensor,
        min_max_width: Tuple[int, int],
        min_max_height: Tuple[int, int],
        min_max_x_center: Tuple[int, int],
        min_max_y_center: Tuple[int, int],
        save_proportion: bool = True
):
    """
    Random crop image
    Args:
        image:
        bboxes:
        labels:
        min_max_width:
        min_max_height:
        min_max_x_center:
        min_max_y_center:
        save_proportion:

    Returns:

    """
    assert min_max_width[0] > 0 and min_max_width[1] <= image.width, \
        f"min_max_width should be in range {[0, image.width]} instead {min_max_width}"
    assert min_max_height[0] > 0 and min_max_height[1] <= image.height, \
        f"min_max_width should be in range {[0, image.height]} instead {min_max_height}"

    x_center = randint(*min_max_x_center)
    y_center = randint(*min_max_y_center)
    if save_proportion:
        width = randint(*min_max_width)
        height = image.height / image.width * width
    else:
        width = randint(*min_max_width)
        height = randint(*min_max_height)
    x_min = max(x_center - width // 2, 0)
    y_min = max(y_center - height // 2, 0)
    x_max = min(x_center + width // 2, image.width)
    y_max = min(y_center + height // 2, image.height)
    image = image.crop((x_min, y_min, x_max, y_max))
    bboxes[:, 0] -= x_min
    bboxes[:, 1] -= y_min

    return image, bboxes, labels




