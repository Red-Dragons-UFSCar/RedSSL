import numpy as np
from commons.math import angle_between, rotate_vector, ortogonal_projection
from entities.Obstacle import Obstacle
import time
import concurrent.futures

IS_PYTHON_MODULE = False

if IS_PYTHON_MODULE:
        import pyvisgraph as vg
else:
        import sys
        import os
        #sys.path.insert(0, 
        #    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import path.cppvisgraph.build.cppyvisgraph as vg

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
        self.logger_obstacle = False  # Habilita o log de tempo da construção do mapa de obstaculos

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

        self.r_obstacle = obstacle.radius

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
        triangle = [p1, p2, p3]

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

    def update_obstacle_map(self) -> None:
        """
        Descrição:
                Função responsável por converter um conjunto de poligonos
                VisibilityGraph em um mapa de obstaculos
        """
        self.obstacle_map = vg.VisGraph()
        if IS_PYTHON_MODULE:
                self.obstacle_map.build(self.vg_obstacles, status=False, workers=1)
        else:
                if len(self.vg_obstacles) > 0:
                        self.obstacle_map.build(self.vg_obstacles)


    def get_path(self) -> list:
        """
        Descrição:
                Função responsável por gerar o path a partir dos
                obstaculos gerados
        Saídas:
                path:   Lista de pontos VisibilityGraph
        """
        path = self.obstacle_map.shortest_path(self.origin, self.target)
        return path

    def update_target_with_obstacles(
        self, robot, field, x_target, y_target, cont_target
    ):
        """
        Descrição:
                Função que atualiza o alvo considerando obstáculos e
                calcula o próximo ponto no caminho gerado pelo algoritmo de visibilidade.
        Entradas:
                robot0:         Objeto do robô controlado
                field:          Instância da classe Field
                x_target:       Lista de alvos no eixo x
                y_target:       Lista de alvos no eixo y
                cont_target:    Contador de alvo atual
        Saídas:
                next_target:    Próximo alvo considerando obstáculos
        """
        # Definir origem e alvo atuais
        current_position = np.array(
                [robot.get_coordinates().X, robot.get_coordinates().Y]
        )
        current_target = np.array([x_target[cont_target], y_target[cont_target]])
        self.set_origin(current_position)
        self.set_target(current_target)

        # Adicionar obstáculos ao mapa de visibilidade
        vg_obstacles = []
        obstacles = robot.map_obstacle.get_map_obstacle()

        for obstacle in obstacles: 
                if not self.ignore_obstacle(robot, field.ball, obstacle):
                        triangle = self.robot_triangle_obstacle(obstacle, robot)
                        vg_triangle = self.convert_to_vgPoly(triangle)
                        vg_obstacles.append(vg_triangle)
        self.vg_obstacles = vg_obstacles

        t1 = time.time()
        self.update_obstacle_map()

        t2 = time.time()
        if self.logger_obstacle:
                print("---- LOGGER OBSTACULO -----")
                print("Robô ", robot.robot_id)
                print("Tempo de construção do mapa de obstáculo: ", (t2-t1)*1000)
                if t2-t1 > 0.005:
                        print("[TIMEOUT]")
                print("----------------")
        
        path = self.get_path()

        if path:
                # Pega o próximo ponto no caminho gerado pelo algoritmo de visibilidade
                next_point = path[1] if len(path) > 1 else path[0]
                next_target = np.array([next_point.x, next_point.y])
        else:
                # Se não há caminho, mantém o alvo atual
                next_target = current_target

        return next_target
    
    def ignore_obstacle(self, robot, ball, obstacle):
        """
        Descrição:
                Função que indica se um obstáculo deve ser desconsiderado.
                Caso a bola esteja entre o robô controlado e o obstáculo, mas dentro
                do obstáculo, então considera-se que esse a bola é acessível ao nosso
                robô e o obstáculo é indicado a ser desconsiderado.

                Por meio da projeção da posição do obstáculo (vetor u) e o vetor da reta 
                entre o robô e a bola, se a operação u*v/(v*v), sendo * o produto 
                escalar, for menor que 1, então quer dizer que a bola está depois do
                obstáculo e então ele não deve ser ignorado.
        Entradas:
                robot:          Robô realizando o percurso
                ball:           Objeto da bola
                obstacle:       Obstaculo em analise
        Saídas:
                ignore?:        Booleana que indica se deve ou não ignorar o obstaculo
        """
        p_robot = np.array([robot.get_coordinates().X, robot.get_coordinates().Y])  # Ponto coordenado robô
        p_ball = np.array([ball.get_coordinates().X, ball.get_coordinates().Y])  # Ponto coordenado bola
        p_obstacle = np.array([obstacle.get_coordinates().X, obstacle.get_coordinates().Y])  # Ponto coordenado obstáculo
        # Projeção ortogonal do obstáculo na reta robô-bola
        [_, t] = ortogonal_projection(p_robot, p_ball, p_obstacle)  

        if t>1:
              return True
        else:
              return False

