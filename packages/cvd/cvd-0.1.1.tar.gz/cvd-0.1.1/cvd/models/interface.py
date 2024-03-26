from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from typing import List

from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.objects import PredictedObject, TrackPRObject
from cvd.datasets.annotations.video_annotation import VideoAnnotation, Frame
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.image_dataset_item import ImageDatasetItem
import numpy as np

from cvd.datasets.video_dataset import VideoDataset

from tqdm.auto import tqdm


class PredictionModel(ABC):

    @abstractmethod
    def load_model(self, weight_file: Path):
        pass

    @abstractmethod
    def _predict(self, img: np.ndarray) -> List[PredictedObject]:
        pass

    def predict_on_images(self, ds: ImagesDataset, *args, **kwargs) -> ImagesDataset:
        pred_ds_meta = deepcopy(ds.dataset_meta)
        pred_ds_meta.description = "Prediction: " + pred_ds_meta.description
        pred_ds = ImagesDataset(dataset_meta=pred_ds_meta)
        ds_item: ImageDatasetItem
        for ds_item in tqdm(ds):
            pred_list = self._predict(ds_item.load_image(), *args, **kwargs)
            pred_ds.add_item(
                file_info=ds_item.file_info,
                annotation=ImageAnnotation(
                    objects=pred_list
                )
            )
        return pred_ds

    def predict_on_video(self, ds: VideoDataset) -> VideoDataset:
        pred_ds_meta = deepcopy(ds.dataset_meta)
        pred_ds_meta.description = "Prediction: " + pred_ds_meta.description
        pred_ds = VideoDataset(dataset_meta=pred_ds_meta)
        main_pbar = tqdm(ds, desc='video files')
        for ds_item in main_pbar:
            main_pbar.set_description(f"Processing {ds_item.file_info.abs_path.name}")
            frame_list_anns = []
            pbar = tqdm(ds_item, desc='frames', leave=False, total=ds_item.file_info.frames_number)
            for frame_img, frame_annotation in pbar:
                pred_list = self._predict(frame_img)
                frame_list_anns.append(
                    Frame(
                        objects=pred_list,
                        number=frame_annotation.number
                    )
                )
                pbar.update()
            pred_ds.add_item(
                file_info=ds_item.file_info,
                annotation=VideoAnnotation(frames=frame_list_anns)
            )
            main_pbar.update()
        return pred_ds


class TrackPredictionModel(PredictionModel, ABC):

    @abstractmethod
    def _track_predict(self, predicted_obj: List[PredictedObject]) -> List[TrackPRObject]:
        pass

    def predict_on_video(self, ds: VideoDataset) -> VideoDataset:
        pred_ds_meta = deepcopy(ds.dataset_meta)
        pred_ds_meta.description = "Prediction: " + pred_ds_meta.description
        pred_ds = VideoDataset(dataset_meta=pred_ds_meta)
        main_pbar = tqdm(ds, desc='video files')
        for ds_item in main_pbar:
            main_pbar.set_description(f"Processing {ds_item.file_info.abs_path.name}")
            frame_list_anns = []
            pbar = tqdm(ds_item, desc='frames', leave=False, total=ds_item.file_info.frames_number)
            for frame_img, frame_annotation in pbar:
                pred_list = self._predict(frame_img)
                track_list = self._track_predict(pred_list)
                frame_list_anns.append(
                    Frame(
                        objects=track_list,
                        number=frame_annotation.number
                    )
                )
                pbar.update()
            pred_ds.add_item(
                file_info=ds_item.file_info,
                annotation=VideoAnnotation(frames=frame_list_anns)
            )
            main_pbar.update()
        return pred_ds
