import socket
import struct
from .proto import ssl_simulation_robot_control_pb2 as pb2



class Actuator():
    def __init__(self, ip:str='localhost', port:int=10000,team_port:int=10302, logger:bool=True) -> None:
        """
        Descrição:
                Classe para interação com um atuador em um sistema de controle ou automação.

        Entradas:
                ip:             Endereço IP para comunicação. Padrão é 'localhost'.
                port:           Porta de comunicação. Padrão é 10000.
                team_port:      Porta da equipe. Padrão é 10302.
                logger:         Flag que ativa o log de recebimento de mensagens no terminal. Por 
                                padrão se mantém desativado
        """
        # Newtork parameters
        self.ip = ip
        self.port = port
        self.team_port = team_port
        self.buffer_sice = 65536 # Parametro que define o tamanho da palavra binária a ser recebida da rede
 
        # Logger control
        self.logger = logger

        # Create socket
        self._create_socket()



    def _create_socket(self):
        '''
        Descrição:  
                Método responsável pela criação do socket de conexão com o servidor de visão
        '''
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    
    def send_socket(self, data):
        '''
        Descrição:  
                Método responsável pelo envio da mensagem para o simulador
        '''
        try:
            self.socket.sendto(data, (self.ip, self.team_port))
            if self.logger: print("[Actuator] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[Actuator] Falha ao enviar. Socket bloqueado")
            else:
                print("[Actuator] Socket error:", e)



    def send_wheelVelocity_message(self, index, wheel_bl, wheel_br, wheel_fl, wheel_fr):
        '''
        Descrição:  
                Método responsável pelo envio das velocidades diretamente para as rodas do robô
        '''
        self.robot_id = index
        self.wheel_bl = wheel_bl
        self.wheel_br = wheel_br
        self.wheel_fl = wheel_fl
        self.wheel_fr = wheel_fr



        # Crie uma mensagem RobotControl
        robot_control = pb2.RobotControl()

        #Crie uma mensagem RobotCommand
        robot_command = robot_control.robot_commands.add()
        robot_command.id = self.robot_id

        #Crie uma mensagem MoveWheelVelocity
        move_command = pb2.MoveWheelVelocity()
        move_command.front_right = self.wheel_fr
        move_command.back_right = self.wheel_fl
        move_command.back_left = self.wheel_br
        move_command.front_left = self.wheel_bl

        # Atribua a mensagem MoveWheelVelocity ao campo move_command da mensagem RobotCommand
        robot_command.move_command.wheel_velocity.CopyFrom(move_command)


        self.send_socket(robot_control.SerializeToString())
        


    def send_globalVelocity_message(self, index,velocity_x, velocity_y, angular):
        '''
        Descrição:  
                Método responsável pelo envio da velocidade global do robô
        '''
        self.robot_id = index
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.angular = angular
        

        # Crie uma mensagem RobotControl
        robot_control = pb2.RobotControl()

        #Crie uma mensagem RobotCommand
        robot_command = robot_control.robot_commands.add()
        robot_command.id = self.robot_id

        #Crie uma mensagem MoveGlobalVelocity
        move_command = pb2.MoveGlobalVelocity()
        move_command.x = self.velocity_x
        move_command.y = self.velocity_y
        move_command.angular = self.angular

        # Atribua a mensagem MoveGlobalVelocity ao campo move_command da mensagem RobotCommand
        robot_command.move_command.global_velocity.CopyFrom(move_command)


        self.send_socket(robot_control.SerializeToString())

    def send_localVelocity_message(self, index, forward, left, angular):
        '''
        Descrição:  
                Método responsável pelo envio da velocidade local do robô
        '''
        self.robot_id = index
        self.forward = forward
        self.left = left
        self.angular = angular
        

        # Crie uma mensagem RobotControl
        robot_control = pb2.RobotControl()

        #Crie uma mensagem RobotCommand
        robot_command = robot_control.robot_commands.add()
        robot_command.id = self.robot_id

        #Crie uma mensagem MoveLocalVelocity
        move_command = pb2.MoveLocalVelocity()
        move_command.forward = self.forward
        move_command.left = self.left
        move_command.angular = self.angular

        # Atribua a mensagem MoveLocalVelocity ao campo move_command da mensagem RobotCommand
        robot_command.move_command.local_velocity.CopyFrom(move_command)


        self.send_socket(robot_control.SerializeToString())
