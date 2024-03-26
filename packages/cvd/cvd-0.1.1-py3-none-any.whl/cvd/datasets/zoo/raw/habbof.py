from pathlib import Path
from typing import List

import imagesize
import pandas as pd

from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.objects import DetectionObjectBBox
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.meta import DatasetMeta, DatasetPart, DatasetType, ImageFileInfo


def import_dataset(main_data_folder: Path, image_set: DatasetPart) -> ImagesDataset:
    """
    The function allow import HABBOF dataset.
    @param main_data_folder: main path to wilder dataset
    @type main_data_folder: Path
    @param image_set: Type of dataset
    @type image_set: DatasetPart
    @return: Imported dataset in specific structure
    @rtype: ImagesDataset
    """
    if image_set.value != 'all':
        raise Exception(f"Raw dataset doesn't contain {image_set.value} part")
    images_anns: List[ImageAnnotation] = []
    files_info: List[ImageFileInfo] = []
    for video_path in main_data_folder.iterdir():
        for ann_file in video_path.glob('*.txt'):
            ann_frame = pd.read_csv(ann_file, delimiter=' ', names=['class', 'x', 'y', 'width', 'height', 'angle'])
            frame_image_path = video_path / f'{ann_file.stem}.jpg'
            width, height = imagesize.get(str(frame_image_path))
            files_info.append(
                ImageFileInfo(
                    abs_path=frame_image_path,
                    unique_id=video_path.stem + "_" + frame_image_path.stem,
                    width=width,
                    height=height
                )
            )
            objects = []
            for _, ann in ann_frame.iterrows():
                objects.append(
                    DetectionObjectBBox(
                        bbox=RBBoxXYCenterWHA(
                            x_center=ann.x,
                            y_center=ann.y,
                            width=ann.width,
                            height=ann.height,
                            angle=ann.angle if ann.angle > 0 else ann.angle + 180
                        ),
                        label='person',
                    )
                )
            images_anns.append(
                ImageAnnotation(objects=objects)
            )
    habbof_dataset = ImagesDataset(
        DatasetMeta(
            name='HABBOF',
            version='1.0.0',
            description="Human-Aligned Bounding Boxes from Overhead Fisheye cameras dataset (HABBOF). "
                        "Human-Aligned Bounding Boxes from Overhead Fisheye cameras (HABBOF) dataset has "
                        "been developed at the Visual Information Processing (VIP) Laboratory at Boston "
                        "University and published in September 2019. The dataset contains 4 videos "
                        "recorded by overhead-mounted fisheye cameras in two different rooms "
                        "(a computer lab and a small conference room) and associated annotations of 5,837 "
                        "frames in total. In these videos, 3 or 4 people perform daily activities like standing, "
                        "walking, sitting, and writing on a whiteboard. In some videos, lights are being turned "
                        "on and off, and some furniture is moved. This increases realism and the level of difficulty "
                        "for tasks such as people detection and tracking. ",
            part=image_set,
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        habbof_dataset.add_item(file_info, ann)
    return habbof_dataset
