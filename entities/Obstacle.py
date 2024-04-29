from entities.KinematicBody import KinematicBody

class Obstacle(KinematicBody):
    """Input: Coordinates and velocity of object.
    Description: Stores coordinates and velocity of an obstacle to a robot.
    Output: Coordinates and velocity of object."""

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

    def set_obst(self, x, y, rotation):
        """Input: Coordinates of obstacle.
        Description: Sets obstacle coordinates with data from vision.
        Output: None"""
        self.set_coordinates(x, y, rotation)