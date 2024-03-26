import logging
from pathlib import Path
from typing import List

import imagesize

from datasets.annotations import ImageAnnotation, DetectionObject
from datasets.image_dataset import ImagesDataset
from datasets.meta import DatasetMeta, FileInfo, DatasetPart, DatasetType
from datasets.annotations.bbox import BBoxXYXY

INDEX_TO_LABEL = {
    1: "pedestrian",
    2: "rider",
    3: "partially-visible person",
    4: "ignore region",
    5: "crowd"
}


def read_wider_person_labels(label_file: Path):
    logger = logging.getLogger(__name__)
    with open(label_file, 'r') as f:
        f.readline()
        labels = [x.split() for x in f.read().splitlines()]
    output_labels = []
    for label in labels:
        xmin = int(label[1])
        xmax = int(label[3])
        ymin = int(label[2])
        ymax = int(label[4])
        if xmin < xmax and ymin < ymax:
            output_labels.append(
                DetectionObject(
                    BBoxXYXY(
                        xmin=int(label[1]),
                        ymin=int(label[2]),
                        xmax=int(label[3]),
                        ymax=int(label[4])
                    ),
                    label=INDEX_TO_LABEL[int(label[0])],
                )
            )
        else:
            logger.warning(f"Label file `{label_file}` contains incorrect bbox coordinates: {label}")
    return output_labels


def import_dataset(main_data_folder: Path, image_set: str, result_image_set: DatasetPart) -> ImagesDataset:
    """
    The function allow import wilder dataset.
    @param main_data_folder: main path to wilder dataset
    @type main_data_folder: Path
    @param image_set: file name which contains set of image (example: train.txt)
    @type image_set: str
    @return: Imported dataset in specific structure
    @rtype: ImagesDataset
    """
    with open(main_data_folder/image_set, 'r') as f:
        images_names = [f"{x}.jpg" for x in f.read().splitlines()]

    images_anns: List[ImageAnnotation] = []
    files_info: List[FileInfo] = []

    for image_name in images_names:
        objects = read_wider_person_labels(main_data_folder/"Annotations"/f"{image_name}.txt")

        images_anns.append(
            ImageAnnotation(
                objects=objects,
            )
        )
        abs_path = main_data_folder/Path("Images")/image_name
        width, height = imagesize.get(str(abs_path))
        files_info.append(
            FileInfo(
                abs_path=abs_path,
                unique_id=image_name,
                width=width,
                height=height
            )
        )
    wp_dataset = ImagesDataset(
        DatasetMeta(
            name='WiderPerson',
            version='1.0.0',
            description="The WiderPerson dataset is a pedestrian detection benchmark dataset in the wild, "
                        "of which images are selected from a wide range of scenarios, no longer limited to "
                        "the traffic scenario. We choose 13,382 images and label about 400K annotations "
                        "with various kinds of occlusions. We randomly select 8000/1000/4382 images "
                        "as training, validation and testing subsets."
                        "we do not release the bounding box ground truths for the test images."
                        "url=http://www.cbsr.ia.ac.cn/users/sfzhang/WiderPerson/",
            part=result_image_set,
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        wp_dataset.add_item(file_info, ann)
    return wp_dataset
