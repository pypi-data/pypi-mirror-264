import json
from copy import deepcopy
from pathlib import Path
from typing import List, Optional, Union

from toloka.client import TolokaClient
from toloka.client.assignment import Assignment
from toloka.client.search_requests import AssignmentSearchRequest

from cvd.datasets.annotations.objects import DetectionObjectPolygon
from cvd.datasets.annotations.polygon import Polygon
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.importer.rawimages import raw_images
from cvd.datasets.meta import DatasetPart

import pandas as pd

from datasets.annotations.image_annotation import ImageAnnotation
from datasets.interfaces.idataset import DuplicationError


def loads_toloka_json(input_str: str):
    try:
        input_str = input_str.replace("\\", '')
        input_str = '[' + input_str + ']'
        return json.loads(input_str)
    except (json.JSONDecodeError, AttributeError) as e:
        raise e


def toloka_polygon2cvd_polygon(toloka_points, image_width, image_height):
    polygon_points = []
    for point in toloka_points:
        x = float(point["left"] * image_width)
        y = float(point["top"] * image_height)
        polygon_points.append((x, y))
    return Polygon(polygon_points)


def toloka_importer_api(
        ds: ImagesDataset,
        toloka_client: TolokaClient,
        pool_id: str,
        only_annotated: bool = False,
        default_label: str = "None"
) -> ImagesDataset:

    assig_req = AssignmentSearchRequest(pool_id=pool_id)
    answers = list(toloka_client.get_assignments(assig_req))
    acc_ans = filter_accepted(answers)
    if only_annotated:
        new_ds = ImagesDataset(dataset_meta=ds.dataset_meta)

    for i, ans in enumerate(acc_ans):
        ans_id = str(Path(ans.tasks[0].input_values['image']).name)

        try:
            ds_item = ds[ans_id]
            det_objects = []
            if "path" in ans.solutions[0].output_values:
                for tol_obj in ans.solutions[0].output_values["path"]:
                    if tol_obj['shape'] == 'polygon':
                        cvd_poly = toloka_polygon2cvd_polygon(
                            toloka_points=tol_obj["points"],
                            image_width=ds_item.file_info.width,
                            image_height=ds_item.file_info.height
                        )
                        det_obj_poly = DetectionObjectPolygon(polygon=cvd_poly, label=tol_obj.get('label', default_label))
                        det_objects.append(det_obj_poly)
                    else:
                        raise Exception(f"Toloka '{tol_obj['shape']}' object isn't supported.")
            try:
                if only_annotated:
                    new_ds.add_item(file_info=ds_item.file_info, annotation=ImageAnnotation(objects=det_objects))
                else:
                    ds_item.annotations.add_objects(det_objects)
            except DuplicationError:
                print(f"The annotation for the key '{ans_id}' is exist")

        except KeyError:
            print(f"The item with the key '{ans_id}' is not found in the dataset")

    if only_annotated:
        return new_ds
    return ds

def filter_accepted(user_answers):
    accepted_ans = []
    for ans in user_answers:
        if ans.submitted and not ans.rejected and ans.status == Assignment.Status.ACCEPTED:
            accepted_ans.append(ans)
    return accepted_ans

def toloka_polygon_importer(
        images_folder: Path,
        annotations_file: Path,
        file_extensions: Union[str, List[str]] = 'jpg',
        dataset_name: Optional[str] = None,
        dataset_description: Optional[str] = None,
        dataset_part: Union[DatasetPart, str] = DatasetPart.TRAIN,
        input_column_name: str = 'INPUT:image',
        result_column_name: str = 'OUTPUT:path',
        toloka_client: Optional[TolokaClient] = None
):
    """
        Import polygon points from Toloka
    Args:
        images_folder: location of files with images.
        annotations_file: annotations '.xml' file location.
        file_extensions: extension/extensions of image file. From folder will be read files with this extension.
        dataset_name: Dataset name will be used in meta information about dataset.
        dataset_description: Dataset description will be used in meta information about dataset.
        dataset_part: define the dataset part, can be 'train', 'test' or 'validation'.
        input_column_name: column name with the input data in Toloka file.
        result_column_name: column name with the output data in Toloka file.
    Returns:
        ImagesDataset without annotation
    """
    try:
        toloka_annotations = pd.read_csv(annotations_file, delimiter='\t', sep='\n')
        raw_ds = raw_images(
            input_folder=images_folder,
            file_extensions=file_extensions,
            dataset_name=dataset_name,
            dataset_description=dataset_description,
            dataset_part=dataset_part
        )
        for _, row in toloka_annotations.iterrows():
            file_name = Path(row[input_column_name]).name
            res_polygons = loads_toloka_json(row[result_column_name])
            ds_item = raw_ds[file_name]
            im_width = ds_item.file_info.width
            im_height = ds_item.file_info.height
            objects = []
            for obj in res_polygons:
                points = []
                for point in obj["points"]:
                    points.append((min(point["left"], 1.0) * im_width, min(point["top"], 1.0) * im_height))
                objects.append(
                    DetectionObjectPolygon(
                        polygon=Polygon(points),
                        label=obj["label"]
                    )
                )
            ds_item.annotations.add_objects(objects)
    except (IOError, TypeError, KeyError, AttributeError, pd.io.parsers.ParserError, pd.io.parsers.EmptyDataError) as e:
        raise e

    return raw_ds
