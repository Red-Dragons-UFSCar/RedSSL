import pyvisgraph as vg
import numpy as np

from commons.math import angle_between, rotate_vector

class VisibilityGraph():
    def __init__(self) -> None:
        self.r_obstable = 18                # Raio de tolerânica para o obstáculo
        self.obstacle_map = vg.VisGraph()   # Mapa de obstáculos do Visibility Graph
        self.origin = vg.Point(0, 0)        # Origem do path
        self.target = vg.Point(0, 0)        # Target do path

    def set_origin(self, coordinates):
        self.origin = vg.Point(coordinates[0], coordinates[1])
    
    def set_target(self, coordinates):
        self.target = vg.Point(coordinates[0], coordinates[1])
    
    def robot_triangle_obstacle(self, obstacle, robot):
        obst_coords = obstacle.get_coordinates()
        obst_coords = np.array([obst_coords.X, obst_coords.Y])

        robot_coords = robot.get_coordinates()
        robot_coords = np.array([robot_coords.X, robot_coords.Y])

        p1_x = self.r_obstable
        p1_y = - np.sqrt(3) * self.r_obstable

        p2_x = self.r_obstable
        p2_y = np.sqrt(3) * self.r_obstable

        p3_x = -2*self.r_obstable
        p3_y = 0

        p1 = np.array([p1_x, p1_y])
        p2 = np.array([p2_x, p2_y])
        p3 = np.array([p3_x, p3_y])

        ref_vector = np.array([1, 0])
        theta = angle_between(robot_coords-obst_coords, ref_vector)

        p1 = rotate_vector(p1, theta)
        p2 = rotate_vector(p2, theta)
        p3 = rotate_vector(p3, theta)

        p1[0], p1[1] = p1[0] + obst_coords[0], p1[1]+obst_coords[1] 
        p2[0], p2[1] = p2[0] + obst_coords[0] , p2[1]+obst_coords[1] 
        p3[0], p3[1] = p3[0] + obst_coords[0] , p3[1]+obst_coords[1] 
        triangle = np.array([p1, p2, p3])

        return triangle
    
    def convert_to_vgPoly(self, points):
        polygons = []
        for point in points:
            poly = vg.Point(point[0], point[1])
            polygons.append(poly)
        return polygons
    
    def update_obstacle_map(self, vg_obstacles):
        self.obstacle_map = vg.VisGraph()
        self.obstacle_map.build(vg_obstacles)
    
    def get_path(self):
        path = self.obstacle_map.shortest_path(self.origin, self.target)
        return path