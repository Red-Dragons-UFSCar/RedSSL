from entities.KinematicBody import KinematicBody
from path.visibilityGraph import VisibilityGraph


class Target(KinematicBody):
    def __init__(self):
        super().__init__()
        self.visibility_graph = VisibilityGraph()

    def set_target(
        self, robot, target_coordinates, robots, enemy_robots, target_rotation=0
    ):
        # Atualiza o mapa de obstáculos
        self.visibility_graph.create_obstacle_map(robots, enemy_robots)

        target_x, target_y = target_coordinates
        new_target = self.visibility_graph.update_target_with_obstacles(
            robot, robots, enemy_robots, [target_x], [target_y], 0
        )
        self.set_coordinates(*new_target, target_rotation)
