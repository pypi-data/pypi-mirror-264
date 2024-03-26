from pathlib import Path
from typing import Optional, Union, List
from xml.etree import ElementTree

from datasets.annotations.objects import DetectionObjectPolygon
from datasets.annotations.polygon import Polygon
from datasets.annotations.video_annotation import VideoAnnotation
from datasets.importer.rawimages import raw_images
from datasets.meta import DatasetPart


def cvat_polygon_importer(
        images_folder: Path,
        annotations_file: Path,
        file_extensions: Union[str, List[str]] = 'jpg',
        dataset_name: Optional[str] = None,
        dataset_description: Optional[str] = None,
        dataset_part: Union[DatasetPart, str] = DatasetPart.TRAIN,
) -> VideoAnnotation:
    """Import images annotations from CVAT labelling
    Args:
        images_folder: location of files with images.
        annotations_file: annotations '.xml' file location.
        file_extensions: extension/extensions of image file. From folder will be read files with this extension.
        dataset_name: Dataset name will be used in meta information about dataset.
        dataset_description: Dataset description will be used in meta information about dataset.
        dataset_part: define the dataset part, can be 'train', 'test' or 'validation'.
    Returns:
        VideoAnnotation object with the frames
    """
    raw_ds = raw_images(
        input_folder=images_folder,
        file_extensions=file_extensions,
        dataset_name=dataset_name,
        dataset_description=dataset_description,
        dataset_part=dataset_part
    )
    try:
        root = ElementTree.parse(annotations_file).getroot()

        for tag_item in list(root):
            if tag_item.tag != 'image':
                continue
            file_name = Path(tag_item.attrib['name']).name
            objects = []
            for polygon_tag in list(tag_item):
                objects.append(
                    DetectionObjectPolygon(
                        polygon=Polygon(
                            points=list(
                                map(
                                    lambda x: (min(float(x.split(",")[0]), float(tag_item.attrib['width'])),
                                               min(float(x.split(",")[1]), float(tag_item.attrib['height']))
                                               ),
                                    polygon_tag.attrib["points"].split(";")
                                )
                            ),
                        ),
                        label=polygon_tag.attrib['label']
                    )
                )
            ds_item = raw_ds[file_name]
            ds_item.annotations.add_objects(objects)
    except (KeyError, ElementTree.ParseError, FileNotFoundError) as e:
        raise e

    return raw_ds
