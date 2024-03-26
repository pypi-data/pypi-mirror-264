from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Union, Optional

import cv2
from scipy.spatial.distance import cosine
from sklearn.metrics import euclidean_distances

from cvd.datasets.annotations.objects import DetectionObjectPolygon, TrackGTObjectPolygon, DetectionObjectBBox
from cvd.datasets.annotations.polygon import Polygon
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.annotations.type import Object
from cvd.datasets.meta import ImageFileInfo, VideoFileInfo
import numpy as np
from scipy.ndimage import rotate
from scipy.spatial import ConvexHull


class Transformer(ABC):

    @abstractmethod
    def transform(self, obj: Object, file_info: Union[ImageFileInfo, VideoFileInfo]) -> Object:
        pass


class RotatedBBoxToAligned(Transformer):
    def transform(self, obj: Object, file_info: Union[ImageFileInfo, VideoFileInfo]) -> Object:
        new_obj = deepcopy(obj)
        new_obj.bbox = new_obj.bbox.toxyxy()
        return new_obj


class FishEyePolygonToRotatedBBox(Transformer):

    def transform(self, obj: Object, file_info: Union[ImageFileInfo, VideoFileInfo]) -> Optional[Object]:
        assert isinstance(obj, (DetectionObjectPolygon, TrackGTObjectPolygon)), \
            f"{self.__class__.__name__} transformation can be applyed only for DetectionObjectPolygon " \
            f"or TrackGTObjectPolygon"
        x_center, y_center, width, height, angle = self._minimum_bounding_rectangle(obj.polygon.contours(), file_info.width, file_info.height)
        if width > 0 and height > 0:
            return DetectionObjectBBox(
                bbox=RBBoxXYCenterWHA(
                    x_center=x_center,
                    y_center=y_center,
                    width=width,
                    height=height,
                    angle=angle
                ),
                label=obj.label,
                attributes=obj.attributes
            )
        return None

    def _minimum_bounding_rectangle(self, points, image_width, image_height):
        """
        Find the smallest bounding rectangle for a set of points.
        Returns a (x_center, y_xecnter, width, height, angle) of the bounding box.
        """
        pi2 = np.pi / 2.
        np_points = np.array(points).astype(np.int32)
        # get the convex hull for the points
        # hull_points = np_points[ConvexHull(np_points).vertices]

        min_x_hull_points = np.nanmin(np_points[:, 0], axis=0)
        max_x_hull_points = np.nanmax(np_points[:, 0], axis=0)
        min_y_hull_points = np.nanmin(np_points[:, 1], axis=0)
        max_y_hull_points = np.nanmax(np_points[:, 1], axis=0)
        x_middle_point = (min_x_hull_points + max_x_hull_points) / 2
        y_middle_point = (min_y_hull_points + max_y_hull_points) / 2

        middle_point = np.array([x_middle_point, y_middle_point])
        hull_points = np_points - middle_point

        middle_edge = np.array((image_width / 2 - x_middle_point, image_height / 2 - y_middle_point))
        middle_angle = np.arctan2(middle_edge[0], middle_edge[1])

        # middle_angle = np.abs(np.mod(middle_angle, pi2))
        # middle_angle = np.unique(middle_angle)[0]

        rotations = np.array(
            [[np.cos(middle_angle), np.cos(middle_angle - pi2)], [np.cos(middle_angle + pi2), np.cos(middle_angle)]])
        rot_points = np.matmul(hull_points, rotations)

        # find the bounding points
        min_x = np.nanmin(rot_points[:, 0], axis=0)
        max_x = np.nanmax(rot_points[:, 0], axis=0)
        min_y = np.nanmin(rot_points[:, 1], axis=0)
        max_y = np.nanmax(rot_points[:, 1], axis=0)
        angle = np.abs(np.mod(-middle_angle * 180/np.pi, 180))
        return middle_point[0], middle_point[1], max_x-min_x, max_y-min_y, angle


class PolygonToRotatedBBox(Transformer):
    def __init__(self, four_point_polygon: bool = False):
        self._four_point_polygon = four_point_polygon

    def transform(self, obj: Object, file_info: Union[ImageFileInfo, VideoFileInfo]) -> Optional[Object]:
        assert isinstance(obj, (DetectionObjectPolygon, TrackGTObjectPolygon)), \
            f"{self.__class__.__name__} transformation can be applyed only for DetectionObjectPolygon " \
            f"or TrackGTObjectPolygon"
        rect = self._transform_angle(obj.polygon.contours(), file_info.width, file_info.height)
        if rect[0][0] > 0 and rect[0][1]>0 and rect[1][1]>0:
            return DetectionObjectBBox(
                bbox=RBBoxXYCenterWHA(
                    x_center=rect[0][0],
                    y_center=rect[0][1],
                    width=rect[1][0],
                    height=rect[1][1],
                    angle=rect[2]
                ),
                label=obj.label,
                attributes=obj.attributes
            )
        return None


    def _transform_angle(self, contours_point, image_width, image_height):
        rect = cv2.minAreaRect(np.array(contours_point).astype(np.int))
        if self._four_point_polygon:
            contours_ref = self._rect_to_countour(rect)

            center_image_x = image_width/2
            center_image_y = image_height/2
            center_point_box_x = rect[0][0]
            center_point_box_y = rect[0][1]

            dist_point = euclidean_distances(contours_ref,[[center_image_x, center_image_y]])
            sorted_index = np.argsort(dist_point[:,0])[::-1]
            head_line = (contours_ref[sorted_index[0]], contours_ref[sorted_index[1]])
            tmp_head_line = (deepcopy(contours_ref[sorted_index[0]]), deepcopy(contours_ref[sorted_index[1]]))

            tmp_head_line[0][0] += center_image_x - center_point_box_x
            tmp_head_line[1][0] += center_image_x - center_point_box_x
            tmp_head_line[0][1] += center_image_y - center_point_box_y
            tmp_head_line[1][1] += center_image_y - center_point_box_y

            tmp_head_line_center_x = (tmp_head_line[0][0] + tmp_head_line[1][0]) / 2
            tmp_head_line_center_y = (tmp_head_line[0][1] + tmp_head_line[1][1]) / 2
            if tmp_head_line_center_x>=center_image_x:
                if tmp_head_line_center_y<=center_image_y:
                    quarter=1
                else:
                    quarter=2
                left_half = False
            else:
                if tmp_head_line_center_y<=center_image_y:
                    quarter=4
                else:
                    quarter=3
                left_half = True

            cnt_vector = (tmp_head_line_center_x - center_image_x, tmp_head_line_center_y - center_image_y)
            tmp_angle = (180 * np.arccos(1 - cosine(cnt_vector, [0,-1])))/3.14
            new_angle = 360 - tmp_angle if left_half else tmp_angle

            c, s = np.cos(-new_angle / 180 * np.pi), np.sin(-new_angle / 180 * np.pi)
            rotation_matrix = np.asarray([[c, s], [-s, c]])

            rect_points = []
            rect_points_ref = []
            for pt in contours_ref:
        #         rect_points.append((pt @ rotation_matrix - [rect[0][0], rect[0][1]]).astype(int))
                rect_points.append((pt - [rect[0][0], rect[0][1]]) @ rotation_matrix)
                rect_points_ref.append(pt- [rect[0][0], rect[0][1]])
            if rect_points[1][0] > 0 and rect_points[0][0]>0:
                new_height = rect_points[1][1] - rect_points[0][1]
                new_width = rect_points[1][0] - rect_points[2][0]
            elif rect_points[1][1] > 0 and rect_points[0][1]>0:
                new_height = rect_points[1][1] - rect_points[2][1]
                new_width = rect_points[0][0] - rect_points[1][0]
            elif rect_points[0][0] < 0 and rect_points[1][0]<0:
                new_height = rect_points[0][1] - rect_points[1][1]
                new_width = rect_points[2][0] - rect_points[1][0]
            elif rect_points[0][1] < 0 and rect_points[1][1]<0:
                new_height = rect_points[2][1] - rect_points[1][1]
                new_width = rect_points[1][0] - rect_points[0][0]

            return rect[0], (new_width, new_height), new_angle
        return rect[0], rect[1], rect[2]


    def _rect_to_countour(self, rect):
        width = rect[1][0]
        height = rect[1][1]
        c, s = np.cos(rect[2] / 180 * np.pi), np.sin(rect[2] / 180 * np.pi)
        rotation_matrix = np.asarray([[c, s], [-s, c]])
        pts = np.asarray(
            [
                [-width / 2, -height / 2],
                [width / 2, -height / 2],
                [width / 2, height / 2],
                [-width / 2, height / 2]
            ]
        )
        rect_points = []
        for pt in pts:
            rect_points.append(([rect[0][0], rect[0][1]] + pt @ rotation_matrix).astype(int))
        return np.array(list(map(lambda x: (int(x[0]), int(x[1])), rect_points)))