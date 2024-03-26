import logging
from pathlib import Path
from typing import List

import imagesize
import xmltodict

from datasets.annotations import ImageAnnotation
from datasets.annotations.objects import DetectionObjectBBox
from datasets.image_dataset import ImagesDataset
from datasets.meta import DatasetMeta, FileInfo, DatasetPart, DatasetType
from datasets.annotations.sbbox import BBoxXYXY


def import_dataset(main_data_folder: Path, image_set: str) -> ImagesDataset:
    """Allows import FEEDS dataset.
    Args:
        main_data_folder (Path): main path to FEEDS dataset
        image_set (str): Name of image set (example: train)
    Returns:
        ImagesDataset: A class that contains meta information about a dataset.
    """
    logger = logging.getLogger(__name__)
    with open(main_data_folder/"ImageSets"/"Main"/f"WI_PRW_SSM_0322_v2_{image_set}.txt", 'r') as f:
        images_names = [x for x in f.read().splitlines()]

    images_anns = []
    files_info:List[FileInfo] = []
    for image_name in images_names:

        xml_file = main_data_folder / "Annotations"/f"{Path(image_name).stem}.xml"
        with open(str(xml_file)) as fd:
            doc = xmltodict.parse(fd.read())

        anns = doc['annotation']['object'] if isinstance(doc['annotation']['object'], list) else [
            doc['annotation']['object']]

        objects = []
        for ann in anns:
            xmin = int(float(ann["bndbox"]["xmin"]))
            xmax = int(float(ann["bndbox"]["xmax"]))
            ymin = int(float(ann["bndbox"]["ymin"]))
            ymax = int(float(ann["bndbox"]["ymax"]))
            # The coordinates are sometimes slightly less than 0.
            # In order not to lose the marked objects we set them equal to 0.
            if -5 <= xmin and 0 < xmax and -5 <= ymin and 0 < ymax:
                if xmin < 0:
                    logger.warning("xmin less then 0. xmin will be set to 0")
                    xmin = 0
                if ymin < 0:
                    logger.warning("ymin less then 0. ymin will be set to 0")
                    ymin = 0

                bbox_xyxy = BBoxXYXY(
                    xmin=xmin,
                    xmax=xmax,
                    ymin=ymin,
                    ymax=ymax,
                )
                det_object = DetectionObjectBBox(
                    bbox=bbox_xyxy,
                    label=ann["name"],
                    attributes=dict(
                        truncated=ann["truncated"],
                        pose=ann["pose"]
                    )
                )
                objects.append(det_object)
            else:

                logger.warning(f"Incorrect annotations for images {image_name}. "
                               f"BBox coordinates: {ann['bndbox']}")
        images_anns.append(
            ImageAnnotation(
                objects=objects,
            )
        )
        abs_path = main_data_folder / Path("JPEGImages") / image_name
        width, height = imagesize.get(str(abs_path))
        files_info.append(
            FileInfo(
                abs_path=main_data_folder / Path("JPEGImages") / image_name,
                unique_id=image_name,
                width=width,
                height=height
            )
        )
    feeds_dataset = ImagesDataset(
        DatasetMeta(
            name='FEEDS',
            version='1.0.0',
            description="Detection dataset designed for Integrated Detection Method of Pedestrian and Face. "
                        "url=https://github.com/neverland7D/Face-and-Pedestrian-Detection-Dataset",
            part=DatasetPart(image_set),
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        feeds_dataset.add_item(file_info, ann)
    return feeds_dataset
