from entities.KinematicBody import KinematicBody
from communication.actuator import Actuator
from entities.Obstacle import ObstacleMap
from entities.Target import Target
from control.PID import PID
from control.PID_discrete import PIDDiscrete
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
        '''
        # Parâmetros PID
        KP_X = 6.551
        KD_X = 0.1
        KI_X = 0
        N_X = 1 / 0.01898
        KP_Y = 4.857
        KD_Y = 0.1
        KI_Y = 0
        N_Y = 1 / 0.01805
        KP_THETA = 3
        KD_THETA = 0
        KI_THETA = 0
        
        

        ''' Controlador PID original fisico
        KP_X = 4.5
        KD_X = 0
        KI_X = 0
        N_X = 30
        KP_Y = 4.5
        KD_Y = 0
        KI_Y = 0
        N_Y = 30
        KP_THETA = 2
        KD_THETA = 0
        KI_THETA = 0
        '''

        ''' FISICO ATUAL
        KP_X = 25
        KD_X = 0
        KI_X = 15
        N_X = 30
        KP_Y = 25
        KD_Y = 0
        KI_Y = 15
        N_Y = 30
        KP_THETA = 5
        KD_THETA = 0
        KI_THETA = 0
        '''
        

        ''' SIMULACAO 2
        KP_X = 13
        KD_X = 0
        KI_X = 50
        N_X = 30
        KP_Y = 15
        KD_Y = 0
        KI_Y = 50
        N_Y = 30
        KP_THETA = 7
        KD_THETA = 0
        KI_THETA = 0
        '''
        
        

        # Controladores PID
        self.control_PID_x = PIDDiscrete(KP_X, KD_X, KI_X, saturation=2, N=N_X)
        self.control_PID_y = PIDDiscrete(KP_Y, KD_Y, KI_Y, saturation=2, N=N_Y)
        #self.control_PID_theta = PID(KP_THETA, KD_THETA, KI_THETA, saturation=5)
        self.control_PID_theta = PID(KP_THETA, KD_THETA, KI_THETA, saturation=5)

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