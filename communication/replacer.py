import socket
import numpy as np

from commons.math import rotate_vector
from communication.proto.grSim_Replacement_pb2 import grSim_BallReplacement, grSim_Replacement, grSim_RobotReplacement

class Replacer():
    def __init__(self, ip:str='8.8.8.8', port:int=10000, team_port:int=10301, logger:bool=False) -> None:
        """
        Descrição:
                Classe para interação com um atuador em um sistema de controle ou automação.

        Entradas:
                ip:             Endereço IP para comunicação. Padrão é 'localhost'.
                port:           Porta de comunicação. Padrão é 10000.
                team_port:      Porta da equipe. Padrão é 10301.
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
        # self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    
    def send_socket(self, data):
        '''
        Descrição:  
                Método responsável pelo envio da mensagem para o simulador
        '''
        try:
            self.socket.sendto(data, (self.ip, self.team_port))
            if self.logger: print("[Replacer] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[Replacer] Falha ao enviar. Socket bloqueado")
            else:
                print("[Replacer] Socket error:", e)

    
    def send_robotReplacement_message(self, x, y, dir, id, yellowteam, turnon):
        
        self.x = x
        self.y = y
        self.dir = dir
        self.id = id
        self.yellowteam = yellowteam
        self.turnon = turnon

        replacement = grSim_Replacement()

        # ball_replacement = replacement.ball

        # ball_replacement.x = 0
        # ball_replacement.y = 0
        # ball_replacement.vx = 0
        # ball_replacement.vy = 0

        robot_replacement = replacement.robots.add()

        robot_replacement.x = self.x
        robot_replacement.y = self.y
        robot_replacement.dir = self.dir
        robot_replacement.id = self.id
        robot_replacement.yellowteam = self.yellowteam
        robot_replacement.turnon = self.turnon

        # print(ball_replacement)
        # print(ball_replacement.SerializeToString())
        # print(robot_replacement.SerializeToString())
        print(replacement)
        # print(replacement.SerializeToString())

        self.send_socket(replacement.SerializeToString())


    def send_ballReplacement_message(self, x, y, vx, vy):

        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        replacement = grSim_Replacement()
        
        ball_replacement = replacement.ball

        ball_replacement.x = x
        ball_replacement.y = y
        ball_replacement.vx = vx
        ball_replacement.vy = vy

        self.send_socket(replacement.SerializeToString())


    def send_replacement_message(self):
        pass


if __name__ == '__main__':
    import time
    replacer = Replacer(team_port=10300, logger=True)

    # replacer.send_robotReplacement_message(1, 1, 1, 1, 0, 1)

    for i in range(10):
        # replacer.send_robotReplacement_message(0, 0, 0, 0, 0, 1)
        time.sleep(1)
        print(i)
        for j in range(3):
            replacer.send_robotReplacement_message(2, 2, 2, j, 0, 1)

    from entities.Robot import Robot
    from actuator import Actuator
    import json

    # with open('constants/network.json', 'r') as file:
    #     network = json.load(file)

    # actuator = Actuator(ip=network['command']['ip'], team_port=network['command']['port'])
    actuator = Actuator(ip='localhost', team_port=10301)
    robot0 = Robot(robot_id=0, actuator=actuator)

    robot0.vx = 20
    robot0.vy = 20
    robot0.w = 2

    for i in range(10):
        # replacer.send_robotReplacement_message(0, 0, 0, 0, 0, 1)
        time.sleep(1)
        print(i)
        actuator.send_wheel_from_global(robot0, robot0.vx, robot0.vy, robot0.w)


    # while True:
    #     t1 = time.time()
    #     replacer.send_robotReplacement_message(0, 0, 0, 0, 0, 0)
    #     t2 = time.time()

    #     print('a')

    #     if( (t2-t1) < 1/300 ):
    #         time.sleep(1/300 - (t2-t1))