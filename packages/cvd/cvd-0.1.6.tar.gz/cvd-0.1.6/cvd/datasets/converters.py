from pathlib import Path
from tempfile import NamedTemporaryFile,gettempdir

from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.meta import DatasetMeta, DatasetType, ImageFileInfo
from cvd.datasets.video_dataset import VideoDataset
import cv2

from cvd.datasets.annotations.image_annotation import ImageAnnotation


def video2image_dataset(video_dataset: VideoDataset, output_images_folder: Path = None) -> ImagesDataset:
    if output_images_folder is None:
        output_images_folder = Path(gettempdir())/NamedTemporaryFile().name
    output_images_folder.mkdir(parents=True, exist_ok=True)
    video_dataset_meta = video_dataset.dataset_meta
    image_dataset_meta = DatasetMeta(
        name=video_dataset_meta.name + "_image",
        version=video_dataset_meta.version,
        description=video_dataset_meta.description,
        part=video_dataset_meta.part,
        dstype=DatasetType.IMAGE

    )
    image_dataset = ImagesDataset(dataset_meta=image_dataset_meta)
    for ds_item in video_dataset:
        for image, frame_ann in ds_item:
            height, width = image.shape[:2]
            unique_id = f"{ds_item.file_info.unique_id.split('.')[0]}_{frame_ann.number}.jpg"
            abs_path = output_images_folder / unique_id
            cv2.imwrite(str(abs_path), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            file_info = ImageFileInfo(
                abs_path=abs_path,
                unique_id=unique_id,
                width=width,
                height=height
            )
            if frame_ann.objects:
                image_dataset.add_item(
                    file_info=file_info,
                    annotation=ImageAnnotation(objects=frame_ann.objects)
                )
            else:
                image_dataset.add_item(file_info=file_info)

    return image_dataset
