import json
import logging
from pathlib import Path
from typing import List

import imagesize
import xmltodict

from datasets.annotations import ImageAnnotation, DetectionObject
from datasets.image_dataset import ImagesDataset
from datasets.meta import DatasetMeta, FileInfo, DatasetPart, DatasetType
from datasets.annotations.bbox import BBoxXYXY, BBoxXYWH


def import_dataset(main_data_folder: Path, image_set: str) -> ImagesDataset:
    """Allows import CrowdHuman dataset.
    Args:
        main_data_folder (Path): main path to FEEDS dataset
        image_set (str): Name of image set (example: train)
    Returns:
        ImagesDataset: A class that contains meta information about a dataset.
    """
    logger = logging.getLogger(__name__)
    assert image_set in ("train", "val"), "Incorrect image_set. Valid values: 'train', 'val'"
    with open(str(main_data_folder / f"annotation_{image_set}.odgt"), 'r+') as f:
        datalist = f.readlines()
    image_folder = main_data_folder / f"CrowdHuman_{image_set}/Images"

    images_anns: List[ImageAnnotation] = []
    files_info: List[FileInfo] = []
    for line in datalist:
        data = json.loads(line)
        image_file = image_folder/f"{data['ID']}.jpg"
        width, height = imagesize.get(str(image_file))
        file_info = FileInfo(
            abs_path=image_folder/f"{data['ID']}.jpg",
            unique_id=image_file.name,
            width=width,
            height=height
        )
        files_info.append(file_info)
        objects = []
        for raw_bbox in data['gtboxes']:
            head_object = procesing_bbox(
                bbox=raw_bbox['hbox'],
                attribute=raw_bbox['head_attr'],
                label='head',
                image_width=width,
                image_height=height
            )
            if head_object:
                objects.append(head_object)

            full_object = procesing_bbox(
                bbox=raw_bbox['fbox'],
                attribute=raw_bbox['extra'],
                label='full person',
                image_width=width,
                image_height=height
            )
            if full_object:
                objects.append(full_object)

            visible_object = procesing_bbox(
                bbox=raw_bbox['vbox'],
                attribute=raw_bbox['extra'],
                label='visible person',
                image_width=width,
                image_height=height
            )
            if visible_object:
                objects.append(visible_object)

        images_anns.append(
            ImageAnnotation(
                objects=objects,
            )
        )
    crowd_dataset = ImagesDataset(
        DatasetMeta(
            name='CrowdHuman',
            version='1.0.0',
            description="WCrowdHuman is a benchmark dataset to better evaluate detectors in crowd scenarios. "
                        "The CrowdHuman dataset is large, rich-annotated and contains high diversity. "
                        "CrowdHuman contains 15000, 4370 and 5000 images for training, validation, "
                        "and testing, respectively. There are a total of 470K human instances from train "
                        "and validation subsets and 23 persons per image, with various kinds of occlusions "
                        "in the dataset. Each human instance is annotated with a head bounding-box, "
                        "human visible-region bounding-box and human full-body bounding-box. "
                        "url=https://www.crowdhuman.org/",
            part=DatasetPart(image_set),
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        crowd_dataset.add_item(file_info, ann)
    return crowd_dataset


def procesing_bbox(bbox, attribute, label, image_width, image_height):
    if bbox[2] > 0 and bbox[3] > 0:
        head_bbox_xyxy = BBoxXYWH(
            x=max(0, bbox[0]),
            y=max(0, bbox[1]),
            width=min(image_width, bbox[2]),
            height=min(image_height, bbox[3]),
        )
        dobject = DetectionObject(
            bbox=head_bbox_xyxy,
            label=label,
            attributes=dict(
                ignore=attribute["ignore"] if 'ignore' in attribute else None,
                unsure=attribute["unsure"] if 'unsure' in attribute else None,
                occ=attribute["occ"] if 'occ' in attribute else None,

            )
        )
        return dobject
    return None
