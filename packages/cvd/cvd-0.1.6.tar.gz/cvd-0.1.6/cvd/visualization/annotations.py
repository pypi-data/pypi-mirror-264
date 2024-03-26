import io
import logging
import math
import random
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
from matplotlib import pyplot as plt
import cv2

from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.image_dataset_item import ImageDatasetItem
from cvd.visualization.objects import draw_objects
from cvd.visualization.tools import get_mpl_colormap

logger = logging.getLogger(__name__)


# define a function which returns an image as numpy array from figure
def get_img_from_fig(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def draw_samples(
        dataset: ImagesDataset,
        sample_num: int = 10,
        fig_size: Tuple[int, int] = (15, 20),
        output_file: Optional[Path] = None,
        font_size: float = 1
):
    random_number = random.sample(range(0, len(dataset)), sample_num)
    columns = 2
    color_map = dict(zip(dataset.labels, get_mpl_colormap("gist_rainbow", num=len(dataset.labels))))
    rows = math.ceil(sample_num / columns)
    fig, axs = plt.subplots(rows, columns, figsize=fig_size)
    for num, ax in zip(random_number, axs.ravel()):
        ds_item = dataset[num]
        img = cv2.cvtColor(cv2.imread(str(ds_item.file_info.abs_path)), cv2.COLOR_BGR2RGB)
        img = draw_objects(
            image=img,
            objects=ds_item.annotations.objects,
            label_to_color=color_map,
            font_size=font_size
        )

        ax.imshow(img)
    result_img = get_img_from_fig(fig)
    if output_file:
        cv2.imwrite(filename=str(Path), img=result_img)
    # return result_img


def load_image(abs_path: Path):
    return cv2.cvtColor(cv2.imread(str(abs_path)), cv2.COLOR_BGR2RGB)