from pathlib import Path
from typing import Dict, Optional, Union
from xml.etree import ElementTree

from cvd.datasets.annotations.objects import BBoxXYXY, TrackGTObjectPolygon
from cvd.datasets.annotations.objects import TrackGTObjectBBox
from cvd.datasets.annotations.polygon import Polygon
from cvd.datasets.annotations.video_annotation import VideoAnnotation, Frame
from cvd.datasets.importer.rawvideo import raw_videos
from cvd.datasets.meta import DatasetPart, DatasetMeta, DatasetType
from cvd.datasets.video_dataset import VideoDataset


def import_video_bbox(
        cvat_xml_path,
        frame_width: Optional[int] = None,
        frame_height: Optional[int] = None
) -> VideoAnnotation:
    """Import video annotations from CVAT labelling"""

    frames_dict: Dict[int, Frame] = {}
    root = ElementTree.parse(cvat_xml_path).getroot()
    for track in list(root):
        if track.tag != 'track':
            continue
        track_id = int(track.attrib['id'])
        for box in list(track):
            if ('outside' in box.attrib and box.attrib['outside'] == '1') or \
                    ('occluded' in box.attrib and box.attrib['occluded']) == '1':
                continue
            attributes = dict([(item.attrib["name"], item.text) for item in box])
            xmin = max(0.0, float(box.attrib['xtl']))
            ymin = max(0.0, float(box.attrib['ytl']))
            xmax = float(box.attrib['xbr'])
            if frame_width:
                xmax = min(float(frame_width), xmax)
            ymax = float(box.attrib['ybr'])
            if frame_height:
                ymax = min(float(frame_height), ymax)
            gt_object = TrackGTObjectBBox(
                    bbox=BBoxXYXY(
                        xmin=xmin,
                        ymin=ymin,
                        xmax=xmax,
                        ymax=ymax
                    ),
                    track_id=track_id,
                    label=track.attrib['label'],
                    attributes=attributes
                )
            frame_number = int(box.attrib["frame"])
            if frame_number in frames_dict:
                frames_dict[frame_number].add_objects([gt_object])
            else:
                frames_dict[frame_number] = Frame(
                    objects=[gt_object],
                    number=frame_number
                )

    frames = sorted(list(frames_dict.values()), key=lambda x: x.number)
    vd_ann = VideoAnnotation(
        frames=frames
    )
    return vd_ann


def import_video_cvat_polygon(
        video_direcory_path: Path,
        file_extensions: str = "mp4",
        dataset_name: Optional[str] = None,
        dataset_description: Optional[str] = None,
        dataset_part: Union[DatasetPart, str] = DatasetPart.TRAIN,
) -> VideoDataset:
    """Import video annotations from CVAT labelling"""

    raw_ds = raw_videos(
        input_folder=video_direcory_path,
        file_extensions=file_extensions
    )
    res_ds = VideoDataset(
        dataset_meta=DatasetMeta(
            name=dataset_name if dataset_name is not None else '',
            version='1.0.0',
            description=dataset_description if dataset_description is not None else '',
            part=dataset_part,
            dstype=DatasetType.VIDEO
        )
    )
    for ds_item in raw_ds:
        frames_dict: Dict[int, Frame] = {}
        cvat_xml_path = video_direcory_path / f"{ds_item.file_info.abs_path.stem}.xml"
        root = ElementTree.parse(cvat_xml_path).getroot()
        for track in list(root):
            if track.tag != 'track':
                continue
            track_id = int(track.attrib['id'])
            for box in list(track):
                if ('outside' in box.attrib and box.attrib['outside'] == '1') or \
                        ('occluded' in box.attrib and box.attrib['occluded']) == '1':
                    continue
                attributes = dict([(item.attrib["name"], item.text) for item in box])
                gt_object = TrackGTObjectPolygon(
                    polygon=Polygon(
                        points=list(
                            map(
                                lambda x: (float(x.split(",")[0]), float(x.split(",")[1])),
                                box.attrib["points"].split(";")
                            )
                        ),
                    ),
                    track_id=track_id,
                    label=track.attrib['label'],
                    attributes=attributes
                )

                frame_number = int(box.attrib["frame"])
                if frame_number in frames_dict:
                    frames_dict[frame_number].add_objects([gt_object])
                else:
                    frames_dict[frame_number] = Frame(
                        objects=[gt_object],
                        number=frame_number
                    )

        frames = sorted(list(frames_dict.values()), key=lambda x: x.number)
        vd_ann = VideoAnnotation(
            frames=frames
        )
        res_ds.add_item(ds_item.file_info, vd_ann)
    return res_ds
