from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from control.PID import PID

import time
import numpy as np

# Objeto de visão
visao = Vision(ip="224.5.23.2", port=10020)

# Client de conexão de atuação do simulador
actuator = Actuator(team_port=10301)

# Robo azul 0
robot0 = Robot(robot_id=0, actuator=actuator)


# Controlador para a posição x
Kp_x = 1/100 
Kd_x = -0.0631/100 
Ki_x = 0
control_PID_x = PID(Kp_x, Kd_x, Ki_x, saturation=2)


# Controlador para a posição y
Kp_y = 1/100 
Kd_y = -0.0169/100 
Ki_y = 0
control_PID_y = PID(Kp_y, Kd_y, Ki_y, saturation=2)


# Controlador para a rotação theta
Kp_theta = 0.6
Kd_theta = 0 
Ki_theta = 0
control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=1)


# Alvos para cada eixo coordenado
control_PID_x.set_target(400)
control_PID_y.set_target(300)
control_PID_theta.set_target(-np.pi/2)


# Contador para garantir a leitura dos dados da camera
cont = 0

# Sinais de controle
vx = 0
vy = 0
w = 0

while True:
    t1 = time.time()

    # Recebimento dos dados da visão
    visao.update()
    frame = visao.get_last_frame()

    # Detecção dos robôs azuis
    for detection in frame["robots_blue"]:
        if detection["robot_id"] == 0:
            x_pos = detection["x"]
            y_pos = detection["y"]
            theta = detection["orientation"]
            robot0.set_coordinates(x_pos, y_pos, theta)

    cont = cont + 1

    # Se foi recebido ao menos 5 frames de visão, realizar o controle
    # Garantia de recebimento de todos os dados da visão
    # (sim, isso é uma gambiarra, é apenas para teste)
    if cont==5:
        control_PID_x.set_actual_value(robot0.get_coordinates().X)
        vx = control_PID_x.update()

        control_PID_y.set_actual_value(robot0.get_coordinates().Y)
        vy = control_PID_y.update()

        control_PID_theta.set_actual_value(robot0.get_coordinates().rotation)
        w = control_PID_theta.update()

        cont = 0

    # Envio de velocidades para o robô
    robot0.sim_set_global_vel(vx, vy, w)

    print("Vx = ", vx)
    print("Vy = ", vy)
    print("w = ", w)
    print("---")

    t2 = time.time()

    if( (t2-t1) < 1/300 ):
        time.sleep(1/300 - (t2-t1))

