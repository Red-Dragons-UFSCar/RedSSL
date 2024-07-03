from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from path.visibilityGraph import VisibilityGraph
from control.PID import PID
import time
import numpy as np


def atualizar_target(robot0, x_target, y_target):
    n_points = len(x_target)

    target_distance = np.sqrt(
        (robot0.get_coordinates().X - x_target[robot0.cont_target]) ** 2
        + (robot0.get_coordinates().Y - y_target[robot0.cont_target]) ** 2
    )

    if target_distance < 10:
        robot0.cont_target = (robot0.cont_target + 1) % n_points


def calcular_target(robot0, x_target, y_target, theta_target, robots, enemy_robots, vg):
    atualizar_target(robot0, x_target, y_target)

    current_position = np.array(
        [robot0.get_coordinates().X, robot0.get_coordinates().Y]
    )
    current_target = np.array(
        [
            x_target[robot0.cont_target],
            y_target[robot0.cont_target],
            theta_target[robot0.cont_target],
        ]
    )

    next_target = desvio_obstaculo(
        current_position, current_target, robots, enemy_robots, vg
    )

    # Garantir que o next_target tenha o theta
    next_target_with_theta = np.array(
        [next_target[0], next_target[1], current_target[2]]
    )

    return next_target_with_theta


def quadradinho(robot0, robots, enemy_robots, vg):
    # Alvos para cada eixo coordenado
    x_target = [100, 100, 600, 600]
    y_target = [500, 100, 100, 500]
    theta_target = [-np.pi / 2, 0, np.pi / 2, np.pi]

    next_target = calcular_target(
        robot0, x_target, y_target, theta_target, robots, enemy_robots, vg
    )

    # Atualizar o target do robô
    robot0.set_target(next_target)


def inicializar_controladores_PID():
    # Controladores PID para posição e orientação
    Kp_x, Kd_x, Ki_x = 1 / 100, -0.0631 / 100, 0
    control_PID_x = PID(Kp_x, Kd_x, Ki_x, saturation=2)

    Kp_y, Kd_y, Ki_y = 1 / 100, -0.0169 / 100, 0
    control_PID_y = PID(Kp_y, Kd_y, Ki_y, saturation=2)

    Kp_theta, Kd_theta, Ki_theta = 0.6, 0, 0
    control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=1)

    return control_PID_x, control_PID_y, control_PID_theta


def desvio_obstaculo(current_position, current_target, robots, enemy_robots, vg):
    vg.set_origin(current_position)
    vg.set_target(current_target)

    # Adicionar obstáculos ao mapa de visibilidade
    vg_obstacles = []
    obstacles = robots[1:] + enemy_robots
    for obstacle in obstacles:
        triangle = vg.robot_triangle_obstacle(obstacle, robot0)
        vg_triangle = vg.convert_to_vgPoly(triangle)
        vg_obstacles.append(vg_triangle)

    vg.update_obstacle_map(vg_obstacles)
    path = vg.get_path()

    if path:
        # Pega o próximo ponto no caminho gerado pelo algoritmo de visibilidade
        next_point = path[1] if len(path) > 1 else path[0]
        next_target = np.array([next_point.x, next_point.y])
    else:
        # Se não há caminho, mantém o alvo atual
        next_target = current_target

    return next_target


def controle_PID(robot0, control_PID_x, control_PID_y, control_PID_theta):
    if robot0.target is None:
        return 0, 0, 0

    control_PID_x.set_target(robot0.target[0])
    control_PID_y.set_target(robot0.target[1])
    control_PID_theta.set_target(robot0.target[2])

    control_PID_x.set_actual_value(robot0.get_coordinates().X)
    vx = control_PID_x.update()

    control_PID_y.set_actual_value(robot0.get_coordinates().Y)
    vy = control_PID_y.update()

    control_PID_theta.set_actual_value(robot0.get_coordinates().rotation)
    w = control_PID_theta.update_angular()

    # Envio de velocidades para o robô
    robot0.sim_set_global_vel(vx, vy, w)


# Objeto de visão
visao = Vision(ip="224.5.23.2", port=10020)

# Client de conexão de atuação do simulador
actuator = Actuator(team_port=10301)

# Robôs azuis (o primeiro é o robô controlado, os outros são obstáculos)
robot0 = Robot(robot_id=0, actuator=actuator)
robot1 = Robot(robot_id=1, actuator=None)
robot2 = Robot(robot_id=2, actuator=None)

robots = [robot0, robot1, robot2]

# Robôs amarelos (considerados como obstáculos)
enemy_robot0 = Robot(robot_id=0, actuator=None)
enemy_robot1 = Robot(robot_id=1, actuator=None)

enemy_robots = [enemy_robot0, enemy_robot1]

# Inicializar controladores
control_PID_x, control_PID_y, control_PID_theta = inicializar_controladores_PID()

# Visibilidade
vg = VisibilityGraph()


# Contador para garantir a leitura dos dados da câmera
cont = 0
cont_target = 0

# Sinais de controle
vx, vy, w = 0, 0, 0

while True:
    t1 = time.time()

    # Recebimento dos dados da visão
    visao.update()
    frame = visao.get_last_frame()

    # Detecção dos robôs azuis
    for detection in frame["robots_blue"]:
        for i in range(len(robots)):
            if detection["robot_id"] == i:
                x_pos, y_pos, theta = (
                    detection["x"],
                    detection["y"],
                    detection["orientation"],
                )
                robots[i].set_coordinates(x_pos, y_pos, theta)

    # Detecção dos robôs amarelos
    for detection in frame["robots_yellow"]:
        for i in range(len(enemy_robots)):
            if detection["robot_id"] == i:
                x_pos, y_pos, theta = (
                    detection["x"],
                    detection["y"],
                    detection["orientation"],
                )
                enemy_robots[i].set_coordinates(x_pos, y_pos, theta)

    cont += 1

    # Se foi recebido ao menos 5 frames de visão, realizar o controle
    if cont == 5:
        quadradinho(robot0, robots, enemy_robots, vg)

        controle_PID(robot0, control_PID_x, control_PID_y, control_PID_theta)

        cont = 0

    t2 = time.time()

    if (t2 - t1) < 1 / 300:
        time.sleep(1 / 300 - (t2 - t1))
