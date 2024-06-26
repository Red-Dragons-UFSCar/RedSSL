import socket
import struct
from communication.proto.ssl_vision_wrapper_pb2 import SSL_WrapperPacket

class Vision():
    def __init__(self, ip:str="224.0.0.1", port:int=10002, logger:bool=False, convert_coordinates:bool=True) -> None:
        '''
        Descrição:  
                Classe utilizada para comunicação com a interface de visão na qual recebe as mensagens
                protobuf e as converte em um dicionário
        Entradas:
                ip:                  String com o ip do server de visão
                port:                Porta de conexão do server de visão
                logger:              Flag que ativa o log de recebimento de mensagens no terminal. Por 
                                     padrão se mantém desativado
                convert_coordinates: Flag que ativa a conversão de mm para cm, com origem no vertice 
                                     inferior esquerdo. Por padrão se mantém ativado
        '''
        #  Network parameters
        self.ip = ip 
        self.port = port
        self.buffer_size = 65536  # Parametro que define o tamanho da palavra binária a ser recebida da rede

        # Logger control
        self.logger=logger

        # Field characteritics. 
        #TODO: Fazer isso mais genérico para conversão.
        self.length = 9000  # Comprimento do campo (mm)
        self.goal_depth = 180  # Profundidade do gol (mm)
        self.width = 6000  # Largura do campo (mm)

        self.convert_coordinates = convert_coordinates
        self.last_frame = []  # Variavel para armazenar o frame de detecção recebido da visão

        self._create_socket()
        self._start_frame()

    def _create_socket(self):
        '''
        Descrição:  
                Método responsável pela criação do socket de conexão com o servidor de visão
        '''
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack("=4sl", socket.inet_aton(self.ip), socket.INADDR_ANY))
        self.socket.bind((self.ip, self.port))
        # Opções para utilização em tempo real não-bloqueante
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def _start_frame(self):
        '''
        Descrição:  
                Método responsável pela criação do frame inicial de detecção
        '''
        robots_blue = []
        robots_yellow = []
        for i in range(0, 5):
            robots_blue.append( dict([ ("confidence", 0),
                                       ("robot_id", 0), 
                                       ("x", 0), 
                                       ("y", 0), 
                                       ("orientation", 0), 
                                       ("pixel_x", 0), 
                                       ("pixel_y", 0), 
                                       ("height", 0) ]) )
            robots_yellow.append( dict([ ("confidence", 0),
                                       ("robot_id", 0), 
                                       ("x", 0), 
                                       ("y", 0), 
                                       ("orientation", 0), 
                                       ("pixel_x", 0), 
                                       ("pixel_y", 0), 
                                       ("height", 0) ]) )
        ball = dict([ ("confidence", 0),
                      ("area", 0),
                      ("x", 0), 
                      ("y", 0), 
                      ("z", 0), 
                      ("pixel_x", 0), 
                      ("pixel_y", 0)])

        self.last_frame = dict([ ("frame_number", 0),
                                 ("t_capture", 0),
                                 ("t_sent", 0),
                                 ("camera_id", 0),
                                 ("ball", ball), 
                                 ("robots_yellow", robots_yellow), 
                                 ("robots_blue", robots_blue)])

    def _convert_parameters(self, msgRaw):
        '''
        Descrição:  
                Método responsável pela conversão da mensagem serializada protobuf em um 
                dicionário Python para utilização.
        Entradas:
                msgRaw: Mensagem serializada WrapperPacket recebida pelo socket
        '''
        msg = SSL_WrapperPacket()
        msg.ParseFromString(msgRaw)

        msg_robots_blue = msg.detection.robots_blue
        msg_robots_yellow = msg.detection.robots_yellow
        msg_ball = msg.detection.balls
        msg_geometry = msg.geometry

        self.data_ball_avaliable = len(msg_ball) > 0

        if self.convert_coordinates:
            correction_position_x = self.length/2
            correction_position_y = self.width/2
            for i in range(0, len(msg_robots_blue)):
                msg_robots_blue[i].x = (msg_robots_blue[i].x + correction_position_x)/10
                msg_robots_blue[i].y = (msg_robots_blue[i].y + correction_position_y)/10
            for i in range(0, len(msg_robots_yellow)):
                msg_robots_yellow[i].x = (msg_robots_yellow[i].x + correction_position_x)/10
                msg_robots_yellow[i].y = (msg_robots_yellow[i].y + correction_position_y)/10
            if self.data_ball_avaliable:
                msg_ball[0].x = (msg_ball[0].x + correction_position_x)/10
                msg_ball[0].y = (msg_ball[0].y + correction_position_y)/10

        robots_blue = []
        robots_yellow = []
        for i in range(0, len(msg_robots_blue)):
            robots_blue.append( dict([ ("confidence", msg_robots_blue[i].confidence),
                                       ("robot_id", msg_robots_blue[i].robot_id), 
                                       ("x", msg_robots_blue[i].x), 
                                       ("y", msg_robots_blue[i].y), 
                                       ("orientation", msg_robots_blue[i].orientation), 
                                       ("pixel_x", msg_robots_blue[i].pixel_x), 
                                       ("pixel_y", msg_robots_blue[i].pixel_y), 
                                       ("height", msg_robots_blue[i].height) ]) )
        for i in range(0, len(msg_robots_yellow)):
            robots_yellow.append( dict([ ("confidence", msg_robots_yellow[i].confidence),
                                         ("robot_id", msg_robots_yellow[i].robot_id), 
                                         ("x", msg_robots_yellow[i].x), 
                                         ("y", msg_robots_yellow[i].y), 
                                         ("orientation", msg_robots_yellow[i].orientation), 
                                         ("pixel_x", msg_robots_yellow[i].pixel_x), 
                                         ("pixel_y", msg_robots_yellow[i].pixel_y), 
                                         ("height", msg_robots_yellow[i].height) ]) )
        if self.data_ball_avaliable:
            ball = dict([ ("confidence", msg_ball[0].confidence),
                        ("area", msg_ball[0].area),
                        ("x", msg_ball[0].x), 
                        ("y", msg_ball[0].y), 
                        ("z", msg_ball[0].z), 
                        ("pixel_x", msg_ball[0].pixel_x), 
                        ("pixel_y", msg_ball[0].pixel_y)])
        else:
            ball = self.last_frame["ball"]
        
        self.last_frame = dict([ ("frame_number", msg.detection.frame_number),
                                 ("t_capture", msg.detection.t_capture),
                                 ("t_sent", msg.detection.t_sent),
                                 ("camera_id", msg.detection.camera_id),
                                 ("ball", ball), 
                                 ("robots_yellow", robots_yellow), 
                                 ("robots_blue", robots_blue)])

    def update(self):
        '''
        Descrição:  
                Método responsável pela atualização dos ultimos valores recebidos pelo socket
                realizando a conversão necessária. É necessário chamá-lo todas as vezes que
                novas informações são desejadas
        '''
        msgRaw = None
        try: 
            bytesAddressPair = self.socket.recvfrom(self.buffer_size)
            msgRaw = bytesAddressPair[0]
            self.error = 0

            if self.logger:
                print("[VISION] Recebido!")

            self._convert_parameters(msgRaw=msgRaw)

            
        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                self.error = 1
                if self.logger:
                    print("[VISION] Falha ao receber. Socket bloqueado.")
            else:
                self.error = 2
                print("[VISION] Socket error:", e)

    def get_last_frame(self):
        '''
        Descrição:  
                Obtem o ultimo frame recebido pelo socket
        Saída:
                last_frame: Ultimo frame de detecção (dicionário)
        '''
        return self.last_frame

if __name__ == '__main__':
    import time
    visao = Vision(ip="224.0.0.1", port=10002)

    while True:
        t1 = time.time()

        visao.update()
        frame = visao.get_last_frame()

        print("\n---START LOGGER---")
        print("Camera ID: ", frame["camera_id"])
        print("Robots blue: ")
        for robot in frame["robots_blue"]:
            print("Index: ", robot["robot_id"], end = ' ')
            print("X: ", robot["x"], end = ' ')
            print("Y: ", robot["y"], end = '\n')
        print("Robots yellow: ")
        for robot in frame["robots_yellow"]:
            print("Index: ", robot["robot_id"], end = ' ')
            print("X: ", robot["x"], end = ' ')
            print("Y: ", robot["y"], end = '\n')
        
        if (len(frame["ball"]) > 0):
            print("Ball: ")
            ball  = frame["ball"]
            print("X: ", int(ball["x"]), end = ' ')
            print("Y: ", ball["y"], end = '\n')

        t2 = time.time()

        if( (t2-t1) < 1/300 ):
            time.sleep(1/300 - (t2-t1))