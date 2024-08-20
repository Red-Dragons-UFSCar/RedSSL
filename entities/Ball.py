from entities.KinematicBody import KinematicBody



class Ball(KinematicBody):
    """Stores data on the game ball."""
    def __init__(self):
        super().__init__()
    def set_coordinates(self, x, y):
        super().set_coordinates(x, y, 0)
        