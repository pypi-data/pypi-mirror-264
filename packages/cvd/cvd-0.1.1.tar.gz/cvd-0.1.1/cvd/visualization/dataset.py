from pathlib import Path
from typing import Callable, Union, Optional, Tuple

import cv2

from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.image_dataset_item import ImageDatasetItem
from cvd.visualization.objects import draw_objects
from cvd.visualization.tools import get_mpl_colormap


def dataset_render(
        dataset: ImagesDataset,
        output_directory: Path,
        output_type: str = 'image',
        output_filename: Optional[str] = 'res.avi',
        fps_vido: int = 20,
        size: Tuple[int, int] = (1024, 768),
        sort_fn: Optional[Callable[[ImageDatasetItem], Union[str, int]]] = None,
        font_size: float = 1
):
    if isinstance(dataset, ImagesDataset):
        output_video = None
        color_map = dict(zip(dataset.labels, get_mpl_colormap("gist_rainbow", num=len(dataset.labels))))
        ds_items_list = list(dataset)
        if sort_fn:
            ds_items_list = sorted(ds_items_list, key=sort_fn)
        if output_type == 'video':
            output_video = cv2.VideoWriter(
                str(output_directory/output_filename),
                cv2.VideoWriter_fourcc(*'MJPG'),
                fps_vido,
                size
            )
        for ds_item in ds_items_list:
            img = cv2.cvtColor(cv2.imread(str(ds_item.file_info.abs_path)), cv2.COLOR_BGR2RGB)
            img = draw_objects(
                image=img,
                objects=ds_item.annotations.objects,
                label_to_color=color_map,
                font_size=font_size
            )
            if output_type == 'image':
                cv2.imwrite(
                    filename=str(output_directory / ds_item.file_info.abs_path.name),
                    img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                )
            elif output_type == 'video':
                resized = cv2.cvtColor(cv2.resize(img, size, interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2BGR)
                output_video.write(resized)

            else:
                raise Exception(f'Unsupported output_type `{output_type}`')
        if output_video:
            output_video.release()
    else:
        raise Exception("VideoDataset isn't supported")


def dataset_video_render(
        dataset: ImagesDataset,
        output_directory: Path,
        sort_fn: Callable[[ImageDatasetItem], Union[str, int]],
        font_size: float = 1
):

    color_map = dict(zip(dataset.labels, get_mpl_colormap("gist_rainbow", num=len(dataset.labels))))
    ds_items_list = list(dataset)
    res = sorted(ds_items_list, key=sort_fn)
    return res
    for ds_item in dataset:

        img = cv2.cvtColor(cv2.imread(str(ds_item.file_info.abs_path)), cv2.COLOR_BGR2RGB)
        img = draw_objects(
            image=img,
            objects=ds_item.annotations.objects,
            label_to_color=color_map,
            font_size=font_size
        )
        cv2.imwrite(
            filename=str(output_directory / ds_item.file_info.abs_path.name),
            img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        )