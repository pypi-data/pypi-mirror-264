from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
from matplotlib import pyplot as plt

from cvd.datasets.annotations.type import ObjectsSet
from cvd.datasets.annotations.video_annotation import VideoAnnotation, Frame
from cvd.datasets.meta import VideoFileInfo
from cvd.visualization.objects import draw_objects
from cvd.visualization.tools import get_mpl_colormap


@dataclass
class VideoDatasetItem:
    file_info: VideoFileInfo
    annotations: Optional[VideoAnnotation]

    def __post_init__(self):
        self._last_frame = -1
        self._cap = cv2.VideoCapture(str(self.file_info.abs_path))

    def show_frame(
            self,
            frame_number: int,
            fig_size: Tuple[int, int] = (15, 20),
            show_conf: bool = False,
            show_track_id: bool = False,
            draw_top: bool = False,
            draw_center_point: bool = False
    ):
        img = self._load_frame(frame_number)
        res_img = self._draw_objects(
            image=img,
            objects=self.annotations[frame_number].objects,
            draw_top=draw_top,
            show_conf=show_conf,
            show_track_id=show_track_id,
            draw_center_point=draw_center_point
        )
        fig, axs = plt.subplots(1, 1, figsize=fig_size)
        axs.imshow(res_img)

    def _draw_objects(
            self,
            image: np.ndarray,
            objects: ObjectsSet,
            show_conf: bool = False,
            show_track_id: bool = False,
            draw_top: bool = False,
            draw_center_point: bool = False
    ):
        color_map = dict(
            zip(self.annotations.labels, get_mpl_colormap("gist_rainbow", num=len(self.annotations.labels)))
        )
        res_img = draw_objects(
            image=image,
            objects=objects,
            label_to_color=color_map,
            show_conf=show_conf,
            show_track_id=show_track_id,
            draw_top=draw_top,
            draw_center_point=draw_center_point
        )
        return res_img

    def generate_video(
            self,
            output_folder: Path,
            output_file_name: str,
            show_conf: bool = False,
            show_track_id: bool = False,
            draw_top: bool = False,
            draw_center_point: bool = False
    ):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_folder.mkdir(parents=True, exist_ok=True)
        out = cv2.VideoWriter(
            str(output_folder / f"{output_file_name}.mp4"),
            fourcc,
            self.file_info.fps,
            (self.file_info.width, self.file_info.height)
        )
        for frame_image, frame_ann in self:
            out.write(
                cv2.cvtColor(
                    self._draw_objects(
                        image=frame_image,
                        objects=frame_ann.objects,
                        show_conf=show_conf,
                        show_track_id=show_track_id,
                        draw_top=draw_top,
                        draw_center_point=draw_center_point
                    ),
                    cv2.COLOR_RGB2BGR)
            )
        out.release()

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self) -> Tuple[np.ndarray, Frame]:
        if self._current >= self.file_info.frames_number:
            raise StopIteration
        else:
            frame_img = self._load_frame(self._current)
            frame_ann = self.annotations[self._current]
            self._current += 1
            return frame_img, frame_ann

    def get_frame(self, number: int):
        return self._load_frame(number)

    def _load_frame(self, frame_number: int) -> np.ndarray:
        if frame_number > self._last_frame:
            while self._last_frame != frame_number:
                self._cap.grab()
                self._last_frame += 1
            res, frame = self._cap.retrieve()
            self._frame = frame
        elif frame_number < self._last_frame:
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self._last_frame = -1
            self._load_frame(frame_number)
        return cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)