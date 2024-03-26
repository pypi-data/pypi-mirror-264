import itertools
from pathlib import Path
from typing import Union, List, Optional

from cvd.datasets.meta import DatasetMeta, DatasetPart, DatasetType, VideoFileInfo
from cvd.datasets.video_dataset import VideoDataset
import cv2


def raw_videos(
        input_folder: Path,
        file_extensions: Union[str, List[str]] = 'mp4',
        dataset_name: Optional[str] = None,
        dataset_description: Optional[str] = None,
        dataset_part: Union[DatasetPart, str] = DatasetPart.TRAIN
) -> VideoDataset:
    """Create image dataset from images without annotations
    Args:
        input_folder: file with videos.
        file_extensions: extension/extensions of image file. From folder will be read files with this extension.
        dataset_name: Dataset name will be used in meta information about dataset.
        dataset_description: Dataset description will be used in meta information about dataset.
        dataset_part: define the dataset part, can be 'train', 'test' or 'validation'
    Returns: VideoDataset without annotation

    """
    if isinstance(dataset_part, str):
        assert dataset_part.lower() in ['train', 'test', 'validation'], "Incorrect name of part dataset"
        _dataset_part = DatasetPart(dataset_part.lower())
    else:
        _dataset_part = dataset_part

    if isinstance(file_extensions, str):
        _file_extensions = [f".{file_extensions}"]
    else:
        _file_extensions = list(map(lambda x: f".{x}", file_extensions))
    if input_folder.is_dir():
        files = [Path(input_folder).glob(f'**/*{e}') for e in _file_extensions]
        files = sorted(list(itertools.chain.from_iterable(files)))
    else:
        files = [input_folder]
    video_dataset = VideoDataset(
        dataset_meta=DatasetMeta(
            name=dataset_name if dataset_name is not None else '',
            version='1.0.0',
            description=dataset_description if dataset_description is not None else '',
            part=_dataset_part,
            dstype=DatasetType.VIDEO
        )
    )
    for file in files:
        cap = cv2.VideoCapture(str(file))

        # get total number of frames
        total_frames = 0
        while True:
            ret, frame = cap.read()
            if ret:
                total_frames += 1
            else:
                break
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        file_info = VideoFileInfo(
            abs_path=file,
            unique_id=file.stem,
            width=width,
            height=height,
            fps=fps,
            frames_number=total_frames
        )
        video_dataset.add_item(file_info=file_info)

    return video_dataset
