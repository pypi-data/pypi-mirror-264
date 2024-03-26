from typing import Optional

from cvd.datasets.annotations import DetectionObject, BBoxXYXY
from cvd.datasets.annotations.type import ObjectsSet
from cvd.datasets.autoannotation.iautoannotator import IAutoAnnotator
from retinaface.pre_trained_models import get_model
import numpy as np


class RetinaFaceAnnotator(IAutoAnnotator):

    def __init__(self, confidence_threshold: float = 0.8, nms_threshold: float = 0.4, device: str = 'cuda'):
        self._confidence_threshold = confidence_threshold
        self._nms_threshold = nms_threshold
        self._retina_face_model = get_model("resnet50_2020-07-20", max_size=2048, device='cuda')

    def _model(self, image: np.ndarray, objects: Optional[ObjectsSet]) -> ObjectsSet:
        objs = self._retina_face_model.predict_jsons(image, confidence_threshold=self._confidence_threshold)
        height, width, _ = image.shape
        face_objs = []
        for det in objs:
            # print(det)
            if det["bbox"]:
                face_objs.append(
                    DetectionObject(
                        bbox=BBoxXYXY(
                            xmin=max(0, det["bbox"][0]),
                            ymin=max(0, det["bbox"][1]),
                            xmax=min(width, det["bbox"][2]),
                            ymax=min(height, det["bbox"][3])
                        ),
                        label='face'
                    )
                )
        return face_objs
