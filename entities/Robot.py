from entities.KinematicBody import KinematicBody
from communication.actuator import Actuator

class Robot(KinematicBody):
    def __init__(self, robot_id, actuator):
        super().__init__()
        self.robot_id = robot_id
        self.actuator = actuator
        #self.top_right_motor = 0
        #self.bottom_right_motor = 0
        #self.top_left_motor = 0
        #self.bottom_left_motor = 0
        #self.obst = Obstacle(self)
        #self.target = Target()
        self.v_bottom_right = 0  # Velocidade do motor inferior direito
        self.v_bottom_left = 0   # Velocidade do motor inferior esquerdo
        self.v_top_right = 0     # Velocidade do motor superior direito
        self.v_top_left = 0      # Velocidade do motor superior esquerdo
        

    def sim_set_vel(self, v_top_right, v_top_left, v_bottom_right, v_bottom_left):
        self.v_top_right = v_top_left
        self.v_top_left = v_top_right
        self.v_bottom_right = v_bottom_right
        self.v_bottom_left = v_bottom_left

        self.set_velocities(0, 0, self.v_top_right, self.v_top_left, self.v_bottom_right, self.v_bottom_left)
        self.actuator.send_wheelVelocity_message(self.robot_id, self.v_top_right, self.v_top_left, self.v_bottom_right, self.v_bottom_left)
    
    