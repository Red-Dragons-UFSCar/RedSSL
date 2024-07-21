from entities.KinematicBody import KinematicBody
from communication.actuator import Actuator
from entities.Target import Target
from entities.Obstacle import Obstacle

import numpy as np


class Robot(KinematicBody):
    """Stores data about robots in the game."""

    def __init__(self, robot_id, actuator):
        super().__init__()
        self.robot_id = robot_id
        self.actuator = actuator
        # self.top_right_motor = 0
        # self.bottom_right_motor = 0
        # self.top_left_motor = 0
        # self.bottom_left_motor = 0
        # self.obst = Obstacle(self)
        self.cont_target = 0  # Adicionado cont_target como atributo do robô
        self.target = Target()
        self.obst = Obstacle(self)
        self.v_bottom_right = 0  # Velocidade do motor inferior direito
        self.v_bottom_left = 0  # Velocidade do motor inferior esquerdo
        self.v_top_right = 0  # Velocidade do motor superior direito
        self.v_top_left = 0  # Velocidade do motor superior esquerdo

    def sim_set_vel(self, v_top_right, v_top_left, v_bottom_right, v_bottom_left):
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
        self.actuator.send_wheelVelocity_message(
            self.robot_id,
            self.v_top_right,
            self.v_top_left,
            self.v_bottom_right,
            self.v_bottom_left,
        )

    def sim_set_global_vel(self, velocity_x, velocity_y, angular):
        self.actuator.send_globalVelocity_message(
            self.robot_id, velocity_x, velocity_y, angular
        )

    def set_target(self, target):
        self.target = target

    def target_reached(self):
        # Implemente sua lógica para verificar se o robô alcançou o alvo aqui
        if self.target is None:
            return False
        current_position = np.array(
            [self.get_coordinates().X, self.get_coordinates().Y]
        )
        target_position = np.array([self.target.x, self.target.y])
        distance_to_target = np.linalg.norm(current_position - target_position)
        return distance_to_target < 10
