import torch


def normalize_bbox(xywha, w, h, max_angle=1):
    '''
    Normalize bounding boxes to 0~1 range

    Args:
        xywha: torch.tensor, bounding boxes, shape(...,5)
        w: image width
        h: image height
        max_angle: the angle will be divided by max_angle
    '''
    assert torch.is_tensor(xywha)

    if xywha.dim() == 1:
        assert xywha.shape[0] == 5
        xywha[0] /= w
        xywha[1] /= h
        xywha[2] /= w
        xywha[3] /= h
        xywha[4] /= max_angle
    elif xywha.dim() == 2:
        assert xywha.shape[1] == 5
        xywha[:, 0] /= w
        xywha[:, 1] /= h
        xywha[:, 2] /= w
        xywha[:, 3] /= h
        xywha[:, 4] /= max_angle
    else:
        raise Exception('unkown bbox format')

    return xywha