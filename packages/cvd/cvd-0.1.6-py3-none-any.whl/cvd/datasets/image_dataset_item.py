from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, Dict

import cv2
from matplotlib import pyplot as plt

from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.meta import ImageFileInfo
from cvd.visualization.objects import draw_objects
from cvd.visualization.tools import get_mpl_colormap


@dataclass
class ImageDatasetItem:
    """Just for bboxes objects annotation"""
    file_info: ImageFileInfo
    annotations: Optional[ImageAnnotation]

    def show(
            self,
            fig_size: Tuple[int, int] = (15, 20),
            annotation: bool = True,
            show_conf: bool = True
    ):
        fig, axs = plt.subplots(1, 1, figsize=fig_size)
        if annotation:
            res_img = self.draw_annotations(show_conf=show_conf)
        else:
            res_img = self.load_image()
        axs.imshow(res_img)
        plt.show()
        plt.close()

    def draw_annotations(self, show_conf: bool = False):
        img = cv2.cvtColor(cv2.imread(str(self.file_info.abs_path)), cv2.COLOR_BGR2RGB)
        color_map = dict(
            zip(self.annotations.labels, get_mpl_colormap("gist_rainbow", num=len(self.annotations.labels)))
        )

        res_img = draw_objects(
            image=img,
            objects=self.annotations.objects,
            show_conf=show_conf,
            label_to_color=color_map
        )
        return res_img

    def load_image(self):
        try:
            return cv2.cvtColor(cv2.imread(str(self.file_info.abs_path)), cv2.COLOR_BGR2RGB)
        except Exception:
            raise

    def __repr__(self):
        return f"{self.__class__.__name__}(file_info={self.file_info}, annotations={self.annotations})"