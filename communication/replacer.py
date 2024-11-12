import socket
import numpy as np

from commons.math import rotate_vector
from communication.proto.grSim_Commands_pb2 import grSim_Commands, grSim_Robot_Command
from communication.proto.grSim_Replacement_pb2 import grSim_BallReplacement, grSim_Replacement, grSim_RobotReplacement
from communication.proto.grSim_Packet_pb2 import grSim_Packet

class Replacer():
    def __init__(self, ip:str='localhost', port:int=10000, team_port:int=20011, logger:bool=False) -> None:
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

        packet = grSim_Packet()

        replacement = packet.replacement

        robot_replacement = replacement.robots.add()

        robot_replacement.x = self.x
        robot_replacement.y = self.y
        robot_replacement.dir = self.dir
        robot_replacement.id = self.id
        robot_replacement.yellowteam = self.yellowteam
        robot_replacement.turnon = self.turnon

        self.send_socket(packet.SerializeToString())


    def send_ballReplacement_message(self, x, y, vx, vy):

        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        packet = grSim_Packet()

        replacement = packet.replacement
        
        ball_replacement = replacement.ball

        ball_replacement.x = x
        ball_replacement.y = y
        ball_replacement.vx = vx
        ball_replacement.vy = vy

        self.send_socket(packet.SerializeToString())


if __name__ == '__main__':
    import time
    replacer = Replacer()

    ball_x = [-0.5, 0.5, 0.5 , -0.5]
    ball_y = [0.5 , 0.5, -0.5, -0.5]
    ball_cont = 0

    robot_x = [[-1.25, 1.25, 1.25, -1.25],
               [-1   , 1   , 1   , -1   ],
               [-0.75, 0.75, 0.75, -0.75]]
    robot_y = [[1.25, 1.25, -1.25, -1.25],
               [1   , 1   , -1   , -1   ],
               [0.75, 0.75, -0.75, -0.75]]
    robot_dir = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    robot_count = 0

    while True:
        t1 = time.time()

        replacer.send_ballReplacement_message(ball_x[ball_cont], ball_y[ball_cont], 0, 0)
        for i in range(3):
            replacer.send_robotReplacement_message(robot_x[i][robot_count], robot_y[i][robot_count], robot_dir[i][robot_count], i, 0, 1)

        ball_cont = (ball_cont + 1) % 4
        robot_count = (robot_count + 1) % 4
        time.sleep(0.5)

        t2 = time.time()

        if( (t2-t1) < 1/300 ):
            time.sleep(1/300 - (t2-t1))