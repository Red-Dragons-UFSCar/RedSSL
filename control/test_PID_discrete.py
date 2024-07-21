from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from control.PID import PID
from control.PID_discrete import PID_discrete

import time
import numpy as np

# Objeto de visão
visao = Vision(ip="224.5.23.2", port=10020)

# Client de conexão de atuação do simulador
actuator = Actuator(team_port=10301)

# Robo azul 0
robot0 = Robot(robot_id=0, actuator=actuator)


# Controlador para a posição x
Kp_x = 6.551
Kd_x = 1.004 
Ki_x = 0
N_x = 1/0.01898
control_PID_x = PID_discrete(Kp_x, Kd_x, Ki_x, saturation=2, N=N_x)

# Controlador para a posição y 
Kp_y = 4.857
Kd_y = 1.077 
Ki_y = 0
N_y = 1/0.01805
control_PID_y = PID_discrete(Kp_y, Kd_y, Ki_y, saturation=2, N=N_y)


# Controlador para a rotação theta
Kp_theta = 1.5
Kd_theta = 0
Ki_theta = 0
control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=1)

# Alvos para cada eixo coordenado
x_target = [100, 100, 600, 600]
y_target = [500, 100, 100, 500]
theta_target = [-np.pi/2, 0, np.pi/2, np.pi]
n_points = len(x_target)
cont_target = 0


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
        control_PID_x.set_target(x_target[cont_target])
        control_PID_y.set_target(y_target[cont_target])
        control_PID_theta.set_target(theta_target[cont_target])

        control_PID_x.set_actual_value(robot0.get_coordinates().X)
        vx = control_PID_x.update()

        control_PID_y.set_actual_value(robot0.get_coordinates().Y)
        vy = control_PID_y.update()

        control_PID_theta.set_actual_value(robot0.get_coordinates().rotation)
        w = control_PID_theta.update_angular()

        cont = 0

    # Envio de velocidades para o robô
    robot0.sim_set_global_vel(vx, vy, w)

    print("Vx = ", vx)
    print("Vy = ", vy)
    print("w = ", w)
    print("---")

    target_distance = np.sqrt((robot0.get_coordinates().X - x_target[cont_target]) ** 2 +
                              (robot0.get_coordinates().Y - y_target[cont_target]) ** 2)
    
    # Atualização da lista de targets
    if target_distance < 10:
        cont_target = cont_target + 1
        if cont_target == n_points:
            cont_target = 0

    t2 = time.time()

    if( (t2-t1) < 1/300 ):
        time.sleep(1/300 - (t2-t1))

