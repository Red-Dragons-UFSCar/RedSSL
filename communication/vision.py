import socket
import struct
from commons.math import convert_coordinates
from communication.proto.ssl_vision_wrapper_pb2 import SSL_WrapperPacket


class Vision:
    def __init__(
        self,
        ip: str = "224.0.0.1",
        port: int = 10002,
        logger: bool = False,
        convert_coordinates: bool = True,
        is_right_side = False
    ) -> None:
        """
        Descrição:
            Classe utilizada para comunicação com a interface de visão, na qual recebe as mensagens
            protobuf e as converte em um dicionário.
        Entradas:
            ip:                  String com o IP do server de visão.
            port:                Porta de conexão do server de visão.
            logger:              Flag que ativa o log de recebimento de mensagens no terminal.
                                 Por padrão, se mantém ativado.
            convert_coordinates: Flag que ativa a conversão de mm para cm, com origem no vértice
                                 inferior esquerdo. Por padrão, se mantém ativado.
        """
        # Parâmetros de rede
        self.ip = ip
        self.port = port
        self.buffer_size = 4096  # Tamanho do buffer ajustado para melhor desempenho

        # Controle de logging
        self.logger = logger

        # Características do campo
        self.length = 4500  # Comprimento do campo (mm)
        self.width = 3000  # Largura do campo (mm)

        # Configuração de conversão de coordenadas
        self.convert_coordinates = convert_coordinates
        self.is_right_side = is_right_side
        self.last_frame = self._initialize_frame()  # Inicializa o frame vazio

        # Criação do socket de conexão
        self._create_socket()

        # Frame numbers dos últimos frames recebidos
        self.before_last_frame_frame_number = 0 # Penúltimo
        self.last_frame_frame_number = 0        # Último

        # Dados do frame que já foram recebidos
        self.validated_data = {"ball": [],
                               "robots_yellow": [],
                               "robots_blue": []}

    def _create_socket(self):
        """
        Descrição:
            Método responsável pela criação do socket de conexão com o servidor de visão.
        """
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.socket.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            struct.pack("=4sl", socket.inet_aton(self.ip), socket.INADDR_ANY),
        )
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False)
        self.socket.settimeout(0.0)

    def _initialize_frame(self):
        """
        Descrição:
            Método responsável pela criação do frame inicial de detecção.
        """
        robots = [
            {
                "confidence": 0,
                "robot_id": 0,
                "x": 0,
                "y": 0,
                "orientation": 0,
                "pixel_x": 0,
                "pixel_y": 0,
                "height": 0,
            }
            for _ in range(5)
        ]
        ball = {
            "confidence": 0,
            "area": 0,
            "x": 0,
            "y": 0,
            "z": 0,
            "pixel_x": 0,
            "pixel_y": 0,
        }

        return {
            "frame_number": 0,
            "t_capture": 0,
            "t_sent": 0,
            "ball": ball,
            "robots_yellow": robots,
            "robots_blue": robots,
        }

    def _convert_parameters(self, msgRaw):
        """
        Descrição:
            Método responsável pela conversão da mensagem serializada protobuf em um
            dicionário Python para utilização.
        Entradas:
            msgRaw: Mensagem serializada WrapperPacket recebida pelo socket.
        """
        msg = SSL_WrapperPacket()
        msg.ParseFromString(msgRaw)

        robots_blue = msg.detection.robots_blue
        robots_yellow = msg.detection.robots_yellow
        balls = msg.detection.balls
        msg_geometry = msg.geometry


        # Conversão de coordenadas, se necessário
        if self.convert_coordinates:
            convert_coordinates(list(robots_blue), list(robots_yellow), list(balls), self.length, self.width, self.is_right_side)

        # Atualiza o frame com os novos dados recebidos
        ball = (
            {
                "confidence": balls[0].confidence,
                "area": balls[0].area,
                "x": balls[0].x,
                "y": balls[0].y,
                "z": balls[0].z,
                "pixel_x": balls[0].pixel_x,
                "pixel_y": balls[0].pixel_y,
            }
            if balls
            else self.last_frame["ball"]
        )
        robots_blue = [
            {
                "confidence": robot.confidence,
                "robot_id": robot.robot_id,
                "x": robot.x,
                "y": robot.y,
                "orientation": robot.orientation,
                "pixel_x": robot.pixel_x,
                "pixel_y": robot.pixel_y,
                "height": robot.height,
            }
            for robot in robots_blue
        ]
        robots_yellow = [
            {
                "confidence": robot.confidence,
                "robot_id": robot.robot_id,
                "x": robot.x,
                "y": robot.y,
                "orientation": robot.orientation,
                "pixel_x": robot.pixel_x,
                "pixel_y": robot.pixel_y,
                "height": robot.height,
            }
            for robot in robots_yellow
        ]

        self.last_frame = {
            "frame_number": msg.detection.frame_number,
            "t_capture": msg.detection.t_capture,
            "t_sent": msg.detection.t_sent,
            "ball": ball,
            "robots_yellow": robots_yellow,
            "robots_blue": robots_blue,
        }
    
    def _convert_parameters2(self, msgRaw):
        """
        Descrição:
            Método responsável pela conversão da mensagem serializada protobuf em um
            dicionário Python para utilização.
        Entradas:
            msgRaw: Mensagem serializada WrapperPacket recebida pelo socket.
        """
        msg = SSL_WrapperPacket()
        msg.ParseFromString(msgRaw)

        robots_blue = msg.detection.robots_blue
        robots_yellow = msg.detection.robots_yellow
        balls = msg.detection.balls
        msg_geometry = msg.geometry

        # Conversão de coordenadas, se necessário
        if self.convert_coordinates:
            convert_coordinates(list(robots_blue), list(robots_yellow), list(balls), self.length, self.width, self.is_right_side)
        
        # Atualização dos últimos frame numbers
        self.before_last_frame_frame_number = self.last_frame_frame_number
        self.last_frame_frame_number = msg.detection.frame_number

        # Verifica se houve mudança do frame number entre os frames recebidos
        # Reseta os dados validados para processar novos dados
        if not self.before_last_frame_frame_number == self.last_frame_frame_number:
            self.validated_data = {"ball": [],
                                   "robots_yellow": [],
                                   "robots_blue": []}
        
        validated_data = self.validated_data

        # Atualiza o frame com os novos dados recebidos
        if balls and not validated_data["ball"]:
            ball = (
                {
                    "confidence": balls[0].confidence,
                    "area": balls[0].area,
                    "x": balls[0].x,
                    "y": balls[0].y,
                    "z": balls[0].z,
                    "pixel_x": balls[0].pixel_x,
                    "pixel_y": balls[0].pixel_y,
                }
            )
            validated_data["ball"] = True
        else:
            ball = ()
        
        robots_blue_validated = []
        for robot in robots_blue:
            if not robot.robot_id in validated_data["robots_blue"]:
                robots_blue_validated.append(
                    {
                        "confidence": robot.confidence,
                        "robot_id": robot.robot_id,
                        "x": robot.x,
                        "y": robot.y,
                        "orientation": robot.orientation,
                        "pixel_x": robot.pixel_x,
                        "pixel_y": robot.pixel_y,
                        "height": robot.height,
                    }
                )
                validated_data["robots_blue"].append(robot.robot_id)
        
        robots_yellow_validated = []
        for robot in robots_yellow:
            if not robot.robot_id in validated_data["robots_yellow"]:
                robots_yellow_validated.append(
                    {
                        "confidence": robot.confidence,
                        "robot_id": robot.robot_id,
                        "x": robot.x,
                        "y": robot.y,
                        "orientation": robot.orientation,
                        "pixel_x": robot.pixel_x,
                        "pixel_y": robot.pixel_y,
                        "height": robot.height,
                    }
                )
                validated_data["robots_yellow"].append(robot.robot_id)

        self.last_frame = {
            "frame_number": msg.detection.frame_number,
            "t_capture": msg.detection.t_capture,
            "t_sent": msg.detection.t_sent,
            "ball": ball,
            "robots_yellow": robots_yellow_validated,
            "robots_blue": robots_blue_validated,
        }

    def update(self):
        """
        Descrição:
            Método responsável pela atualização dos últimos valores recebidos pelo socket,
            realizando a conversão necessária. É necessário chamá-lo todas as vezes que
            novas informações são desejadas.
        """
        try:
            self.reset_last_frame()
            msgRaw, _ = self.socket.recvfrom(self.buffer_size)
            self._convert_parameters2(msgRaw=msgRaw)

            if self.logger:
                print("[VISION] Dados recebidos e convertidos com sucesso.")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[VISION] Falha ao receber. Socket bloqueado.")
            else:
                print("[VISION] Erro no socket:", e)

    def get_last_frame(self):
        """
        Descrição:
            Obtém o último frame recebido pelo socket.
        Saída:
            last_frame: Último frame de detecção (dicionário).
        """
        return self.last_frame
    
    def reset_last_frame(self):
        """
        Descrição:
            Reseta o último frame recebido pelo socket.
        """

        self.last_frame = {
            "frame_number": 0,
            "t_capture": 0,
            "t_sent": 0,
            "ball": [],
            "robots_yellow": [],
            "robots_blue": [],
        }

if __name__ == "__main__":
    import time

    visao = Vision(ip="224.5.23.2", port=10020)

    while True:
        t1 = time.time()

        visao.update()
        frame = visao.get_last_frame()

        print("\n---START LOGGER---")
        print("Robots blue: ")
        for robot in frame["robots_blue"]:
            print(f"Index: {robot['robot_id']} X: {robot['x']} Y: {robot['y']}")
        print("Robots yellow: ")
        for robot in frame["robots_yellow"]:
            print(f"Index: {robot['robot_id']} X: {robot['x']} Y: {robot['y']}")

        if frame["ball"]["confidence"] > 0:  # Verifica se há dados válidos da bola.
            print("Ball: X: ", int(frame["ball"]["x"]), " Y: ", frame["ball"]["y"])

        t2 = time.time()

        # Controla a taxa de atualização para 300Hz.
        if (t2 - t1) < 1 / 300:
            time.sleep(1 / 300 - (t2 - t1))
