import itertools
import logging
from pathlib import Path
from typing import List

import imagesize
from pycocotools.coco import COCO
from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.objects import DetectionObjectBBox, DetectionObjectPolygon
from cvd.datasets.annotations.polygon import Polygon
from cvd.datasets.annotations.sbbox import BBoxXYWH
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.meta import DatasetMeta, FileInfo, DatasetPart, DatasetType, ImageFileInfo

import numpy as np


def coco_polygon2cvd_polygon(coco_points):
    polygon_points = []
    coco_points = np.array(list(itertools.chain(*coco_points))).reshape((-1, 2))
    for point in coco_points:
        x = float(point[0])
        y = float(point[1])
        polygon_points.append((x, y))
    return Polygon(polygon_points)


def import_dataset(main_data_folder: Path,  result_image_set: DatasetPart, import_type: str) -> ImagesDataset:
    """
    The function allow import wilder dataset.
    @param main_data_folder: main path to coco dataset
    @type main_data_folder: Path
    @param result_image_set: Determines which part of the dataset is imported.
    @type result_image_set: DatasetPart
    @return: Imported dataset in specific structure
    @param import_type: Type of imported annotations. Two options are possible: 'bbox' or 'segmentation'
    @type import_type: str
    @rtype: ImagesDataset
    """
    if result_image_set == DatasetPart.TRAIN:
        raw_image_set = 'train2017'
    elif result_image_set == DatasetPart.VALIDATION:
        raw_image_set = 'val2017'
    elif result_image_set == DatasetPart.TEST:
        raw_image_set = ''

    logger = logging.getLogger(__name__)
    if result_image_set == DatasetPart.TEST:
        coco = None
    else:
        coco = COCO(main_data_folder / "annotations" / f"instances_{raw_image_set}.json")
        # get all images containing given categories, select one at random
        cat_ids = coco.getCatIds()
        img_ids = coco.getImgIds()

    images_anns: List[ImageAnnotation] = []
    files_info: List[FileInfo] = []
    for img_id in img_ids:
        img_info = coco.loadImgs(img_id)[0]
        ann_ids = coco.getAnnIds(imgIds=img_info['id'], catIds=cat_ids, iscrowd=False)
        anns = coco.loadAnns(ann_ids)
        objects = []
        for obj in anns:
            if import_type == 'bbox':
                bbox = obj["bbox"]
                x = round(bbox[0])
                y = round(bbox[1])
                width = round(bbox[2])
                height = round(bbox[3])
                if x >= 0 and y >= 0 and width > 0 and height > 0:
                    objects.append(
                        DetectionObjectBBox(
                            bbox=BBoxXYWH(
                                x=x,
                                y=y,
                                width=width,
                                height=height
                            ),
                            label=coco.cats[obj["category_id"]]["name"]
                        )
                    )
                else:
                    logger.warning(f"Incorrect annotations for images {img_id}. BBox coordinates: {obj['bbox']}")
            elif import_type == 'segmentation':
                polygon = coco_polygon2cvd_polygon(obj["segmentation"])
                det_obj_poly = DetectionObjectPolygon(
                    polygon=polygon,
                    label=coco.cats[obj["category_id"]]["name"]
                )
                objects.append(det_obj_poly)
            else:
                raise Exception(f"Incorrect `import_type`. import type is {import_type} "
                                f"but possible value is: 'bbox' or 'segmentation'")

        images_anns.append(
            ImageAnnotation(
                objects=objects,
            )
        )
        abs_path = main_data_folder / Path("images") / raw_image_set / img_info["file_name"]
        width, height = imagesize.get(str(abs_path))
        files_info.append(
            ImageFileInfo(
                abs_path=abs_path,
                unique_id=img_info["file_name"],
                width=width,
                height=height
            )
        )
    coco_dataset = ImagesDataset(
        DatasetMeta(
            name='COCO' if import_type == 'bbox' else 'COCO_segmentation',
            version='1.0.0',
            description="COCO is a large-scale object detection, segmentation, and captioning dataset. "
                        "url=https://cocodataset.org/#home",
            part=result_image_set,
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        coco_dataset.add_item(file_info, ann)
    return coco_dataset
