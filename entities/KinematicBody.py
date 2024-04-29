from numpy import sqrt, zeros, int32
from entities.SpatialCoordinates import SpatialCoordinates
from entities.Velocities import Velocities

#Units: cm, rad, s

class KinematicBody:
    #Base classe for all moving bodies

    def __init__(self):
        self._coordinates = SpatialCoordinates()
        self._velocities = Velocities()
    

    def set_coordinates(self, x, y, rotation):
        self._coordinates.X = x
        self._coordinates.Y = y
        self._coordinates.rotation = rotation


    def set_velocities(self, linear, angular, vtopRight, vTopLeft, vBottomRight, vBottomLeft):
        self._velocities.linear = linear
        self._velocities.angular = angular
        self._velocities.vtopRight = vtopRight
        self._velocities.vtopLeft = vTopLeft
        self._velocities.vbottomRight = vBottomRight
        self._velocities.vbottomLeft = vBottomLeft


    def get_coordinates(self):
        """Returns coordinates"""
        coordinates = SpatialCoordinates(self._coordinates.X, self._coordinates.Y, self._coordinates.rotation)
        return coordinates
    

    def get_velocities(self):
        """Returns velocities"""
        velocities = Velocities(self._velocities.linear, self._velocities.angular, self._velocities.vtopRight,
                                self._velocities.vtopLeft, self._velocities.vbottomRight, self._velocities.vbottomLeft)
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