from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from control.PID import PID
from behavior.skills import *
import time
import numpy as np


# Objeto de visão
visao = Vision(ip="224.5.23.2", port=10020)

# Client de conexão de atuação do simulador
actuator = Actuator(team_port=10301)

# Robôs azuis (o primeiro é o robô controlado, os outros são obstáculos)
robot0 = Robot(
    robot_id=0,
    actuator=actuator,
)

robot1 = Robot(robot_id=1, actuator=None)
robot2 = Robot(robot_id=2, actuator=None)

robots = [robot0, robot1, robot2]


# Robôs amarelos (considerados como obstáculos)
enemy_robot0 = Robot(robot_id=0, actuator=None)
enemy_robot1 = Robot(robot_id=1, actuator=None)


enemy_robots = [enemy_robot0, enemy_robot1]


# Contador para garantir a leitura dos dados da câmera
cont = 0
cont_target = 0


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

        vx, vy, w = go_to_point(robot0, 100, 0, robots, enemy_robots)
        robot0.apply_velocity(vx, vy, w)
        cont = 0

    t2 = time.time()

    if (t2 - t1) < 1 / 300:
        time.sleep(1 / 300 - (t2 - t1))
