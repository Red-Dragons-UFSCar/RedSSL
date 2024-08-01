from entities.KinematicBody import KinematicBody
from path.visibilityGraph import VisibilityGraph


class Target(KinematicBody):
    def __init__(self):
        super().__init__()
        self.visibility_graph = VisibilityGraph()

    def set_target(self, robot, robots, enemy_robots, target_x, target_y, cont_target):

        new_target = self.visibility_graph.update_target_with_obstacles(
            robot, robots, enemy_robots, target_x, target_y, cont_target
        )
        self.set_coordinates(*new_target, rotation=0)
