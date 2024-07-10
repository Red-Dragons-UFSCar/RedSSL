from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from control.PID import PID
from control.PID_discrete import PID_discrete
from path.visibilityGraph import VisibilityGraph
import time
import numpy as np


# Objeto de visão
visao = Vision(ip="224.5.23.2", port=10020)

# Client de conexão de atuação do simulador
actuator = Actuator(team_port=10301)

# Robôs azuis (o primeiro é o robô controlado, os outros são obstáculos)
robot0 = Robot(robot_id=0, actuator=actuator)
robot1 = Robot(robot_id=1, actuator=None)
robot2 = Robot(robot_id=2, actuator=None)
# robot3 = Robot(robot_id=3, actuator=None)
# robot4 = Robot(robot_id=4, actuator=None)

robots = [robot0, robot1, robot2]

# Robôs amarelos (considerados como obstáculos)
enemy_robot0 = Robot(robot_id=0, actuator=None)
enemy_robot1 = Robot(robot_id=1, actuator=None)
# enemy_robot2 = Robot(robot_id=2, actuator=None)
# enemy_robot3 = Robot(robot_id=3, actuator=None)
# enemy_robot4 = Robot(robot_id=4, actuator=None)

enemy_robots = [enemy_robot0, enemy_robot1]
# Controladores PID para posição e orientação

Kp_x, Kd_x, Ki_x = 1 / 100, -0.0631 / 100, 0
control_PID_x = PID(Kp_x, Kd_x, Ki_x, saturation=2)

Kp_y, Kd_y, Ki_y = 1 / 100, -0.0169 / 100, 0
control_PID_y = PID(Kp_y, Kd_y, Ki_y, saturation=2)

Kp_theta, Kd_theta, Ki_theta = 0.6, 0, 0
control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=1)
'''
Kp_x = 6.551
Kd_x = 1.004 
Ki_x = 0
N_x = 1/0.01898
control_PID_x = PID_discrete(Kp_x, Kd_x, Ki_x, saturation=1, N=N_x)

Kp_y = 4.857
Kd_y = 1.077 
Ki_y = 0
N_y = 1/0.01805
control_PID_y = PID_discrete(Kp_y, Kd_y, Ki_y, saturation=1, N=N_y)
'''
Kp_theta, Kd_theta, Ki_theta = 0.6, 0, 0
control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=1)

# Visibilidade
vg = VisibilityGraph()

# Alvos para cada eixo coordenado
x_target = [100, 100, 600, 600]
y_target = [500, 100, 100, 500]
theta_target = [-np.pi / 2, 0, np.pi / 2, np.pi]
n_points = len(x_target)
cont_target = 0

# Contador para garantir a leitura dos dados da câmera
cont = 0

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
        # print(f"Target atual: x = {x_target[cont_target]}, y = {y_target[cont_target]}")

        # Definir origem e alvo atuais
        current_position = np.array(
            [robot0.get_coordinates().X, robot0.get_coordinates().Y]
        )
        current_target = np.array([x_target[cont_target], y_target[cont_target]])
        vg.set_origin(current_position)
        vg.set_target(current_target)

        # Adicionar obstáculos ao mapa de visibilidade
        vg_obstacles = []
        obstacles = robots[1:] + enemy_robots
        for obstacle in obstacles:
            triangle = vg.robot_triangle_obstacle(obstacle, robot0)
            vg_triangle = vg.convert_to_vgPoly(triangle)
            vg_obstacles.append(vg_triangle)

        for robot in robots[1:]:
            print(robot.robot_id)

        vg.update_obstacle_map(vg_obstacles)
        path = vg.get_path()

        if path:
            # Pega o próximo ponto no caminho gerado pelo algoritmo de visibilidade
            next_point = path[1] if len(path) > 1 else path[0]
            next_target = np.array([next_point.x, next_point.y])
        else:
            # Se não há caminho, mantém o alvo atual
            next_target = current_target

        # Configura os controladores PID com o próximo alvo
        control_PID_x.set_target(next_target[0])
        control_PID_y.set_target(next_target[1])

        control_PID_x.set_actual_value(robot0.get_coordinates().X)
        vx = control_PID_x.update()

        control_PID_y.set_actual_value(robot0.get_coordinates().Y)
        vy = control_PID_y.update()

        control_PID_theta.set_actual_value(robot0.get_coordinates().rotation)
        w = control_PID_theta.update_angular()

        cont = 0

    # Envio de velocidades para o robô
    robot0.sim_set_global_vel(vx, vy, w)

    #print("Vx =", vx)
    #print("Vy =", vy)
    #print("w =", w)
    #print("---")

    target_distance = np.sqrt(
        (robot0.get_coordinates().X - x_target[cont_target]) ** 2
        + (robot0.get_coordinates().Y - y_target[cont_target]) ** 2
    )

    if target_distance < 10:
        cont_target = cont_target + 1
        if cont_target == n_points:
            cont_target = 0

    t2 = time.time()

    if (t2 - t1) < 1 / 300:
        time.sleep(1 / 300 - (t2 - t1))
