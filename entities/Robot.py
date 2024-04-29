from entities.KinematicBody import KinematicBody
from communication.actuator import Actuator

class Robot(KinematicBody):
    def __init__(self, robot_id, actuator):
        super().__init__()
        self.robot_id = robot_id
        self.actuator = actuator
        #self.topRightMotor = 0
        #self.bottomRightMotor = 0
        #self.topLeftMotor = 0
        #self.bottomLeftMotor = 0
        #self.obst = Obstacle(self)
        #self.target = Target()
        self.vbottomRight = 0  # Velocidade do motor inferior direito
        self.vbottomLeft = 0   # Velocidade do motor inferior esquerdo
        self.vtopRight = 0     # Velocidade do motor superior direito
        self.vtopLeft = 0      # Velocidade do motor superior esquerdo
        

    def sim_set_vel(self, vtopRight, vtopLeft, vbottomRight, vbottomLeft):
        self.vtopRight = vtopRight
        self.vtopLeft = vtopLeft
        self.vbottomRight = vbottomRight
        self.vbottomLeft = vbottomLeft

        self.set_velocities(0, 0, self.vtopRight, self.vtopLeft, self.vbottomRight, self.vbottomLeft)
        self.actuator.send_wheelVelocity_message(self.robot_id, self.vtopRight, self.vtopLeft, self.vbottomRight, self.vbottomLeft)
    