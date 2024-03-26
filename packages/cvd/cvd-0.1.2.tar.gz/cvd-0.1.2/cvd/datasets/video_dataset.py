import shutil
from copy import deepcopy
from pathlib import Path
from typing import Optional, List, Dict, Union, Tuple, Iterable
from xml.etree import ElementTree
from xml.dom import minidom

import numpy as np

from cvd.datasets.annotations.coco import COCODataset, COCOLicense, COCOImage, COCOInfo
from cvd.datasets.annotations.video_annotation import VideoAnnotation, Frame
from cvd.datasets.filters import ObjectsFilter, IncludeLabelsFilter, ExcludeLabelsFilter
from cvd.datasets.image_dataset import string_to_number
from cvd.datasets.interfaces.idataset import IDataset

from cvd.datasets.meta import DatasetMeta, FileInfo, VideoFileInfo
from cvd.datasets.transformers import Transformer
from cvd.datasets.video_dataset_item import VideoDatasetItem
from cvd.datasets.annotations.type import MarkupType
from cvd.tools.hash import md5


class VideoDataset(IDataset):
    def __init__(self, dataset_meta: Optional[DatasetMeta] = None):
        super().__init__(dataset_meta)
        self._files: List[VideoFileInfo] = []
        self._files_index: Dict[str, VideoFileInfo] = {}

    def __getitem__(self, value) -> Union[VideoDatasetItem, 'VideoDataset']:
        if isinstance(value, int):
            file_info = self._files[value]
            return VideoDatasetItem(
                file_info=file_info,
                annotations=self._annotations[file_info.unique_id]
            )
        elif isinstance(value, str):
            file_info = self._files_index[value]
            return VideoDatasetItem(
                file_info=file_info,
                annotations=self._annotations[file_info.unique_id]
            )
        elif isinstance(value, slice):
            new_ds: VideoDataset = VideoDataset(
                dataset_meta=DatasetMeta(
                    name=deepcopy(self.dataset_meta.name),
                    version=self.dataset_meta.version,
                    description=self.dataset_meta.description,
                    part=deepcopy(self.dataset_meta.part),
                    dstype=deepcopy(self.dataset_meta.dstype)
                )
            )
            start, stop, step = value.indices(len(self._files))
            for i in range(start, stop, step):
                ds_item = self[i]
                new_ds.add_item(ds_item.file_info, ds_item.annotations)
            return new_ds
        elif isinstance(value, list):
            new_ds: VideoDataset = VideoDataset(
                dataset_meta=DatasetMeta(
                    name=deepcopy(self.dataset_meta.name),
                    version=self.dataset_meta.version,
                    description=self.dataset_meta.description,
                    part=deepcopy(self.dataset_meta.part),
                    dstype=deepcopy(self.dataset_meta.dstype)
                )
            )
            for i in value:
                ds_item = self[i]
                new_ds.add_item(ds_item.file_info, ds_item.annotations)
            return new_ds
        else:
            raise KeyError

    def __next__(self) -> VideoDatasetItem:
        if self._current >= len(self._files):
            raise StopIteration
        else:
            file_info = self._files[self._current]
            ann = self._annotations[file_info.unique_id]
            self._current += 1
            return VideoDatasetItem(
                file_info=file_info,
                annotations=ann
            )

    def add_item(self, file_info: VideoFileInfo, annotation: Optional[VideoAnnotation] = None):
        if annotation is None:
            annotation: VideoAnnotation = VideoAnnotation(frames=[])
        super().add_item(file_info, annotation)

    #TODO пока стоит проверка на дубликаты при инициализации
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
    ) -> Optional['VideoDataset']:
        filtered_video = []
        for item in self:
            filtered_frame = []
            for frame in item.annotations.frames:
                filtered_objects = []
                for obj in frame.objects:
                    if not object_filter.filter(obj):
                        filtered_objects.append(obj)
                filtered_frame.append(Frame(objects=filtered_objects, number=frame.number))
            filtered_video.append((item.file_info, VideoAnnotation(frames=filtered_frame)))

        if not keep_empty:
            filtered_video = filter(lambda x: any([bool(frame.objects) for frame in x[1].frames]), filtered_video)

        if inplace:
            self._files = []
            self._annotations = {}
            self._labels = []
            for f_v in list(filtered_video):
                fi, ann = f_v[0], f_v[1]
                self._files.append(fi)
                self._annotations[fi.unique_id] = ann
                if len(ann):
                    self._labels = sorted(list(set(self._labels) | set(ann.labels)))
            return None
        else:
            new_datasets = VideoDataset(dataset_meta=self._dataset_meta)
            for f_v in list(filtered_video):
                new_datasets.add_item(f_v[0], f_v[1])
            return new_datasets

    def filter_labels(
            self,
            include_labels: Optional[List[str]] = None,
            excluded_labels: Optional[List[str]] = None,
            keep_empty: bool = False,
            inplace: bool = False
    ) -> Optional['VideoDataset']:

        if include_labels:
            include_filter = IncludeLabelsFilter(include_labels=include_labels)
            new_ds = self.apply_filter(include_filter, keep_empty=keep_empty, inplace=inplace)

        if excluded_labels:
            exclude_filter = ExcludeLabelsFilter(exclude_labels=excluded_labels)
            if inplace:
                return self.apply_filter(exclude_filter, keep_empty=keep_empty, inplace=inplace)
            else:
                return new_ds.apply_filter(exclude_filter, keep_empty=keep_empty, inplace=inplace)
        return new_ds

    def rename_labels(self, rename_map: Dict[str, str], inplace: bool = False):
        _rename_map = dict(map(lambda x: (x, x), self.labels))
        _rename_map.update(rename_map)

        if inplace:
            self._labels = tuple(x for x in rename_map.values())
            for item in self:
                if item.annotations:
                    item.annotations.rename_labels(rename_map=rename_map)
        else:
            newdataset = VideoDataset(self.dataset_meta)
            for item in self:
                if item.annotations and item.file_info:
                    new_ann = deepcopy(item.annotations)
                    new_ann.rename_labels(rename_map=rename_map)
                    newdataset.add_item(item.file_info, new_ann)
            return newdataset

    @staticmethod
    def from_list(
            image_annotations_list: Union[
                Iterable[Tuple[VideoFileInfo, VideoAnnotation]],
                List[Tuple[VideoFileInfo, VideoAnnotation]]
            ]
    ) -> 'VideoDataset':
        new_dataset = VideoDataset()
        for file_info, ann in image_annotations_list:
            new_dataset.add_item(file_info, ann)
        return new_dataset

    def generate_video(self, output_folder: Path, show_conf: bool = False, draw_top: bool = False):
        for ds_item in self:
            ds_item.generate_video(
                output_folder=output_folder,
                output_file_name=ds_item.file_info.unique_id,
                show_conf=show_conf,
                draw_top=draw_top
            )

    def to_coco(self, overall: bool = True) -> Tuple[Union[COCODataset, List[COCODataset]], Dict[str, int]]:
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
            for obj in ann_img.objects:
                bboxxywh = obj.bbox_xywh()
                ann_list.append(
                    COCOAnnotation(
                        segmentation=[],
                        area=bboxxywh.width*bboxxywh.height,
                        iscrowd=False,
                        image_id=string_to_number(file_info.unique_id),
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
        for file_info, ann_img in self:
            for obj in ann_img.objects:
                bboxxywh = obj.bbox.toxywh()
                obj_list.append([
                    string_to_number(file_info.unique_id), # image_id
                    bboxxywh.x,
                    bboxxywh.y,
                    bboxxywh.width,
                    bboxxywh.height,
                    obj.confidence,  # score
                    label_to_index[obj.label]  # category_id
                ])

        return np.array(obj_list)

    def to_cvat(
            self,
            export_folder: Path,
            export_video: bool = True,
            track_id_attr_name: str = 'track_id',
            keyframe_period: int = 10,
    ):
        assert isinstance(keyframe_period, int) and keyframe_period >= 0,\
            "Keyframe_period must have integer type and value >= 0."
        export_folder.mkdir(exist_ok=True, parents=True)

        for i, v_ds_i in enumerate(self):
            assert v_ds_i.annotations.markup_type == MarkupType.BBOX.value, \
                'Conversion to cvat format for polygon objects type not working for now.'
            #TODO  Conversion for video dataset with polygon objects to cvat format
            df_ann = v_ds_i.annotations.to_df()
            assert 'x_center' not in df_ann.columns, 'Conversion for rotated bbox is not supported for now.'
            #TODO  Conversion for video dataset with rbbox objects to cvat format
            assert track_id_attr_name in df_ann.columns, \
                f"Can't found `track_id_attr_name`={track_id_attr_name} in columns names "

            if export_video:
                shutil.copy(v_ds_i.file_info.abs_path, export_folder/f'{Path(v_ds_i.file_info.unique_id).stem}.mp4')

            root = ElementTree.Element('annotations')
            for group_name, group in df_ann.groupby(track_id_attr_name):
                track = ElementTree.SubElement(root, 'track')

                assert group.label.nunique() == 1, f"Different labels are found in the track. {group.label.unique()}"
                track.set('id', str(group_name))
                track.set('label', group.label.iloc[0])
                for i, (_, row) in enumerate(group.iterrows()):
                    box = ElementTree.SubElement(track, 'box')
                    box.set('frame', str(row['frame_number']))
                    # set outside = 1 for the last frame of the track
                    box.set('xtl', str(row['xmin']))
                    box.set('ytl', str(row['ymin']))
                    box.set('xbr', str(row['xmax']))
                    box.set('ybr', str(row['ymax']))
                    box.set('occluded', '0')
                    box.set('keyframe', '0' if i % keyframe_period and i + 1 < len(group) else '1')
                    box.set('outside', '0' if i + 1 < len(group) else '1')

                    for key, values in row.drop(['frame_number', 'xmin', 'ymin', 'xmax', 'ymax','label',track_id_attr_name]).to_dict().items():
                        box.set(key, str(values))

            rough_string = ElementTree.tostring(root, 'utf-8')
            xml_tree_minidom = minidom.parseString(rough_string).toprettyxml(indent="\t")

            with open(export_folder/f"{Path(v_ds_i.file_info.unique_id).stem}.xml", 'w') as out_file:
                out_file.write(xml_tree_minidom)

    def transformation(
            self,
            transformer: Transformer,
            inplace: bool = False
    ):
        transformed_items = []
        for ds_item in self:
            transformed_frames = []
            for frame in ds_item.annotations.frames:
                transformed_objects = []
                for obj in frame.objects:
                    transformed_objects.append(transformer.transform(obj=obj, file_info=ds_item.file_info))
                transformed_frames.append(Frame(objects=transformed_objects, number=frame.number))
            transformed_items.append((ds_item.file_info, VideoAnnotation(frames=transformed_frames)))

        if inplace:
            self._files = []
            self._annotations = {}
            for file_info, ann in transformed_items:
                self._files.append(file_info)
                self._annotations[file_info.unique_id] = ann
        else:
            new_datasets = VideoDataset(dataset_meta=self._dataset_meta)
            for file_info, ann in transformed_items:
                new_datasets.add_item(file_info, ann)
            return new_datasets
