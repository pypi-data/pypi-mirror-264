import hashlib
import os.path
import random
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Optional, List, Dict, Union, Tuple, Iterable, Callable
from xml.etree import ElementTree
from xml.dom import minidom

from IPython.core.display import display
from matplotlib import pyplot as plt

from cvd.datasets.annotations.objects import DetectionObjectBBox, DetectionObjectPolygon, RBBoxXYCenterWHA
from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.coco import COCODataset, COCOInfo, COCOLicense, COCOImage, COCOAnnotation, COCOCategory
import numpy as np

from cvd.datasets.filters import ObjectsFilter
from cvd.datasets.image_dataset_item import ImageDatasetItem
from cvd.datasets.transformers import Transformer
from cvd.datasets.interfaces.idataset import IDataset
from cvd.datasets.meta import DatasetMeta, FileInfo, ImageFileInfo
from cvd.tools.hash import md5


def string_to_number(s: str):
    md5hash = hashlib.md5(s.encode('utf-8'))
    return int(md5hash.hexdigest(), 16)


class ImagesDataset(IDataset):
    """Dataset contained images list with fileinfo and annotation for this images
        Args:
            dataset_meta - dataset description
    """
    def __init__(self, dataset_meta: Optional[DatasetMeta] = None):
        """
        Initialize the ImagesDataset with the given dataset_meta.

        Parameters:
            dataset_meta (DatasetMeta, optional): Meta information about the dataset. Default is None.
        """
        super().__init__(dataset_meta)
        self._files: List[ImageFileInfo] = []
        self._files_index: Dict[str, ImageFileInfo] = {}

    def __getitem__(self, value) -> Union[ImageDatasetItem, 'ImagesDataset']:
        """
            Get the ImageDatasetItem at the given index or for the given file name.
            If a slice is provided, returns a new ImagesDataset with the items in the slice.
            If a list is provided, returns a new ImagesDataset with the items in the list.

            Parameters:
                value (int, str, slice, list): The value to index the dataset with.

            Returns:
                ImageDatasetItem or ImagesDataset: The ImageDatasetItem at the given index or for the given file name.
                If a slice or list is provided, returns a new ImagesDataset with the items in the slice or list.
            """
        try:
            if isinstance(value, (int, np.integer)):
                file_info = self._files[value]
                return ImageDatasetItem(
                    file_info=file_info,
                    annotations=self._annotations[file_info.unique_id]
                )
            elif isinstance(value, str):
                file_info = self._files_index[value]
                return ImageDatasetItem(
                    file_info=file_info,
                    annotations=self._annotations[file_info.unique_id]
                )
            elif isinstance(value, slice):
                new_ds: ImagesDataset = ImagesDataset(
                    dataset_meta=DatasetMeta(
                        name=deepcopy(self.dataset_meta.name),
                        version=self.dataset_meta.version,
                        description=deepcopy(self.dataset_meta.description),
                        part=deepcopy(self.dataset_meta.part),
                        dstype=deepcopy(self.dataset_meta.dstype)
                    ) if self.dataset_meta is not None else None
                )
                start, stop, step = value.indices(len(self._files))
                for i in range(start, stop, step):
                    ds_item = self[i]
                    new_ds.add_item(deepcopy(ds_item.file_info), deepcopy(ds_item.annotations))
                return new_ds
                # return [self[i] for i in range(start, stop, step)]
            elif isinstance(value, list):
                new_ds: ImagesDataset = ImagesDataset(
                    dataset_meta=DatasetMeta(
                        name=deepcopy(self.dataset_meta.name),
                        version=self.dataset_meta.version,
                        description=deepcopy(self.dataset_meta.description),
                        part=deepcopy(self.dataset_meta.part),
                        dstype=deepcopy(self.dataset_meta.dstype)
                    ) if self.dataset_meta is not None else None
                )
                for num in value:
                    ds_item = self[num]
                    new_ds.add_item(deepcopy(ds_item.file_info), deepcopy(ds_item.annotations))
                return new_ds
        except (KeyError, IndexError) as e:
            print(type(value))
            raise e

    def __next__(self) -> 'ImageDatasetItem':
        """
        Returns the next ImageDatasetItem in the dataset.
        Raises StopIteration when the end of the dataset is reached.
        """
        if self._current >= len(self._files):
            raise StopIteration
        else:
            file_info = self._files[self._current]
            ann = self._annotations[file_info.unique_id]
            self._current += 1
            return ImageDatasetItem(
                file_info=file_info,
                annotations=ann
            )

    def add_item(self, file_info: ImageFileInfo, annotation: Optional[ImageAnnotation] = None):
        """
        Add a new ImageDatasetItem to the dataset.

        Parameters:
            file_info (ImageFileInfo): Information about the file, including its unique id and file path.
            annotation (ImageAnnotation, optional): Annotation for the file. Default is None.
        """
        if annotation is None:
            annotation: ImageAnnotation = ImageAnnotation(objects=[])
        super().add_item(file_info, annotation)

    def add_ds_item(self, ds_item: ImageDatasetItem):
        super().add_item(deepcopy(ds_item.file_info), deepcopy(ds_item.annotations))

    def add_ds_items(self, ds_items: Iterable[ImageDatasetItem]):
        for ds_item in ds_items:
            super().add_item(deepcopy(ds_item.file_info), deepcopy(ds_item.annotations))

    def remove_item(self, unique_id: str):
        ifi = self._files_index[unique_id]
        self._files.remove(ifi)
        self._annotations.pop(ifi.unique_id)
        self._files_index.pop(ifi.unique_id)

    def remove_duplicate(self):
        _files_md5: Dict[str, FileInfo] = {}
        for ifi in self._files:
            file_md5 = md5(ifi.abs_path)
            if file_md5 in _files_md5:
                self._logger.info(f"The '{_files_md5[file_md5].unique_id}' file is identical "
                                  f"is identical to file '{ifi.unique_id}'.")
                self._files.remove(ifi)
                self._annotations.pop(ifi.unique_id)
                self._files_index.pop(ifi.unique_id)
            else:
                _files_md5[file_md5] = ifi

    def apply_filter(
            self,
            object_filter: ObjectsFilter,
            keep_empty: bool = False,
            inplace: bool = False
    ) -> Optional['ImagesDataset']:
        filtered_images = []
        for ds_item in self:
            filtered_objects = []
            for obj in ds_item.annotations.objects:
                if not object_filter.filter(obj):
                    filtered_objects.append(obj)
            filtered_images.append((ds_item.file_info, ImageAnnotation(objects=filtered_objects)))

        if not keep_empty:
            filtered_images = filter(lambda x: bool(x[1].objects), filtered_images)

        if inplace:
            self._files = []
            self._annotations = {}
            for file_info, ann in filtered_images:
                self._files.append(file_info)
                self._annotations[file_info.unique_id] = ann
        else:
            new_datasets = ImagesDataset(dataset_meta=self._dataset_meta)
            for file_info, ann in filtered_images:
                new_datasets.add_item(file_info, ann)
            return new_datasets

    def filter(
            self,
            include_labels: Optional[List[str]] = None,
            excluded_labels: Optional[List[str]] = None,
            keep_empty: bool = False,
            inplace: bool = False
    ) -> Optional['ImagesDataset']:

        if include_labels:
            in_labels = set(include_labels)
            in_filtered_images: List[ImageDatasetItem] = []
            for ds_item in self:
                filtered_objects = tuple(filter(lambda x: x.label in in_labels, ds_item.annotations.objects))
                in_filtered_images.append(
                    ImageDatasetItem(
                        file_info=ds_item.file_info,
                        annotations=ImageAnnotation(objects=filtered_objects)
                    )
                )
        else:
            in_filtered_images: List[ImageDatasetItem] = list(self)
        if excluded_labels:
            ex_labels = set(excluded_labels)
            ex_filtered_images: List[ImageDatasetItem] = []
            for ds_item in in_filtered_images:
                filtered_objects = tuple(filter(lambda x: x.label not in ex_labels, ds_item.annotations.objects))
                ex_filtered_images.append(
                    ImageDatasetItem(
                        file_info=ds_item.file_info,
                        annotations=ImageAnnotation(objects=filtered_objects)
                    )
                )
            filtered_images: List[ImageDatasetItem] = ex_filtered_images
        else:
            filtered_images: List[ImageDatasetItem] = in_filtered_images

        if not keep_empty:
            filtered_images = list(filter(lambda x: bool(x.annotations.objects), filtered_images))

        if inplace:
            self._files = []
            self._annotations = {}
            for file_info, ann in filtered_images:
                self._files.append(file_info)
                self._annotations[file_info.unique_id] = ann
        else:
            new_datasets = ImagesDataset(dataset_meta=self._dataset_meta)
            for ds_item in filtered_images:
                new_datasets.add_item(ds_item.file_info, ds_item.annotations)
            return new_datasets

    def rename_labels(self, rename_map: Dict[str, str], inplace: bool = False):
        _rename_map = dict(map(lambda x: (x, x), self.labels))
        _rename_map.update(rename_map)

        def _rename(_img_ann: ImageAnnotation):
            return ImageAnnotation(
                objects=list(map(
                    lambda x: DetectionObjectBBox(
                        bbox=x.bbox,
                        label=_rename_map[x.label],
                        attributes=x.attributes
                    ),
                    _img_ann.objects
                )),
            )

        if inplace:
            labels = []
            for id, ann in self._annotations.items():
                self._annotations[id] = _rename(ann)
                labels += self._annotations[id].labels
            self._labels = sorted(list(set(labels)))
        else:
            newdataset = ImagesDataset(self.dataset_meta)
            for ds_item in self:
                new_ann = _rename(ds_item.annotations)
                newdataset.add_item(ds_item.file_info, new_ann)
            return newdataset

    @staticmethod
    def from_list(
            image_annotations_list: Union[
                Iterable[Tuple[FileInfo, ImageAnnotation]],
                List[Tuple[FileInfo, ImageAnnotation]]
            ]
    ) -> 'ImagesDataset':
        new_dataset = ImagesDataset()
        for file_info, ann in image_annotations_list:
            new_dataset.add_item(file_info, ann)
        return new_dataset

    def to_coco(self) -> Tuple[COCODataset, Dict[str, int]]:
        info = COCOInfo(
            description=self.dataset_meta.description if self.dataset_meta else '',
            url='',
            version=self.dataset_meta.version if self.dataset_meta else '',
            year=0,
            contributor='',
            date_created=''
        )
        coco_license = COCOLicense(
            url='',
            id=0,
            name='fake'
        )
        ann_list = []
        img_list = []
        categories = []
        obj_id = 0
        label_to_index = dict([(label, index) for index, label in enumerate(self.labels)])
        for ds_item in self:
            img_list.append(
                COCOImage(
                    license=0,
                    file_name=ds_item.file_info.abs_path.name,
                    coco_url='',
                    height=ds_item.file_info.height,
                    width=ds_item.file_info.width,
                    date_captured='',
                    flickr_url='',
                    id=string_to_number(ds_item.file_info.unique_id)
                )
            )
            for obj in ds_item.annotations.objects:
                bboxxywh = obj.bbox_xywh()
                ann_list.append(
                    COCOAnnotation(
                        segmentation=[],
                        area=bboxxywh.width*bboxxywh.height,
                        iscrowd=False,
                        image_id=string_to_number(ds_item.file_info.unique_id),
                        bbox=[float(bboxxywh.x), float(bboxxywh.y), float(bboxxywh.width), float(bboxxywh.height)],
                        category_id=label_to_index[obj.label],
                        id=obj_id
                    )
                )
                obj_id += 1

            categories = [
                COCOCategory(supercategory='fake', id=label_to_index[label], name=label) for label in self.labels
            ]

        return COCODataset(
            info=info,
            licenses=[coco_license],
            images=img_list,
            annotations=ann_list,
            categories=categories
        ), label_to_index

    def to_coco_pred(self, label_to_index: Dict[str, int]) -> np.ndarray:
        obj_list = []
        for ds_item in self:
            for obj in ds_item.annotations.objects:
                bboxxywh = obj.bbox.toxywh()
                obj_list.append([
                    string_to_number(ds_item.file_info.unique_id),  # image_id
                    bboxxywh.x,
                    bboxxywh.y,
                    bboxxywh.width,
                    bboxxywh.height,
                    obj.confidence,  # score
                    label_to_index[obj.label]  # category_id
                ])

        return np.array(obj_list)

    def to_cvat(self, export_folder: Path, prepare_image: bool = True):
        xml_tree = ElementTree.Element('annotations')

        export_folder.mkdir(exist_ok=True)
        image_folder = None
        if prepare_image:
            image_folder = export_folder / "images"
            image_folder.mkdir(exist_ok=True)

        for i, (ds_item) in enumerate(self):
            if prepare_image:
                f_dest_path = image_folder/f'{Path(ds_item.file_info.unique_id).stem}.jpg'
                if os.path.exists(f_dest_path):
                    os.remove(f_dest_path)
                shutil.copy(ds_item.file_info.abs_path, f_dest_path)
            image = ElementTree.SubElement(xml_tree, 'image')

            image.set('id', str(i))
            image.set('name', str(ds_item.file_info.abs_path))
            image.set('width', str(ds_item.file_info.width))
            image.set('height', str(ds_item.file_info.height))
            for obj in ds_item.annotations.objects:
                if isinstance(obj, DetectionObjectPolygon):
                    polygon = ElementTree.SubElement(image, 'polygon')
                    polygon.set('label', str(obj.label))
                    polygon.set('occluded', '0')
                    polygon.set('source', 'REFERENCE')
                    points_str = []
                    for item in obj.polygon._points:
                        points_str.append(f'{item[0]},{item[1]}')
                    polygon.set('points', ';'.join(points_str))
                else:
                    if isinstance(obj.bbox, RBBoxXYCenterWHA) is True:
                        raise Exception(f"Conversion for rotated bbox objects to cvat format not working for now. Check obj = {str(obj.bbox)}")
                    box = ElementTree.SubElement(image, 'box')
                    box.set('label', str(obj.label))
                    box.set('occluded', '0')
                    box.set('source', 'REFERENCE')
                    box.set('xtl', str(obj.bbox.xmin))
                    box.set('ytl', str(obj.bbox.ymin))
                    box.set('xbr', str(obj.bbox.xmax))
                    box.set('ybr', str(obj.bbox.ymax))

        rough_string = ElementTree.tostring(xml_tree, 'utf-8')
        xml_tree_minidom = minidom.parseString(rough_string).toprettyxml(indent="\t")

        with open(export_folder/"annotations.xml", 'w') as out_file:
            out_file.write(xml_tree_minidom)

    def show_examples(
            self,
            number: int = 16,
            columns: int = 4,
            rows: int = 4,
            figure_size: Tuple[int, int] = (10, 5),
            show_annotations: bool = True
    ):
        _tmp_dt = self[random.sample(list(range(len(self))), number)]
        for i in range(rows):
            fig, axs = plt.subplots(1, columns, figsize=(figure_size[0], figure_size[1]*columns))
            for j in range(columns):
                inter_num = i * columns + j
                if inter_num < len(_tmp_dt):
                    if show_annotations:
                        img = _tmp_dt[inter_num].draw_annotations()
                    else:
                        img = _tmp_dt[inter_num].load_image()
                    if columns == 1:
                        axs.imshow(img)
                        axs.set_title(f"{_tmp_dt[inter_num].file_info.unique_id}")
                    else:
                        axs[j].imshow(img)
                        axs[j].set_title(f"{_tmp_dt[inter_num].file_info.unique_id}")
            display(fig)
            plt.clf()
            plt.close(fig)

    def transformation(
            self,
            transformer: Transformer,
            inplace: bool = False
    ):
        transformed_items = []
        for ds_item in self:
            transformed_objects = []
            for obj in ds_item.annotations.objects:
                res = transformer.transform(obj=obj, file_info=ds_item.file_info)
                if res is not None:
                    transformed_objects.append(res)
            transformed_items.append((ds_item.file_info, ImageAnnotation(objects=transformed_objects)))

        if inplace:
            self._files = []
            self._annotations = {}
            for file_info, ann in transformed_items:
                self._files.append(file_info)
                self._annotations[file_info.unique_id] = ann
        else:
            new_datasets = ImagesDataset(dataset_meta=self._dataset_meta)
            for file_info, ann in transformed_items:
                new_datasets.add_item(file_info, ann)
            return new_datasets

    def sampling(
            self,
            sampler_fn: Callable[[ImageDatasetItem], bool],
            sort: bool = False,
            sort_fn: Optional[Callable[[ImageDatasetItem], bool]] = None
    ) -> 'ImagesDataset':
        new_sample_ds = ImagesDataset(dataset_meta=self._dataset_meta)
        new_sample_ds.dataset_meta.name = None
        new_sample_ds.dataset_meta.version = None
        new_sample_ds.dataset_meta.description = None
        ds_items_list = list(self)
        if sort:
            ds_items_list = sorted(ds_items_list, key=sort_fn)

        new_sample_ds.add_ds_items(filter(sampler_fn, ds_items_list))
        return new_sample_ds






def update_annotations(
        initial_dataset: ImagesDataset,
        remark_dataset: ImagesDataset,
        meta_name: str = None,
        meta_description: str = None,
        meta_version: str = None
):
    dict_annotations = get_annotations_from_dataset(remark_dataset)

    final_dataset = ImagesDataset(dataset_meta=initial_dataset.dataset_meta)
    final_dataset.dataset_meta.name = meta_name                     #'Toloka_fixed'
    final_dataset.dataset_meta.description = meta_description       #'Dataset from Toloka. Bug fixed'
    final_dataset.dataset_meta.version = meta_version               #'1.1.0'

    for item in initial_dataset:
        if item.file_info.unique_id in dict_annotations.keys():
            final_dataset.add_item(file_info=item.file_info, annotation=dict_annotations.pop(item.file_info.unique_id))
        else:
            final_dataset.add_item(file_info=item.file_info, annotation=item.annotations)
    return final_dataset


def get_annotations_from_dataset(in_dataset: ImagesDataset):
    annotations_dict = dict()
    for item in in_dataset:
        annotations_dict[item.file_info.unique_id] = item.annotations

    return annotations_dict

