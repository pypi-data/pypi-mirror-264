from pathlib import Path
from typing import Union, List, Optional

from pycocotools.coco import COCO
from tqdm import tqdm

from cvd.datasets.annotations import ImageAnnotation
from cvd.datasets.annotations.objects import DetectionObjectBBox
from cvd.datasets.annotations.sbbox import BBoxXYWH
from cvd.datasets.annotations.type import BBox
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.meta import DatasetPart, DatasetMeta, DatasetType, ImageFileInfo


def coco_images(
        image_folder: Path,
        annotations_file_path: Path,
        dataset_name: Optional[str] = None,
        dataset_description: Optional[str] = None,
        dataset_part: Union[DatasetPart, str] = DatasetPart.TRAIN
) -> ImagesDataset:
    """Create image dataset from images without annotations
    Args:
        image_folder: file with images.
        annotations_file_path: coco annotations '.json' file.
        dataset_name: Dataset name will be used in meta information about dataset.
        dataset_description: Dataset description will be used in meta information about dataset.
        dataset_part: define the dataset part, can be 'train', 'test' or 'validation'
    Returns: ImageDataset without annotation
    """
    if not image_folder.exists():
        print(f"Path: '{image_folder}' not exist.")
        raise IOError

    if isinstance(dataset_part, str):
        assert dataset_part.lower() in ['train', 'test', 'validation'], "Incorrect name of part dataset"
        _dataset_part = DatasetPart(dataset_part.lower())
    else:
        _dataset_part = dataset_part

    image_dataset = ImagesDataset(
        dataset_meta=DatasetMeta(
            name=dataset_name if dataset_name is not None else '',
            version='1.0.0',
            description=dataset_description if dataset_description is not None else '',
            part=_dataset_part,
            dstype=DatasetType.IMAGE
        )
    )

    coco_gt = COCO(str(annotations_file_path))
    cats = dict(zip(coco_gt.getCatIds(), map(lambda x: x["name"], coco_gt.loadCats(coco_gt.getCatIds()))))
    for img_info in tqdm(coco_gt.imgs.values(), total=len(coco_gt.imgs)):
        anns = coco_gt.loadAnns(coco_gt.getAnnIds(imgIds=img_info['id']))
        file_info = ImageFileInfo(
            abs_path=image_folder / img_info['file_name'],
            unique_id=img_info['file_name'],
            width=img_info['width'],
            height=img_info['height']
        )
        det_objects = []
        for ann in anns:
            bbox = BBoxXYWH(
                ann['bbox'][0],
                ann['bbox'][1],
                ann['bbox'][2],
                ann['bbox'][3]
            )
            det_obj = DetectionObjectBBox(
                bbox=bbox,
                label=cats[ann['category_id']]
            )
            det_objects.append(det_obj)
        image_dataset.add_item(
            file_info=file_info,
            annotation=ImageAnnotation(objects=det_objects)
        )

    return image_dataset
