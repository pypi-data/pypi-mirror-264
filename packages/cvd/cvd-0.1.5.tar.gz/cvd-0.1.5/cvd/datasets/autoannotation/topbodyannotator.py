from copy import deepcopy
from pathlib import Path
from typing import Optional

import numpy as np
import requests
from skimage.measure import label, regionprops

from cvd.datasets.annotations import DetectionObject, BBoxXYXY
from cvd.datasets.annotations.type import ObjectsSet
from cvd.datasets.autoannotation import IAutoAnnotator
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from mmpose.apis import inference_top_down_pose_model, init_pose_model, vis_pose_result


class TopBodyAnnotator(IAutoAnnotator):
    def __init__(
            self,
            instance_segmentation_threshold: float = 0.6,
            pose_model_config: str = "/opt/app/external/mmpose/configs/top_down/hrnet/coco/hrnet_w48_coco_256x192.py",
            pose_model_weight: Optional[str] = None

    ):
        # instance segmentation model from Detectron2
        self.cfg = get_cfg()
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = instance_segmentation_threshold  # set threshold for this model
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")
        self.predictor = DefaultPredictor(self.cfg)

        if pose_model_weight is None and Path(pose_model_config).name == "hrnet_w48_coco_256x192.py":
            url = 'https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth'
            r = requests.get(url, allow_redirects=True, )
            pose_model_weight = '/opt/app/model-weights/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth'
            open(pose_model_weight, 'wb').write(r.content)
        else:
            raise Exception("Incorrect file config. Weight file is downloaded only for hrnet_w48_coco_256x192.py config")

        self.pose_model = init_pose_model(
            pose_model_config,
            "/opt/app/model-weights/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth",
            device='cuda'
        )

    def _model(self, image: np.ndarray, objects: Optional[ObjectsSet]) -> ObjectsSet:
        dataset = self.pose_model.cfg.data['test']['type']
        person_results = []
        objects_top_body = []
        for obj in objects:
            person = {}
            # bbox format is 'xywh'
            bbox = obj.bbox.toxywh()
            if obj.label == 'person':
                person['bbox'] = [bbox.x, bbox.y, bbox.width, bbox.height]
                person_results.append(person)

        # mmdetection keypoint model
        pose_results, returned_outputs = inference_top_down_pose_model(
            self.pose_model,
            image,
            person_results,
            bbox_thr=None,
            format='xywh',
            dataset=dataset,
            return_heatmap=False,
            outputs=None)
        # detectron2 segmentation model
        instances = self._seg_predict(image)

        # bboxes from prediction detectron2
        detectron_boxes = instances.pred_boxes.tensor.cpu().detach().tolist()

        for pose_res in pose_results:
            bbox = pose_res['bbox']
            if detectron_boxes:
                # Поиск сегманта соотвествующего исходногу боксу и вычисление бокса по сегменту
                # TODO: Заменить метод _iou на общую реализацию и убрать из класса
                iou_res = list(map(lambda x: self._iou(x[0], x[1]), zip([bbox] * len(detectron_boxes), detectron_boxes)))
                max_iou_arg = int(np.argmax(iou_res))
                one_detection = instances[max_iou_arg]
                pred_mask = one_detection.pred_masks.cpu().detach().numpy()[0, :]

                top_body_points = pose_res["keypoints"][:7]
                elbow_points = pose_res["keypoints"][8:10]
                head_points = pose_res["keypoints"][:5]
                head_points = head_points[head_points[:, 2] > 0.3]
                top_body_points = top_body_points[top_body_points[:, 2] > 0.1]
                if top_body_points.size and head_points.size:
                    bbox = pose_res['bbox']
                    top_body_points = top_body_points.astype(np.int32)

                    ymin = np.min(top_body_points[:, 1])
                    ymax = np.max(top_body_points[:, 1])
                    ymax += (ymax - ymin) // 2

                    pred_mask_top = deepcopy(pred_mask)
                    pred_mask_top[ymax:, :] = False
                    lbl_top = label(pred_mask_top)
                    props_top = regionprops(lbl_top)
                    if props_top:
                        prop_bbox_top = props_top[0].bbox

                        prop_bbox_xmin_top = prop_bbox_top[1]
                        prop_bbox_ymin_top = prop_bbox_top[0]
                        prop_bbox_xmax_top = prop_bbox_top[3]
                        top_elbow_y = np.min(elbow_points[:, 1])
                        xmin = max(bbox[0], min(prop_bbox_xmin_top, np.min(top_body_points[:, 0])))
                        ymin = min(prop_bbox_ymin_top, int(np.min(top_body_points[:, 1])))
                        ymin = max(ymin, ymin if np.min(head_points[:, 1]) < top_elbow_y else top_elbow_y)
                        xmax = min(bbox[2], max(prop_bbox_xmax_top, np.max(top_body_points[:, 0])))
                        objects_top_body.append(
                            DetectionObject(
                                BBoxXYXY(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax),
                                label='top_body'

                            )
                        )
        return objects_top_body

    def _iou(self, bbox: list, other_bbox: list):
        """ Calculates IoU for two bboxes, in format: [x1,y1,x2,y2] """
        inter_x_min = max(bbox[0], other_bbox[0])
        inter_y_min = max(bbox[1], other_bbox[1])
        inter_x_max = min(bbox[2], other_bbox[2])
        inter_y_max = min(bbox[3], other_bbox[3])

        inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)
        bbox_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        other_bbox_area = (other_bbox[2] - other_bbox[0]) * (other_bbox[3] - other_bbox[1])

        return inter_area / float(bbox_area + other_bbox_area - inter_area)

    def _seg_predict(self, img):
        outputs = self.predictor(img)
        instances = outputs["instances"]
        category_0_detections = instances[instances.pred_classes == 0]
        return category_0_detections
