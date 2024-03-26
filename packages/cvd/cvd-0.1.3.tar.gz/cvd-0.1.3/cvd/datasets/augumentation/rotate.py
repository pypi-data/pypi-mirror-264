import torch
import torchvision.transforms.functional as tvf
from PIL import Image
from torch import FloatTensor
import numpy as np


def rotate(
        image: Image,
        bboxes: FloatTensor,
        labels: FloatTensor,
        degrees,
        expand: bool = False
):
    """

    Args:
        image: PIL.Image input image
        bboxes: tensor, shape(N,5), absolute x,y,w,h, angle in degree of bounding boxes
        labels: tensor, shape(N), bounding boxes labels
        degrees: angle in degree
        expand:

    Returns:

    """

    img_w, img_h = image.width, image.height
    image = tvf.rotate(image, angle=-degrees, expand=expand)
    new_w, new_h = image.width, image.height
    # image coordinate to cartesian coordinate
    x = bboxes[:, 0] - 0.5 * img_w
    y = - (bboxes[:, 1] - 0.5 * img_h)

    # cartesian to polar
    r = (x.pow(2) + y.pow(2)).sqrt()

    theta = torch.empty_like(r)
    theta[x >= 0] = torch.atan(y[x >= 0]/x[x >= 0])
    theta[x < 0] = torch.atan(y[x < 0]/x[x < 0]) + np.pi
    theta[torch.isnan(theta)] = 0

    # modify theta
    theta -= (degrees*np.pi/180)

    # polar to cartesian
    x = r * torch.cos(theta)
    y = r * torch.sin(theta)
    bboxes[:, 0] = x + 0.5 * new_w
    bboxes[:, 1] = -y + 0.5 * new_h
    bboxes[:, 4] += degrees
    bboxes[:, 4] = torch.remainder(bboxes[:, 4], 180)
    bboxes[:, 4][bboxes[:, 4] >= 90] -= 180

    return image, bboxes, labels
