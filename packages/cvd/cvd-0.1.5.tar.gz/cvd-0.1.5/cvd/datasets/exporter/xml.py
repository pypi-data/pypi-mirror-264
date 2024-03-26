from copy import deepcopy
from distutils.util import strtobool
from pathlib import Path
from typing import List, Any, Union
from xml.etree.ElementTree import Element

from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.objects import DetectionObjectBBox, TrackGTObjectBBox, TrackGTObjectPolygon, \
    DetectionObjectPolygon
from cvd.datasets.annotations.polygon import Polygon
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.annotations.sbbox import BBoxXYXY
from cvd.datasets.annotations.video_annotation import VideoAnnotation, Frame
from cvd.datasets.image_dataset import ImagesDataset
from bs4 import BeautifulSoup

from cvd.datasets.interfaces import Serializable, CustomSerializer
from cvd.datasets.meta import FileInfo, DatasetMeta, ImageFileInfo, VideoFileInfo
from xml.etree import ElementTree

from cvd.datasets.video_dataset import VideoDataset
from cvd.datasets.zoo.internal_representation import _InternalDatasetsMeta, _InternalDataset, _InternalFileMeta, \
    _InternalDatasetMeta, _InternalFilesMeta

SUPPORTED_CLASS_DICT = {
    'image_dataset': ImagesDataset,
    'video_dataset': VideoDataset,
    'file_info': FileInfo,
    'image_file_info': ImageFileInfo,
    'video_file_info': VideoFileInfo,
    'image_annotation': ImageAnnotation,
    'video_annotation': VideoAnnotation,
    'detection_object_bbox': DetectionObjectBBox,
    'detection_object_polygon':DetectionObjectPolygon,
    'track_object_polygon': TrackGTObjectPolygon,
    'track_object': TrackGTObjectBBox,
    'bboxxyxy': BBoxXYXY,
    'rbboxxycenterwh': RBBoxXYCenterWHA,
    'polygon': Polygon,
    'datasetmeta': DatasetMeta,
    'internal_datasets_meta': _InternalDatasetsMeta,
    'internal_dataset_meta': _InternalDatasetMeta,
    'internal_dataset': _InternalDataset,
    'internal_files_meta': _InternalFilesMeta,
    'internal_file_meta': _InternalFileMeta,
    'frame': Frame

}

supported_class = tuple(SUPPORTED_CLASS_DICT.values())
classname_to_atrname = {v.__name__: k for k, v in SUPPORTED_CLASS_DICT.items()}


def str_to_type(str_type):
    if str_type == 'str':
        return str
    elif str_type == 'int':
        return int
    elif str_type == 'float':
        return float
    elif str_type == 'bool':
        return strtobool
    else:
        raise Exception(f"Type `{str_type}` doesn't supported")


def convert_value(item: Element):
    if item.attrib['type'] == 'str':
        return str(item.attrib['value'])
    elif item.attrib['type'] == 'int':
        return int(item.attrib['value'])
    elif item.attrib['type'] == 'float':
        return float(item.attrib['value'])
    elif item.attrib['type'] == 'bool':
        return strtobool(item.attrib['value'])
    elif item.attrib['type'] == 'None':
        return None
    else:
        raise Exception(f"Type `{item.attrib['type']}` doesn't supported")


def check_homogeneous_type(value: List[Any]) -> bool:
    base_type = type(value[0])
    return not any(not isinstance(y, base_type) for y in value)


def _import_from_xml(tag: Element) -> object:
    tag_name = tag.tag
    if tag_name in SUPPORTED_CLASS_DICT:
        ref_class = SUPPORTED_CLASS_DICT[tag_name]
        instance_ref_class: Serializable = ref_class.__new__(ref_class)
        if isinstance(instance_ref_class, CustomSerializer):
            return instance_ref_class.from_xml(tag)
        else:
            state_dict = {}
            for item in tag:
                item_tag = item.tag
                if item_tag == 'attribute':
                    if len(item) == 1:
                        state_dict[item.attrib["name"]] = _import_from_xml(item[0])
                    else:
                        state_dict[item.attrib["name"]] = convert_value(item)
                else:
                    raise Exception("Incorrect state of class in xml")
            instance_ref_class.__setstate__(state_dict)
        return instance_ref_class

    elif tag_name in ['list', 'tuple']:
        if 'type' in tag.attrib:
            item_class = str_to_type(tag.attrib['type'])
            tmp_map = map(lambda x: item_class(x.attrib['value']), tag)
            if tag.attrib['type'] == 'list':
                return list(tmp_map)
            return tuple(tmp_map)
        else:
            tmp_list = []
            for item in tag:
                tmp_list.append(_import_from_xml(item))
            if tag_name == 'tuple':
                return tuple(tmp_list)
            return tmp_list
    elif tag_name == 'dict':
        tmp_dict = {}
        for item in tag:
            if 'type' in item.attrib:
                type_func = str_to_type(item.attrib["type"])
                tmp_dict[item.attrib['key']] = type_func(item.attrib["value"])
            else:
                tmp_dict[item.attrib['key']] = _import_from_xml(item[0])
        return tmp_dict
    else:
        raise Exception(f"Tag `{tag_name}` is unsupported for deserialize")


def import_from_xml(file_path) -> object:
    root = ElementTree.parse(file_path).getroot()
    return _import_from_xml(root)


def exporter_to_xml(obj: object, output_file: Path):
    soup = BeautifulSoup(features='xml')
    new_tag = _exporter_to_xml(obj, soup)
    soup.append(new_tag)
    f = open(output_file, "w")
    f.write(soup.prettify())
    f.close()


def _exporter_to_xml(obj: object, soup, level=0):
    if isinstance(obj, Serializable) and obj.__class__.__name__ in classname_to_atrname:
        new_tag = soup.new_tag(classname_to_atrname[obj.__class__.__name__])
        if isinstance(obj, CustomSerializer):
            new_tag = obj.to_xml(new_tag)
        else:
            for key, value in obj.__getstate__().items():
                _attribute_tag = soup.new_tag('attribute')
                _attribute_tag.attrs['name'] = key
                if isinstance(value, (Serializable, list, tuple)):
                    _attribute_tag.append(_exporter_to_xml(value, soup, level=level+1))
                elif isinstance(value, dict):
                    dict_tag = soup.new_tag('dict')
                    for k, v in value.items():
                        _new_sub_tag = soup.new_tag('item')
                        _new_sub_tag.attrs["key"] = k
                        if isinstance(v, (int, float, str, bool)):
                            _new_sub_tag.attrs['type'] = v.__class__.__name__
                            _new_sub_tag.attrs['value'] = v
                        elif isinstance(v, Serializable):
                            _new_sub_tag.append(_exporter_to_xml(v, soup, level=level + 1))
                        else:
                            raise Exception(f"Type  `{type(v)} is unsupported")
                        dict_tag.append(_new_sub_tag)
                    _attribute_tag.append(dict_tag)
                elif isinstance(value, (int, float, bool, str)):
                    _attribute_tag.attrs['type'] = value.__class__.__name__
                    _attribute_tag.attrs['value'] = value
                elif value is None:
                    _attribute_tag.attrs['type'] = "None"
                    _attribute_tag.attrs['value'] = "None"
                else:
                    raise Exception(f"Type  `{type(value)} is unsupported")
                new_tag.append(_attribute_tag)
        return new_tag
    elif isinstance(obj, (list, tuple)):
        new_tag = soup.new_tag(obj.__class__.__name__)
        if len(obj):
            if check_homogeneous_type(obj) and isinstance(obj[0], (int, float, str, bool)):
                new_tag.attrs['type'] = obj[0].__class__.__name__
                for item in obj:
                    _new_sub_tag = soup.new_tag('item')
                    _new_sub_tag.attrs['value'] = str(item)
                    new_tag.append(_new_sub_tag)
            else:
                for item in obj:
                    new_tag.append(_exporter_to_xml(item, soup, level=level + 1))
        return new_tag
    else:
        raise Exception(f"Type  `{type(obj)} is unsupported")
