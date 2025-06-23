from entities.KinematicBody import KinematicBody
from communication.actuator import Actuator
from entities.Obstacle import ObstacleMap
from entities.Target import Target
from control.PID import PID
from control.PID_discrete import PID_discrete
import numpy as np


class Robot(KinematicBody):
    """Armazena dados sobre os robôs no jogo."""

    def __init__(self, robot_id: int, actuator: Actuator, vision_id:int=None):
        super().__init__()
        self.robot_id = robot_id
        self.vision_id = vision_id
        self.actuator = actuator
        self.map_obstacle = ObstacleMap()
        self.cont_target = 0  # Adicionado cont_target como atributo do robô
        self.target = Target()
        self.v_bottom_right = 0  # Velocidade do motor inferior direito
        self.v_bottom_left = 0  # Velocidade do motor inferior esquerdo
        self.v_top_right = 0  # Velocidade do motor superior direito
        self.v_top_left = 0  # Velocidade do motor superior esquerdo
        self.vx = 0  # Velocidade X do robô
        self.vy = 0  # Velocidade Y do robô
        self.w = 0  # Velocidade angular do robô

        # Valores máximos do robô móvel
        self.v_max = 1.0  # Velocidade linear máxima em módulo

        '''
        # Parâmetros PID
        Kp_x = 6.551
        Kd_x = 0.1
        Ki_x = 0
        N_x = 1 / 0.01898
        Kp_y = 4.857
        Kd_y = 0.1
        Ki_y = 0
        N_y = 1 / 0.01805
        Kp_theta = 3
        Kd_theta = 0
        Ki_theta = 0
        '''

        # Parâmetros PID simulado - 2
        Kp_x = 1
        Kd_x = 2.5
        Ki_x = 0
        N_x = 1 / 0.01898
        Kp_y = 4.857
        Kd_y = 0.1
        Ki_y = 0
        N_y = 1 / 0.01805
        Kp_theta = 3
        Kd_theta = 0
        Ki_theta = 0


        ''' Controlador PID original fisico
        Kp_x = 4.5
        Kd_x = 0
        Ki_x = 0
        N_x = 30
        Kp_y = 4.5
        Kd_y = 0
        Ki_y = 0
        N_y = 30
        Kp_theta = 2
        Kd_theta = 0
        Ki_theta = 0
        '''

        ''' FISICO ATUAL'''
         

        Kp_x = 25
        Kd_x = 0
        Ki_x = 15
        N_x = 30
        Kp_y = 25
        Kd_y = 0
        Ki_y = 15
        N_y = 30
        Kp_theta = 5
        Kd_theta = 0
        Ki_theta = 0
       

        ''' SIMULACAO 2
        Kp_x = 13
        Kd_x = 0
        Ki_x = 50
        N_x = 30
        Kp_y = 15
        Kd_y = 0
        Ki_y = 50
        N_y = 30
        Kp_theta = 7
        Kd_theta = 0
        Ki_theta = 0
        '''
        
        

        # Controladores PID
        self.control_PID_x = PID_discrete(Kp_x, Kd_x, Ki_x, saturation=2, N=N_x)
        self.control_PID_y = PID_discrete(Kp_y, Kd_y, Ki_y, saturation=2, N=N_y)
        #self.control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=5)
        self.control_PID_theta = PID(Kp_theta, Kd_theta, Ki_theta, saturation=5)

        # Parâmetros construtivos do robo
        # Todos esses parâmetros do grSim estão em grSim/config/Parsian.ini
        '''
        # Simulador
        self.phi1 = 60 * np.pi/180
        self.phi2 = 135 * np.pi/180
        self.phi3 = 225 * np.pi/180
        self.phi4 = 300 * np.pi/180
        self.robot_radius = 0.09
        self.wheel_radius = 0.027
        '''
        # Real
        self.phi1 = 55 * np.pi/180
        self.phi2 = 125 * np.pi/180
        self.phi3 = 235 * np.pi/180
        self.phi4 = 305 * np.pi/180
        self.robot_radius = 0.09
        self.wheel_radius = 0.036

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

    def target_reached(self, treshold=10):
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
        return distance_to_target < treshold
    
    def xtarget_reached(self, xTreshold=10):
        if self.target is None:
            return False
        xDistance_to_target = abs(self.get_coordinates().X - self.target.get_coordinates().X)
        return xDistance_to_target < xTreshold
    
    def ytarget_reached(self, yTreshold=10):
        if self.target is None:
            return False
        yDistance_to_target = abs(self.get_coordinates().Y - self.target.get_coordinates().Y)
        return yDistance_to_target < yTreshold

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