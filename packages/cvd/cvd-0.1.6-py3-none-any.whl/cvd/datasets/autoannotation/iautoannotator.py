import itertools
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional

import numpy as np

from cvd.datasets.annotations import ImageAnnotation
from cvd.datasets.annotations.type import ObjectsSet
from cvd.datasets.image_dataset import ImagesDataset

from tqdm.auto import tqdm


class IAutoAnnotator(ABC):

    @abstractmethod
    def _model(self, image: np.ndarray, objects: Optional[ObjectsSet]) -> ObjectsSet:
        pass

    def annotating(self, dataset: ImagesDataset) -> ImagesDataset:
        new_ds = ImagesDataset(dataset_meta=deepcopy(dataset.dataset_meta))
        new_ds.dataset_meta.version = ''
        new_ds.dataset_meta.description += f" UPDATE: {new_ds.dataset_meta.name} dataset is automatically " \
                                           f"(pre)labeled using the '{self.__class__.__name__}' AutoAnnotator  "
        pbar = tqdm(total=len(dataset))

        for dsitem in dataset:
            img = dsitem.load_image()
            new_objects = self._model(img, dsitem.annotations.objects)
            new_ds.add_item(
                file_info=deepcopy(dsitem.file_info),
                annotation=ImageAnnotation(objects=itertools.chain(dsitem.annotations.objects, new_objects))
            )
            pbar.update()
        pbar.close()
        return new_ds

