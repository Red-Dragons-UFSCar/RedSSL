import pyvisgraph as vg
import numpy as np
from commons.math import angle_between, rotate_vector
from entities.Obstacle import Obstacle


class VisibilityGraph:
    """
    Descrição:
            Classe responsável pela criação de paths a partir do algoritmo
            Visibility Graph
    """

    def __init__(self) -> None:
        self.r_obstacle = 18  # Raio de tolerânica para o obstáculo
        self.obstacle_map = vg.VisGraph()  # Mapa de obstáculos do Visibility Graph
        self.origin = vg.Point(0, 0)  # Origem do path
        self.target = vg.Point(0, 0)  # Target do path

    def set_origin(self, coordinates: np.ndarray) -> None:
        """
        Descrição:
                Função que define a origem do path
        Entradas:
                coordinates:    Vetor numpy [1x2]
        """
        self.origin = vg.Point(coordinates[0], coordinates[1])

    def set_target(self, coordinates: np.ndarray) -> None:
        """
        Descrição:
                Função que define o fim/alvo do path
        Entradas:
                coordinates:    Vetor numpy [1x2]
        """
        self.target = vg.Point(coordinates[0], coordinates[1])

    def robot_triangle_obstacle(self, obstacle: Obstacle, robot) -> np.ndarray:
        """
        Descrição:
                Função responsável por definir os pontos triangulares
                que circunscrevem o obstáculo de raio R
        Entradas:
                obstacle:   Objeto da classe Obstacle
                robot:      Objeto da classe Robot
        Saídas:
                triangle:   Vetor numpy [3x2]
        """
        # Coordenadas do obstaculo
        obst_coords = obstacle.get_coordinates()
        obst_coords = np.array([obst_coords.X, obst_coords.Y])

        # Coordenadas do robô a realizar o path
        robot_coords = robot.get_coordinates()
        robot_coords = np.array([robot_coords.X, robot_coords.Y])

        # Pontos do triângulo padrão - Origem do sistema coordenado
        p1_x = self.r_obstacle
        p1_y = -np.sqrt(3) * self.r_obstacle

        p2_x = self.r_obstacle
        p2_y = np.sqrt(3) * self.r_obstacle

        p3_x = -2 * self.r_obstacle
        p3_y = 0

        p1 = np.array([p1_x, p1_y])
        p2 = np.array([p2_x, p2_y])
        p3 = np.array([p3_x, p3_y])

        # Angulo entre o obstaculo e o robô em relação ao eixo x
        ref_vector = np.array([1, 0])
        theta = angle_between(robot_coords - obst_coords, ref_vector)

        # Rotação do triângulo
        p1 = rotate_vector(p1, theta)
        p2 = rotate_vector(p2, theta)
        p3 = rotate_vector(p3, theta)

        # Translação do triângulo para as coordenadas do obstaculo
        p1[0], p1[1] = p1[0] + obst_coords[0], p1[1] + obst_coords[1]
        p2[0], p2[1] = p2[0] + obst_coords[0], p2[1] + obst_coords[1]
        p3[0], p3[1] = p3[0] + obst_coords[0], p3[1] + obst_coords[1]
        triangle = np.array([p1, p2, p3])

        return triangle

    def convert_to_vgPoly(self, points: np.ndarray) -> vg.Point:
        """
        Descrição:
                Função responsável por converter um array numpy
                em pontos da biblioteca VisibilityGraph
        Entradas:
                points:     Vetor numpy [3x2]
        Saídas:
                polygons:   Vetor de pontos VisibilityGraph
        """
        polygons = []
        for point in points:
            poly = vg.Point(point[0], point[1])
            polygons.append(poly)
        return polygons

    def update_obstacle_map(self, vg_obstacles) -> None:
        """
        Descrição:
                Função responsável por converter um conjunto de poligonos
                VisibilityGraph em um mapa de obstaculos
        Entradas:
                points:     Vetor de poligonos VisibilityGraph
        """
        self.obstacle_map = vg.VisGraph()
        self.obstacle_map.build(vg_obstacles)

    def create_obstacle_map(self, robots, enemy_robots):
        """
        Descrição:
                Função responsável por converter um conjunto de poligonos
                VisibilityGraph em um mapa de obstaculos
        Entradas:
                points:     Vetor de poligonos VisibilityGraph
        """
        vg_obstacles = []
        print("Mapeando obstáculos:")
        for robot in robots:
            if robot.obst.is_active:
                obstacle = self.robot_triangle_obstacle(robot.obst, robot)
                obstacle_vg = self.convert_to_vgPoly(obstacle)
                vg_obstacles.append(obstacle_vg)
                print(f"Robô {robot.robot_id}: {obstacle}")

        for enemy_robot in enemy_robots:
            if enemy_robot.obst.is_active:
                obstacle = self.robot_triangle_obstacle(enemy_robot.obst, enemy_robot)
                obstacle_vg = self.convert_to_vgPoly(obstacle)
                vg_obstacles.append(obstacle_vg)
                print(f"Robô inimigo {enemy_robot.robot_id}: {obstacle}")

        self.update_obstacle_map(vg_obstacles)

    def update_target_with_obstacles(
        self, robot, robots, enemy_robots, X_path, Y_path, target_idx
    ) -> np.ndarray:
        """
        Descrição:
                Função responsável por definir um path e retornar um ponto acessível
        Entradas:
                robot:          Objeto da classe Robot
                robots:         Lista de objetos da classe Robot
                enemy_robots:   Lista de objetos da classe Robot
                X_path:         Lista de pontos X
                Y_path:         Lista de pontos Y
                target_idx:     Ponto target
        """
        current_target = np.array([X_path[target_idx], Y_path[target_idx]])
        self.set_target(current_target)

        robot_coords = robot.get_coordinates()
        current_coords = np.array([robot_coords.X, robot_coords.Y])
        self.set_origin(current_coords)

        path = self.obstacle_map.shortest_path(self.origin, self.target)

        if not path:
            # Se não houver caminho, retornar a posição atual
            return current_coords

        for point in path:
            point_coords = np.array([point.x, point.y])
            if np.linalg.norm(point_coords - current_coords) < self.r_obstacle:
                continue
            return point_coords

        return current_coords
