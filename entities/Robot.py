from entities.KinematicBody import KinematicBody
from communication.actuator import Actuator
from entities.Obstacle import Obstacle
from entities.Target import Target
from control.PID import PID
from control.PID_discrete import PID_discrete
import numpy as np


class Robot(KinematicBody):
    """Armazena dados sobre os robôs no jogo."""

    def __init__(self, robot_id: int, actuator: Actuator):
        super().__init__()
        self.robot_id = robot_id
        self.actuator = actuator
        self.obst = Obstacle(self)
        self.cont_target = 0  # Adicionado cont_target como atributo do robô
        self.target = Target()
        self.v_bottom_right = 0  # Velocidade do motor inferior direito
        self.v_bottom_left = 0  # Velocidade do motor inferior esquerdo
        self.v_top_right = 0  # Velocidade do motor superior direito
        self.v_top_left = 0  # Velocidade do motor superior esquerdo
        self.vx = 0  # Velocidade X do robô
        self.vy = 0  # Velocidade Y do robô
        self.w = 0  # Velocidade angular do robô

        # Parâmetros PID
        Kp_x = 6.551
        Kd_x = 2.5
        Ki_x = 1.5
        N_x = 1 / 0.01898
        Kp_y = 4.857
        Kd_y = 1.8
        Ki_y = 1
        N_y = 1 / 0.01805
        Kp_theta = 5
        Kd_theta = 0
        Ki_theta = 0

        # Controladores PID
        self.control_PID_x = PID_discrete(Kp_x, Kd_x, Ki_x, saturation=1, N=N_x)
        self.control_PID_y = PID_discrete(Kp_y, Kd_y, Ki_y, saturation=1, N=N_y)
        self.control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=3)

    def sim_set_vel(self, v_top_right, v_top_left, v_bottom_right, v_bottom_left):
        # Define as velocidades dos motores
        self.v_top_right = v_top_left
        self.v_top_left = v_top_right
        self.v_bottom_right = v_bottom_right
        self.v_bottom_left = v_bottom_left

        self.set_velocities(
            0,
            0,
            self.v_top_right,
            self.v_top_left,
            self.v_bottom_right,
            self.v_bottom_left,
        )
        # Envia as velocidades das rodas para o atuador
        self.actuator.send_wheelVelocity_message(
            self.robot_id,
            self.v_top_right,
            self.v_top_left,
            self.v_bottom_right,
            self.v_bottom_left,
        )

    def sim_set_global_vel(self, velocity_x, velocity_y, angular):
        # Envia as velocidades globais para o atuador
        self.actuator.send_globalVelocity_message(
            self.robot_id, velocity_x, velocity_y, angular
        )

    def set_target(self, target):
        # Define o alvo do robô
        self.target = target

    def target_reached(self):
        # Verifica se o robô alcançou o alvo
        if self.target is None:
            return False
        current_position = np.array(
            [self.get_coordinates().X, self.get_coordinates().Y]
        )
        target_position = np.array(
            [self.target.get_coordinates().X, self.target.get_coordinates().Y]
        )
        distance_to_target = np.linalg.norm(current_position - target_position)
        return distance_to_target < 10

    def set_robot_velocity(self, target_velocity_x, target_velocity_y, target_angular):
        # Define as velocidades alvo nos controladores PID
        self.control_PID_x.set_target(target_velocity_x)
        self.control_PID_y.set_target(target_velocity_y)
        self.control_PID_theta.set_target(target_angular)

        # Calcula as velocidades do robô usando os controladores PID
        self.control_PID_x.set_actual_value(self.get_coordinates().X)
        self.vx = self.control_PID_x.update()

        self.control_PID_y.set_actual_value(self.get_coordinates().Y)
        self.vy = self.control_PID_y.update()

        self.control_PID_theta.set_actual_value(self.get_coordinates().rotation)
        self.w = self.control_PID_theta.update_angular()

        # Retorna as velocidades calculadas
        return self.vx, self.vy, self.w
