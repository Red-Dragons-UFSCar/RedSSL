from entities.KinematicBody import KinematicBody

class Target(KinematicBody):
    """Input: Current target coordinates.
    Description: Stores coordinates for the robots' current target.
    Output: Current target coordinates."""

    def __init__(self):
        super().__init__()