from copy import deepcopy
from typing import Union, List, Tuple, Mapping

import cv2
import numpy as np

from cvd.datasets.annotations.objects import DetectionObjectBBox, TrackPRObject
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.annotations.type import ObjectsSet
from cvd.visualization.tools import draw_colormap
from cvd.visualization.type import RGB


# Sum of the min & max of (a, b, c)
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c


def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))


def draw_objects(
    image: np.ndarray,
    objects: ObjectsSet,
    label_to_color: Mapping[str, RGB],
    thickness: int = 2,
    font_size: float = 1,
    show_conf: bool = False,
    show_track_id: bool = False,
    draw_top: bool = False,
    draw_center_point: bool = False
) -> np.ndarray:
    ann_image = deepcopy(image)
    scale_factor = int(min(ann_image.shape[:2]) // 400)
    for obj in objects:
        contours = np.array(list(map(lambda x: (int(x[0]), int(x[1])), obj.contours())))
        cv2.polylines(
            ann_image,
            [contours],
            isClosed=True,
            color=label_to_color[obj.label],
            thickness=thickness
        )
        hint_str = ""
        if show_conf and hasattr(obj, "confidence"):
            hint_str += f'{obj.confidence:.2f}'
        if show_track_id:
            if isinstance(obj, TrackPRObject):
                hint_str += f" tr_id: {obj.track_id}"
            else:
                hint_str += f" tr_id: NaN"

        if hint_str:
            try:
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = 1
                font_bold = max(int(2 * text_size), 1)
                cv2.putText(
                    ann_image,
                    hint_str,
                    (int(contours[0][0]), int(contours[0][1])),
                    font,
                    1*text_size,
                    label_to_color[obj.label],
                    font_bold,
                    cv2.LINE_AA
                )
            except AttributeError as e:
                raise e
        if draw_top:
            cv2.line(
                ann_image,
                (contours[0][0], contours[0][1]),
                (contours[1][0], contours[1][1]),
                complement(*label_to_color[obj.label]),
                thickness=1 * max(1, scale_factor)
            )
        if draw_center_point:
            tmp_obj: RBBoxXYCenterWHA = obj.bbox.toxycenterwha()
            cv2.circle(
                ann_image,
                (int(tmp_obj.x_center), int(tmp_obj.y_center)),
                1 * max(1, scale_factor*2),
                label_to_color[obj.label],
                thickness=1 * max(1, scale_factor*2)
            )
    ann_image = draw_colormap(
        image=ann_image,
        labels_color_map=label_to_color,
        font_size=font_size
    )
    return ann_image