import json
from collections import defaultdict
from pathlib import Path
from typing import List

import imagesize

from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.objects import TrackGTObjectBBox
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.meta import DatasetMeta, DatasetPart, DatasetType, ImageFileInfo


def import_dataset(main_data_folder: Path, image_set: DatasetPart) -> ImagesDataset:
    """
    The function allow import MW18 dataset.
    @param main_data_folder: main path to wilder dataset
    @type main_data_folder: Path
    @param image_set: Type of dataset
    @type image_set: DatasetPart
    @return: Imported dataset in specific structure
    @rtype: ImagesDataset
    """
    if image_set.value == 'all':
        ann_folder = main_data_folder / 'annotations'
    else:
        raise Exception(f"Raw dataset doesn't contain {image_set.value} part")
    images_anns: List[ImageAnnotation] = []
    files_info: List[ImageFileInfo] = []
    for ann_file in ann_folder.glob('*.json'):
        with open(ann_file, 'r') as fin:
            frame_anns = json.load(fin)
        frame_anns_dict = defaultdict(list)
        for ann in frame_anns['annotations']:
            frame_anns_dict[ann['image_id']].append(ann)
        frame_images_folder = main_data_folder / f'MW18rAll'
        for frame_image_path in frame_images_folder.glob('*.png'):
            width, height = imagesize.get(str(frame_image_path))
            files_info.append(
                ImageFileInfo(
                    abs_path=frame_image_path,
                    unique_id=frame_image_path.stem,
                    width=width,
                    height=height
                )
            )
            objects = []
            for ann in frame_anns_dict[frame_image_path.stem]:
                if ann['bbox'][1] < ann['bbox'][3]/2:
                    ann['bbox'][3] = ann['bbox'][3]/2 + ann['bbox'][1]
                    ann['bbox'][1] = ann['bbox'][3]/2
                objects.append(
                    TrackGTObjectBBox(
                        bbox=RBBoxXYCenterWHA(
                            x_center=ann['bbox'][0],
                            y_center=ann['bbox'][1],
                            width=ann['bbox'][2],
                            height=ann['bbox'][3],
                            angle=ann['bbox'][4] if ann['bbox'][4] > 0 else ann['bbox'][4]+180
                        ),
                        label='person',
                        track_id=ann['person_id'] if isinstance(ann['person_id'], int) and ann['person_id'] > 0 else -1
                    )
                )
            images_anns.append(
                ImageAnnotation(objects=objects)
            )
    cepdof_dataset = ImagesDataset(
        DatasetMeta(
            name='MWR',
            version='1.0.0',
            description="Mirror Worlds (MW) Challenge is a project at Virginia Tech’s Institute for Creativity, "
                        "Arts and Technology that provides a top-view fisheye image dataset with 30 videos and "
                        "13k frames overall. The dataset is very useful for research on people detection from "
                        "overhead fisheye cameras. To evaluate our algorithms on the MW dataset and "
                        "to provide more resources for the research community, Visual Information Processing "
                        "(VIP) Laboratory manually annotated a subset of the MW dataset "
                        "with rotated bounding-box labels, that we refer to as MW-R. "
                        "Similarly to CEPDOF dataset, MW-R is annotated spatio-temporally, "
                        "that is bounding boxes of the same person carry the same ID in "
                        "consecutive frames, and thus can be also used for additional vision "
                        "tasks using overhead, fisheye images, such as video-object tracking "
                        "and human re-identification.",
            part=image_set,
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        cepdof_dataset.add_item(file_info, ann)
    return cepdof_dataset
