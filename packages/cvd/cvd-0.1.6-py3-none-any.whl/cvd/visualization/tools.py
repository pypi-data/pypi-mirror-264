from copy import deepcopy
from typing import Mapping

import cv2
import numpy as np
from matplotlib import pyplot as plt

from cvd.visualization.type import RGB


def get_mpl_colormap(cmap_name: str, num: int = 5):

    cmap = plt.get_cmap(cmap_name)

    # Initialize the matplotlib color map
    sm = plt.cm.ScalarMappable(cmap=cmap)

    # Obtain linear color range
    color_range = sm.to_rgba(np.linspace(0, 1, num), bytes=True)[:, :3]
    return color_range.reshape(num, 3).tolist()


def draw_colormap(
        image: np.ndarray,
        labels_color_map: Mapping[str, RGB],
        step: int = 30,
        font_size: float = 1
):
    tmp_image = deepcopy(image)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i, (label, color) in enumerate(labels_color_map.items()):
        start_point = (0, i*step+step)
        end_point = (10, (i+1)*step+step//2)
        tmp_image = cv2.rectangle(tmp_image, start_point, end_point, color, thickness=5)
        tmp_image = cv2.putText(tmp_image, f"{label}", (14, (i+1)*step+5), font, font_size, color, 2, cv2.LINE_AA)
    return tmp_image