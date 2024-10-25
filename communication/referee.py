import socket
from communication.proto.ssl_gc_referee_message_pb2 import Referee


class RefereeCommunication:
    REFEREE_IP = "224.5.23.1"
    REFEREE_PORT = 10003

    def __init__(self, field):
        """
        Inicializa o socket para receber mensagens do árbitro e define o estado inicial.
        """
        self.referee_socket = self._init_referee_socket()
        self.referee_state = None
        self.field = field

    def _init_referee_socket(self):
        """
        Configura e inicializa o socket para comunicação com o árbitro.
        """
        referee_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        referee_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        referee_socket.bind((self.REFEREE_IP, self.REFEREE_PORT))
        mreq = socket.inet_aton(self.REFEREE_IP) + socket.inet_aton("0.0.0.0")
        referee_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        referee_socket.setblocking(False)
        return referee_socket

    def get_referee_message(self):
        """
        Recebe e decodifica as mensagens enviadas pelo árbitro, não bloqueante.
        """
        try:
            data, _ = self.referee_socket.recvfrom(1024)
            referee_message = Referee()
            referee_message.ParseFromString(data)
            self.referee_state = referee_message  # Armazena o estado do árbitro
            return self.referee_state
        except BlockingIOError:
            # Retorna None se não houver dados para evitar a exceção de bloqueio
            return None

    def handle_referee_command(self):
        if self.referee_state:
            self.field.update_game_state(self.referee_state)
