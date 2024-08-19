import numpy as np
from numpy import sqrt, zeros, int32
from entities.SpatialCoordinates import SpatialCoordinates
from entities.Velocities import Velocities
from commons.kalmanfilter import KalmanFilter
from commons.math import get_dif


# Units: cm, rad, s

class KinematicBody:
    """Base class for all moving bodies"""

    def __init__(self):
        self._coordinates = SpatialCoordinates()
        self._velocities = Velocities()
        self._is_filtered = False
        self.filter: KalmanFilter = KalmanFilter()
        self.unfiltered_coordinate_buffer = self._coordinates

    def set_coordinates(self, x, y, rotation):
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
        vel_linear = sqrt(self.filter.x[2]**2 + self.filter.x[3]**2)
        self.set_velocities(vel_linear, self._velocities.angular, self._velocities.v_top_right, self._velocities.v_top_left, self._velocities.v_bottom_right, self._velocities.v_bottom_left)

    def unfiltered_coordinates(self, x, y, rotation):
        self._coordinates.X = x
        self._coordinates.Y = y
        self._coordinates.rotation = rotation

    def set_velocities(self, linear, angular, v_top_right, v_top_left, v_bottom_right, v_bottom_left):
        self._velocities.linear = linear
        self._velocities.angular = angular
        self._velocities.v_top_right = v_top_right
        self._velocities.v_top_left = v_top_left
        self._velocities.v_bottom_right = v_bottom_right
        self._velocities.v_bottom_left = v_bottom_left

    def get_coordinates(self):
        """Returns coordinates"""
        coordinates = SpatialCoordinates(self._coordinates.X, self._coordinates.Y, self._coordinates.rotation)
        return coordinates

    def get_velocities(self):
        """Returns velocities"""
        velocities = Velocities(self._velocities.linear, self._velocities.angular, self._velocities.v_top_right,
                                self._velocities.v_top_left, self._velocities.v_bottom_right,
                                self._velocities.v_bottom_left)
        return velocities

    def calculate_distance(self, body):
        """calculates the distance between self and another kinematic body"""
        return sqrt((self.get_coordinates().X - body.get_coordinates().X) ** 2 +
                    (self.get_coordinates().Y - body.get_coordinates().Y) ** 2)

    def show_info(self):
        """Input: None
        Description: Logs location and velocity info on the console.
        Output: Obstacle data."""
        print('coordinates.X: {:.2f} | coordinates.Y: {:.2f} | theta: {:.2f} | velocity: {:.2f}'.format(
            self._coordinates.X, self._coordinates.Y, float(self._coordinates.rotation), self._velocities.linear))
