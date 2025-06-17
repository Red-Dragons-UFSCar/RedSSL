import numpy as np
from numpy import sqrt
from entities.SpatialCoordinates import SpatialCoordinates
from entities.Velocities import Velocities
from commons.kalmanfilter import KalmanFilter


class KinematicBody:
    """Base class for all moving bodies"""

    def __init__(self):
        self._coordinates = SpatialCoordinates()
        self._velocities = Velocities()
        self._is_filtered = True
        self.filter: KalmanFilter = KalmanFilter()
        self.unfiltered_coordinate_buffer = self._coordinates
        self._velocity_cache = (0.0, 0.0)  # cache para componentes X e Y da velocidade

    def set_coordinates(self, x, y, rotation=0):
        if self._is_filtered:
            self.filtered_coordinates(x, y, rotation)
        else:
            self.unfiltered_coordinates(x, y, rotation)

    def filtered_coordinates(self, x, y, rotation):
        self._coordinates.rotation = rotation
        self.filter.v_prediz_kalman()
        self.filter.v_atualiza_kalman(np.array([x, y]))
        self.filter.xPred = self.filter.x
        self.filter.pPred = self.filter.P
        self._coordinates.X = self.filter.x[0][0]
        self._coordinates.Y = self.filter.x[1][0]
        self._coordinates.rotation = rotation
        vel_linear = sqrt(self.filter.x[2][0] ** 2 + self.filter.x[3][0] ** 2)
        self._velocity_cache = (self.filter.x[2][0], self.filter.x[3][0])
        self.set_velocities(
            vel_linear,
            self._velocities.angular,
            self._velocities.v_top_right,
            self._velocities.v_top_left,
            self._velocities.v_bottom_right,
            self._velocities.v_bottom_left,
        )

    def unfiltered_coordinates(self, x, y, rotation):
        self._coordinates.X = x
        self._coordinates.Y = y
        self._coordinates.rotation = rotation

    def set_velocities(
        self, linear, angular, v_top_right, v_top_left, v_bottom_right, v_bottom_left
    ):
        self._velocities.linear = linear
        self._velocities.angular = angular
        self._velocities.v_top_right = v_top_right
        self._velocities.v_top_left = v_top_left
        self._velocities.v_bottom_right = v_bottom_right
        self._velocities.v_bottom_left = v_bottom_left

    def get_coordinates(self):
        """Returns coordinates"""
        return SpatialCoordinates(
            self._coordinates.X, self._coordinates.Y, self._coordinates.rotation
        )

    def get_velocities(self):
        """Returns velocities"""
        return Velocities(
            self._velocities.linear,
            self._velocities.angular,
            self._velocities.v_top_right,
            self._velocities.v_top_left,
            self._velocities.v_bottom_right,
            self._velocities.v_bottom_left,
        )

    def calculate_distance(self, body):
        """calculates the distance between self and another kinematic body"""
        return sqrt(
            (self.get_coordinates().X - body.get_coordinates().X) ** 2
            + (self.get_coordinates().Y - body.get_coordinates().Y) ** 2
        )

    def show_info(self):
        """Input: None
        Description: Logs location and velocity info on the console.
        Output: Obstacle data."""
        print(
            "coordinates.X: {:.2f} | coordinates.Y: {:.2f} | theta: {:.2f} | velocity: {:.2f}".format(
                self._coordinates.X,
                self._coordinates.Y,
                float(self._coordinates.rotation),
                self._velocities.linear,
            )
        )
