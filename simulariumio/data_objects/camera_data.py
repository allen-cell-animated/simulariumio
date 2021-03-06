#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict

import numpy as np

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class CameraData:
    position: np.ndarray
    look_at_position: np.ndarray
    up_vector: np.ndarray
    fov_degrees: float

    def __init__(
        self,
        position: np.ndarray = np.array([0.0, 0.0, 120.0]),
        look_at_position: np.ndarray = np.zeros(3),
        up_vector: np.ndarray = np.array([0.0, 1.0, 0.0]),
        fov_degrees: float = 50.0,
    ):
        """
        This object holds parameters that define
        a camera view of the 3D scene

        Parameters
        ----------
        position : np.ndarray (shape = [3]) (optional)
            3D position of the camera itself
            Default: np.array([0.0, 0.0, 120.0])
        look_at_position : np.ndarray (shape = [3]) (optional)
            position the camera looks at
            Default: np.zeros(3)
        up_vector : np.ndarray (shape = [3]) (optional)
            the vector that defines which direction
            is "up" in the camera's view
            Default: np.array([0.0, 1.0, 0.0])
        fov_degrees : float (optional)
            the angle defining the extent of the 3D world
            that is seen from bottom to top of the camera view
            Default: 50.0
        """
        self.position = position
        self.look_at_position = look_at_position
        self.up_vector = up_vector
        self.fov_degrees = fov_degrees

    @classmethod
    def from_buffer_data(cls, buffer_data: Dict[str, Any]):
        """ """
        return cls(
            position=np.array(
                [
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"]["position"]["x"]
                    ),
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"]["position"]["y"]
                    ),
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"]["position"]["z"]
                    ),
                ]
            ),
            look_at_position=np.array(
                [
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"][
                            "lookAtPosition"
                        ]["x"]
                    ),
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"][
                            "lookAtPosition"
                        ]["y"]
                    ),
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"][
                            "lookAtPosition"
                        ]["z"]
                    ),
                ]
            ),
            up_vector=np.array(
                [
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"]["upVector"]["x"]
                    ),
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"]["upVector"]["y"]
                    ),
                    float(
                        buffer_data["trajectoryInfo"]["cameraDefault"]["upVector"]["z"]
                    ),
                ]
            ),
            fov_degrees=float(
                buffer_data["trajectoryInfo"]["cameraDefault"]["fovDegrees"]
            ),
        )

    def __deepcopy__(self, memo):
        result = type(self)(
            position=np.copy(self.position),
            look_at_position=np.copy(self.look_at_position),
            up_vector=np.copy(self.up_vector),
            fov_degrees=self.fov_degrees,
        )
        return result
