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
    """Allows import WiderFace dataset.
    Args:
        main_data_folder (Path): main path to FEEDS dataset
        image_set (str): Name of image set (example: train)
    Returns:
        ImagesDataset: A class that contains meta information about a dataset.
    """
    logger = logging.getLogger(__name__)
    with open(main_data_folder/f"{image_set}"/f"wider_face_{image_set}_bbx_gt.txt", 'r') as f:
        images_names_bbox_attributes = [x for x in f.read().splitlines()]

    images_anns = []
    files_info:List[FileInfo] = []
    i = 0
    blur_type = {0: "clear", 1: "mormal blur", 2: "heavy blur"}
    expression_type = {0: "typical expression", 1: "exaggerate expression"}
    illumination_type = {0:"normal illumination", 1: "extreme illumination"}
    invalid_type = {0: "valid image", 1: "invalid image"}
    occlusion_type = {0: "no occlusion", 1: "partial occlusion", 2: "heavy occlusion"}
    pose_type = {0: "typical pose", 1: "atypical pose"}

    while i < len(images_names_bbox_attributes):
        rel_path = Path(images_names_bbox_attributes[i])
        abs_path = main_data_folder/f"{image_set}"/"images"/rel_path
        width, height = imagesize.get(str(abs_path))
        file_info = FileInfo(
            abs_path=abs_path,
            unique_id=str(rel_path),
            width=width,
            height=height
        )
        files_info.append(file_info)
        i+=1

        bbox_number = int(images_names_bbox_attributes[i])
        i+=1
        objects = []
        for j in range(bbox_number):
            # print(images_names_bbox_attributes[i+j])
            bbox_attributes = list(map(int, images_names_bbox_attributes[i+j].rstrip().split(" ")))
            x = bbox_attributes[0]
            y = bbox_attributes[1]
            width = bbox_attributes[2]
            height = bbox_attributes[3]
            blur = blur_type[bbox_attributes[4]]
            expression = expression_type[bbox_attributes[5]]
            illumination = illumination_type[bbox_attributes[6]]
            invalid = invalid_type[bbox_attributes[7]]
            occlusion = occlusion_type[bbox_attributes[8]]
            pose = pose_type[bbox_attributes[9]]
            # The coordinates are sometimes slightly less than 0.
            # In order not to lose the marked objects we set them equal to 0.
            if 0 <= x < file_info.width and 0 <= y < file_info.height \
                    and x + width <= file_info.width and y + height <= file_info.height \
                        and width>0 and height>0:
                bbox_xyxy = BBoxXYWH(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                )
                det_object = DetectionObject(
                    bbox=bbox_xyxy,
                    label='face',
                    attributes=dict(
                        blur=blur,
                        expression=expression,
                        illumination=illumination,
                        invalid=invalid,
                        occlusion=occlusion,
                        pose=pose,
                    )
                )
                objects.append(det_object)
            else:

                logger.warning(f"Incorrect annotations for images {rel_path}. "
                               f"BBox coordinates: x={x}, y={y}, width={width}, height={height}, "
                               f"Image: width={file_info.width}, height={file_info.height}")
        i+=bbox_number
        images_anns.append(
            ImageAnnotation(
                objects=objects,
            )
        )
    wf_dataset = ImagesDataset(
        DatasetMeta(
            name='WiderFace',
            version='1.0.0',
            description="WIDER FACE dataset is a face detection benchmark dataset, of which images are selected "
                        "from the publicly available WIDER dataset.32,203 images and label 393,703 faces with "
                        "a high degree of variability in scale, pose and occlusion as depicted in the sample "
                        "images. WIDER FACE dataset is organized based on 61 event classes. For each event class, "
                        "we randomly select 40%/10%/50% data as training, validation and testing sets. "
                        "url=http://shuoyang1213.me/WIDERFACE/",
            part=DatasetPart(image_set),
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        wf_dataset.add_item(file_info, ann)
    return wf_dataset
