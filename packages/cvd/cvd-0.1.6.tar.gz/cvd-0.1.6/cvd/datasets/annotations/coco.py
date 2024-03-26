from typing import Dict, List

from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class COCOInfo:
    description: str
    url: str
    version: str
    year: int
    contributor: str
    date_created: str # format YYYY/MM/DD

@dataclass_json
@dataclass
class COCOLicense:
    url: str
    id: int
    name: str

@dataclass_json
@dataclass
class COCOImage:
    license: int
    file_name: str
    coco_url: str
    height: int
    width: int
    date_captured: str #format YYYY-MM-DD HH:MM:SS
    flickr_url: str
    id: int

@dataclass_json
@dataclass
class COCOAnnotation:
    segmentation: List[List[float]]
    area: float
    iscrowd: bool
    image_id: int
    bbox: List[float]
    category_id: int
    id: int

@dataclass_json
@dataclass
class COCOCategory:
    supercategory: str
    id: int
    name: str


@dataclass_json
@dataclass
class COCODataset:
    info: COCOInfo
    licenses: List[COCOLicense]
    images: List[COCOImage]
    annotations: List[COCOAnnotation]
    categories: List[COCOCategory]


