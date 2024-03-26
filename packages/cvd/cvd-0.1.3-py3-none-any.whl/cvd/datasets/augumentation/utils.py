import numpy as np
import torch
from torch import FloatTensor


def make_vector(line_points1: FloatTensor, line_points2: FloatTensor) -> FloatTensor:
    """
    Args:
        line_points1: 
        line_points2:

    Returns:

    """
    return torch.stack([line_points2[:, 0] - line_points1[:, 0], line_points2[:, 1] - line_points1[:, 1]]).T


def tile(a: FloatTensor, dim: int, n_tile: int):
    init_dim = a.size(dim)
    repeat_idx = [1] * a.dim()
    repeat_idx[dim] = n_tile
    a = a.repeat(*(repeat_idx))
    order_index = torch.LongTensor(np.concatenate([init_dim * np.arange(n_tile) + i for i in range(init_dim)]))
    return torch.index_select(a, dim, order_index)


def get_len(v):
    """vector lenght"""
    return torch.sqrt(v[:, 0] ** 2 + v[:, 1] ** 2)


def get_angle(v1, v2):
    """ Returns the angle in degree between vectors 'v1' and 'v2'::
    """
    scalar_dot = torch.clip(
            torch.einsum('ij,ij->i', v1 * (1 / get_len(v1)).unsqueeze(1), v2 * (1 / get_len(v2)).unsqueeze(1)),
            -1.0,
            1.0
        )
    radians = torch.arccos(
        scalar_dot
    )
    # print("test3")
    # print('v1=', v1)
    # print('v2=', v2)
    # print('scalar_dot=', scalar_dot)
    # print('radians=', radians)
    result = 90 - (radians * 180) / np.pi
    # print('degree', result)

    return result


def four_point2centerxy(rect_points: FloatTensor) -> FloatTensor:
    """
    Convert bounding boxes from four point rotated rectangle representation to
     [x_center, y_center, width, height, angle] format

    Args:
        rect_points: tensor, shape [N, 4, 2]. Four points of rotated rectangle

    Returns: tensor, shape [N, 5]. [x_center, y_center, width, height, angle] format

    """
    reverser_center_x = rect_points[:, :, 0].sum(dim=1) / 4
    reverser_center_y = rect_points[:, :, 1].sum(dim=1) / 4
    v = make_vector(rect_points[:, 2, :], rect_points[:, 1, :])
    axis_vector = tile(torch.Tensor([[1, 0]]), 0, rect_points.shape[0])
    angle = get_angle(v, axis_vector)
    reverse_width = get_len(make_vector(rect_points[:, 0, :], rect_points[:, 1, :]))
    reverse_height = get_len(make_vector(rect_points[:, 1, :], rect_points[:, 2, :]))
    return torch.stack([reverser_center_x, reverser_center_y, reverse_width, reverse_height, angle]).T


def centerxy2four_point(labels: torch.FloatTensor) -> torch.FloatTensor:
    """
    Convert bounding boxes from [x_center, y_center, width, height, angle] format to
    four point polygon representation
    Args:
        labels: tensor, shape [N, 5]. [x_center, y_center, width, height, angle] format

    Returns: tensor, shape [N, 4, 2]. Four points of rotated rectangle

    """
    c, s = torch.cos(labels[:, 4] / 180 * np.pi), torch.sin(labels[:, 4] / 180 * np.pi)
    rotation_matrix = torch.stack([torch.stack([c, s]).T, torch.stack([-s, c]).T], dim=1)
    pts = torch.stack(
        [
            torch.stack([-labels[:, 2] / 2, -labels[:, 3] / 2]).T,
            torch.stack([labels[:, 2] / 2, -labels[:, 3] / 2]).T,
            torch.stack([labels[:, 2] / 2, labels[:, 3] / 2]).T,
            torch.stack([-labels[:, 2] / 2, labels[:, 3] / 2]).T,
        ],
        dim=1
    )
    c_point = torch.stack([labels[:, 0], labels[:, 1]]).T.unsqueeze(1)
    res_matmult = torch.matmul(pts, rotation_matrix)
    rect_points = c_point + res_matmult
    return rect_points


def det(diff_x: FloatTensor, diff_y: FloatTensor) -> FloatTensor:
    return diff_x[:, 0] * diff_y[:, 1] - diff_x[:, 1] * diff_y[:, 0]


def intersection_line(line1_point: FloatTensor, line2_point: FloatTensor) -> FloatTensor:
    diff_x_point: FloatTensor = torch.stack(
        [line1_point[:, 0, 0] - line1_point[:, 1, 0], line2_point[:, 0, 0] - line2_point[:, 1, 0]],
        dim=1
    )
    diff_y_point: FloatTensor = torch.stack(
        [line1_point[:, 0, 1] - line1_point[:, 1, 1], line2_point[:, 0, 1] - line2_point[:, 1, 1]],
        dim=1
    )
    div = det(diff_x_point, diff_y_point)
    d: FloatTensor = torch.stack(
        [det(line1_point[:, :, 0], line1_point[:, :, 1]), det(line2_point[:, :, 0], line2_point[:, :, 1])],
        dim=1
    )

    x = det(d, diff_x_point) / div
    y = det(d, diff_y_point) / div

    return torch.stack([x, y], dim=1)
