import itertools
from pathlib import Path
from typing import Union, List, Optional
import os.path
import imagesize

from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.meta import DatasetMeta, DatasetPart, ImageFileInfo, DatasetType

from tqdm.auto import tqdm


def raw_images(
        input_folder: Path,
        file_extensions: Union[str, List[str]] = 'jpg',
        dataset_name: Optional[str] = None,
        dataset_description: Optional[str] = None,
        dataset_part: Union[DatasetPart, str] = DatasetPart.TRAIN
) -> ImagesDataset:
    """Create image dataset from images without annotations
    Args:
        input_folder: file with images.
        file_extensions: extension/extensions of image file. From folder will be read files with this extension.
        dataset_name: Dataset name will be used in meta information about dataset.
        dataset_description: Dataset description will be used in meta information about dataset.
        dataset_part: define the dataset part, can be 'train', 'test' or 'validation'
    Returns: ImageDataset without annotation
    """
    if not os.path.exists(input_folder):
        print(f"Path: '{input_folder}' not exist.")
        raise IOError

    if isinstance(dataset_part, str):
        assert dataset_part.lower() in ['train', 'test', 'validation'], "Incorrect name of part dataset"
        _dataset_part = DatasetPart(dataset_part.lower())
    else:
        _dataset_part = dataset_part

    if isinstance(file_extensions, str):
        _file_extensions = [f".{file_extensions}"]
    else:
        _file_extensions = list(map(lambda x: f".{x}", file_extensions))

    try:
        files = [Path(input_folder).glob(f'**/*{e}') for e in _file_extensions]
        files = sorted(list(itertools.chain.from_iterable(files)))
        image_dataset = ImagesDataset(
            dataset_meta=DatasetMeta(
                name=dataset_name if dataset_name is not None else '',
                version='1.0.0',
                description=dataset_description if dataset_description is not None else '',
                part=_dataset_part,
                dstype=DatasetType.IMAGE
            )
        )
        for file in tqdm(files, total=len(files)):
            if os.path.exists(file):
                width, height = imagesize.get(str(file))
                file_info = ImageFileInfo(
                    abs_path=file,
                    unique_id=file.name,
                    width=width,
                    height=height
                )
                image_dataset.add_item(file_info=file_info)
            else:
                print(f"File '{file}' not exist in path: '{input_folder}'")
    except IOError as e:
        raise e

    return image_dataset
