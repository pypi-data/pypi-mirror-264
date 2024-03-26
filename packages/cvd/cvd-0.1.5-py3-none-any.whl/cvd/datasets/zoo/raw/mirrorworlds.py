import logging
from pathlib import Path
from typing import List

import imagesize
import pandas as pd

from datasets.annotations import ImageAnnotation
from datasets.annotations.objects import DetectionObjectBBox
from datasets.image_dataset import ImagesDataset
from datasets.meta import DatasetMeta, FileInfo, DatasetPart, DatasetType
from datasets.annotations.sbbox import BBoxXYXY, BBoxXYWH


def import_dataset(main_data_folder: Path, image_set: DatasetPart) -> ImagesDataset:
    """
    The function allow import wilder dataset.
    @param main_data_folder: main path to wilder dataset
    @type main_data_folder: Path
    @return: Imported dataset in specific structure
    @rtype: ImagesDataset
    """
    video_frame_dirs = []
    if image_set.value == 'train':
        data_dir = main_data_folder / 'Train'
    else:
        raise Exception("Raw dataset doesn't contain another part")
    for item in data_dir.iterdir():
        if item.is_dir():
            video_frame_dirs.append(item)

    images_anns: List[ImageAnnotation] = []
    files_info: List[FileInfo] = []
    for video_path in video_frame_dirs:
        anns_df = pd.read_csv(video_path / 'gt' / 'gt.txt')
        anns_df.columns = ["frame_num", "id", "xmin", "ymin", "width", "height", "conf", "x", "y", "z"]
        frame_images = sorted(list((video_path/'img1').glob("*.png")))
        for frame_image_path in frame_images:
            frame_num = int(frame_image_path.stem)
            width, height = imagesize.get(str(frame_image_path))
            files_info.append(
                FileInfo(
                    abs_path=frame_image_path,
                    unique_id=f"{frame_image_path.parent.parent.stem}_{frame_image_path.name}",
                    width=width,
                    height=height
                )
            )
            objects = []
            for _, row in anns_df[anns_df.frame_num == frame_num].iterrows():
                objects.append(
                    DetectionObjectBBox(
                        bbox=BBoxXYWH(
                            x=row.xmin,
                            y=row.ymin,
                            width=row.width,
                            height=row.height
                        ),
                        label='person'
                    )
                )
            images_anns.append(
                ImageAnnotation(objects=objects)
            )
    mw_dataset = ImagesDataset(
        DatasetMeta(
            name='MirrorWorlds',
            version='1.0.0',
            description="Mirror Worlds (MW) dataset are created based on a top-view fisheye camera videos "
                        "MW is a image dataset with 30 videos and 13k frames overall. The dataset is "
                        "very useful for research on people detection from overhead fisheye cameras. "
                        "All person objects in the videos are annotated with axis-aligned bounding boxes.",
            part=image_set,
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        mw_dataset.add_item(file_info, ann)
    return mw_dataset
