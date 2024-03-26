import logging
import sys
from copy import deepcopy
from pathlib import Path
from typing import Dict, Union, Tuple

import PIL
import cv2
import numpy as np
import torch
from PIL import Image
from torch import Tensor, FloatTensor
from torch.utils.data import Dataset
import torchvision.transforms.functional as tvf

from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.objects import DetectionObjectBBox
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.augumentation.crop import random_crop
from cvd.datasets.augumentation.filters import filter_bboxes
from cvd.datasets.augumentation.flip import horizontal_flip, vertical_flip
from cvd.datasets.augumentation.rotate import rotate
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.image_dataset_item import ImageDatasetItem
from tempfile import NamedTemporaryFile
import albumentations

from cvd.datasets.transformations.normalize import normalize_bbox
from cvd.datasets.transformations.resize import resize


def uniform(a, b):
    return a + np.random.rand() * (b-a)


class TorchRotatedBBoxDataset(Dataset):
    def __init__(
            self,
            dataset: ImagesDataset,
            label2index: Dict[str, int],
            img_size: Tuple[int, int] = (608, 608),
            enable_aug: bool = True,
            debug: bool = False
    ):
        """
        dataset initialization. Annotation data are read into memory by API.

        Args:
            dataset: dataset
            img_size: Tuple[int, int], target image size [width, height] input to the YOLO, default: [608, 608]
            enable_aug: bool, enable data augmentations default: True
            debug: bool, if True, only returned dataset item with transformed images and labels
        """
        self._max_labels = 50
        self._dataset = dataset
        self._label2index = label2index
        self._index2label = dict((v, k) for k, v in label2index.items())
        self._img_size = img_size
        self.enable_aug = enable_aug
        self._logger = logging.getLogger(self.__class__.__name__)
        self._debug = debug
        self._tmp_folder_name = Path(NamedTemporaryFile().name)
        self._tmp_folder_name.mkdir(parents=True, exist_ok=True)

    @property
    def img_size(self):
        return self._img_size


    @img_size.setter
    def img_size(self, value: Tuple[int, int]):
        assert isinstance(value, Tuple), "Incorrect type of img_size"
        self._img_size = value

    def __len__(self):
        return len(self._dataset)

    def __getitem__(self, index):
        ds_item: ImageDatasetItem = self._dataset[index]
        img_id = ds_item.file_info.unique_id
        image = Image.fromarray(ds_item.load_image())
        ori_w, ori_h = image.width, image.height
        if image.mode == 'L':
            self._logger.error("Grayscale images don't supported")
            raise Exception("Grayscale images don't supported")

        # load unnormalized annotation
        annotations: ImageAnnotation = ds_item.annotations

        # bboxes shape(50, 5), 5 = [x, y, w, h, angle]
        bboxes = torch.zeros(self._max_labels, 5)
        labels = torch.zeros(self._max_labels, dtype=torch.int32)
        gt_num = 0

        if annotations.objects:
            np_bboxes, np_labels = annotations.to_numpy(self._label2index)
            input_bboxes = torch.FloatTensor(np_bboxes)
            input_labels = torch.IntTensor(np_labels)

            # augmentation
            if self.enable_aug:
                # image, bboxes[:gt_num] = self.augment_PIL(image, bboxes[:gt_num])
                image, aug_bboxes, aug_labels = self._augumentation(image, input_bboxes, input_labels)
                assert aug_bboxes.shape[0] == aug_labels.shape[0], "Bboxes number don't equal labels number"
            else:
                aug_bboxes, aug_labels = input_bboxes, input_labels



            if aug_bboxes.shape[0] > self._max_labels:
                gt_num = self._max_labels
                bboxes = aug_bboxes[:gt_num]
                labels = aug_labels[:gt_num]

            else:
                gt_num = aug_bboxes.shape[0]
                bboxes[:gt_num] = aug_bboxes
                labels[:gt_num] = aug_labels

        # pad to square
        try:
            image, bboxes[:gt_num], labels[:gt_num], pad_info = resize(
                image=image,
                bboxes=bboxes[:gt_num],
                labels=labels[:gt_num],
                target_size=self.img_size,
                pad_value=0,
                save_proportion=False
            )
        except Exception as e:
            t, v, tb = sys.exc_info()
            print("gt_num=", gt_num)
            print(ds_item.file_info)
            print(ds_item.annotations.objects)
            raise e

        # change order if width > height
        width_gr_height = bboxes[:, 2] > bboxes[:, 3]
        bboxes[width_gr_height, 2], bboxes[width_gr_height, 3] = bboxes[width_gr_height, 3], bboxes[width_gr_height, 2]
        bboxes[width_gr_height & (bboxes[:, 4] > 90), 4] -= 90
        bboxes[width_gr_height & (bboxes[:, 4] < -90), 4] += 90

        if not self._debug:
            image = tvf.to_tensor(image)
            bboxes[:gt_num] = normalize_bbox(bboxes[:gt_num], self.img_size[0], self.img_size[1])

            # x,y,w,h: 0~1, angle: -90~90 degrees
            assert image.dim() == 3 and image.shape[0] == 3 and image.shape[1] == image.shape[2]
            assert (bboxes[:, 2] <= bboxes[:, 3]).all(), f'{bboxes[bboxes[:,2]>bboxes[:,3]]}'
            assert (bboxes[:, 0] < 1).all() and (bboxes[:, 1] < 1).all(), f'{bboxes}'
            return image, bboxes, labels, str(img_id), pad_info
        else:
            objects = []
            for bbox, label in zip(bboxes[:gt_num], labels[:gt_num]):
                objects.append(
                    DetectionObjectBBox(
                        bbox=RBBoxXYCenterWHA(
                            x_center=bbox[0],
                            y_center=bbox[1],
                            width=bbox[2],
                            height=bbox[3],
                            angle=bbox[4]
                        ),
                        label=self._index2label[label.item()]
                    )
                )
            new_file_info = deepcopy(ds_item.file_info)
            new_file_info.abs_path = self._tmp_folder_name / ds_item.file_info.unique_id
            np_image = np.asarray(image)
            new_file_info.height, new_file_info.width = np_image.shape[:2]
            cv2.imwrite(str(new_file_info.abs_path), cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR))
            return ImageDatasetItem(
                file_info=new_file_info,
                annotations=ImageAnnotation(
                    objects=objects
                )
            ), bboxes[:gt_num]

    def _augumentation(self, image: Image, bboxes: FloatTensor, labels):
        light = albumentations.Compose([
            albumentations.OneOf(
                [
                    albumentations.RandomBrightnessContrast(p=0.5),
                    albumentations.RandomGamma(p=0.5),
                    albumentations.ChannelShuffle(p=0.2),
                    albumentations.HueSaturationValue(p=0.2),
                    albumentations.RGBShift(p=0.2)
                ],
                p=0.8
            ),
            albumentations.CLAHE(p=0.5, clip_limit=3),
            albumentations.GaussNoise(p=0.2),
            albumentations.GaussianBlur(p=0.2),
        ], p=1)
        augmented = light(image=np.asarray(image))
        image = PIL.Image.fromarray(augmented['image'])
        if np.random.rand() > 0.5:
            image, bboxes, labels = horizontal_flip(image, bboxes, labels)
        # vertical flip
        if np.random.rand() > 0.5:
            image, bboxes, labels = vertical_flip(image, bboxes, labels)
        # random rotation
        if np.random.rand() > 0.6:
            rand_degree = np.random.rand() * 360
            image, bboxes, labels = rotate(image, bboxes, labels, rand_degree,  expand=False)
        if np.random.rand() > 0:
            image, bboxes, labels = random_crop(
                image=image,
                bboxes=bboxes,
                labels=labels,
                min_max_width=(700, image.width),
                min_max_height=(700, image.height),
                min_max_x_center=(image.width // 2 - 100, image.width // 2 + 100),
                min_max_y_center=(image.height // 2 - 100, image.height // 2 + 100),
                save_proportion=True
            )

        image, bboxes, labels = filter_bboxes(image, bboxes, labels, min_area=1000, fix_mode='outside')
        return image, bboxes, labels


class TorchDataset(Dataset):
    def __getitem__(self, index) -> Tuple[Tensor, Tensor]:
        ds_item: ImageDatasetItem = self.image_dataset[index]
        img = cv2.cvtColor(cv2.imread(str(ds_item.file_info.abs_path)), cv2.COLOR_BGR2RGB)
        targets = []
        for obj in ds_item.annotations.objects:
            targets.append([obj.label, obj.bbox.x_min, obj.bbox.x_max, obj.bbox.y_min, obj.bbox.y_max])

        return img, targets

    def __init__(
            self,
            image_dataset: ImagesDataset,
            config_aug: Dict[str, Dict[str, Union[float, int]]]
    ):
        self.image_dataset = image_dataset
        self._transform = self._generate_aug(config_aug)


    def _generate_aug(self, config_aug):
        pass

    def __len__(self):
        return len(self.image_dataset)