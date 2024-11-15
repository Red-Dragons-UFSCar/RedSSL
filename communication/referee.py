import socket
from communication.proto.ssl_gc_referee_message_pb2 import Referee
from google.protobuf.message import DecodeError


class RefereeCommunication:
    def __init__(self, field, ip="224.5.23.1", port=10003):
        """
        Inicializa o socket para receber mensagens do árbitro e define o estado inicial.
        """
        self.referee_state = None
        self.field = field
        self.ip = ip
        self.port = port
        self.referee_socket = self._init_referee_socket()

        self.waiting_free_kick = False
        self.last_foul = Referee.Command.STOP
        self.last_time_saved = 0
        self.ball_x_saved_free_kick = 0
        self.ball_y_saved_free_kick = 0
        self.their_kickoff = False
        self.our_kickoff = False
        self.ball_x_saved_kickoff = 0
        self.ball_y_saved_kickoff = 0

    def _init_referee_socket(self):
        """
        Configura e inicializa o socket para comunicação com o árbitro.
        """
        referee_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        referee_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        referee_socket.bind((self.ip, self.port))
        mreq = socket.inet_aton(self.ip) + socket.inet_aton("0.0.0.0")
        referee_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        referee_socket.setblocking(False)
        return referee_socket

    def get_referee_message(self):
        """
        Recebe e decodifica as mensagens enviadas pelo árbitro, não bloqueante.
        """
        try:
            data, _ = self.referee_socket.recvfrom(4096)
            referee_message = Referee()
            referee_message.ParseFromString(data)
            self.referee_state = referee_message  # Armazena o estado do árbitro
            #print(self.referee_state)
            return self.referee_state
        except BlockingIOError:
            # Retorna None se não houver dados para evitar a exceção de bloqueio
            return None
        except DecodeError:
            print("Erro ao decodificar a mensagem do árbitro.")
            return None

    def handle_referee_command(self):
        if self.referee_state:
            self.field.update_game_state(self.referee_state)

    def change_foul_flags(self, 
                            field,
                            game_on = False,
                            game_stopped = False,
                            game_halted = False,
                            kickoff_offensive = False,
                            kickoff_defensive = False,
                            penalty_offensive = False,
                            penalty_defensive = False,
                            free_kick_offensive = False,
                            free_kick_defensive = False
                            ):
        field.game_on = game_on
        field.game_halted = game_halted
        field.game_stopped = game_stopped
        field.kickoff_offensive = kickoff_offensive
        field.kickoff_defensive = kickoff_defensive
        field.penalty_offensive = penalty_offensive
        field.penalty_defensive = penalty_defensive
        field.free_kick_offensive = free_kick_offensive
        field.free_kick_defensive = free_kick_defensive

    def parse_referee_command(self, field):
        if self.referee_state:
            command = self.referee_state.command
            #print("command: ", command)
            #print("tempo: ", self.referee_state.stage_time_left)

            if (command == Referee.Command.FORCE_START):
                print("Game on")
                self.change_foul_flags(field, game_on=True)
            elif command == Referee.Command.NORMAL_START:
                self.verify_their_kickoff(field, command)
                if self.their_kickoff:
                    print("FREE KICK - Deles")
                    ball_coordinates = field.ball.get_coordinates()
                    dist = (ball_coordinates.X - self.ball_x_saved_kickoff)**2 + (ball_coordinates.Y - self.ball_y_saved_kickoff)**2
                    print(dist)
                    if dist < 40*40 :
                        print("Aguardando")
                    else:
                        print("Atacando")
                        self.change_foul_flags(field, game_on=True)
                        self.their_kickoff = False
                elif self.our_kickoff:
                     self.change_foul_flags(field, game_on=True)

            elif self.verify_our_free_kick(field, command):
                print("FREE KICK - Nosso")
                self.change_foul_flags(field, game_on=True)
            elif self.verify_their_free_kick(field, command):
                print("FREE KICK - Deles")
                ball_coordinates = field.ball.get_coordinates()
                dist = (ball_coordinates.X - self.ball_x_saved_free_kick)**2 + (ball_coordinates.Y - self.ball_y_saved_free_kick)**2
                print(dist)
                if dist < 10*10 :
                    print("Aguardando")
                else:
                    print("Atacando")
                    self.change_foul_flags(field, game_on=True)
            elif self.verify_our_kickoff(field, command):
                print("KICKOFF - Nosso")
                self.change_foul_flags(field, kickoff_offensive=True)
            elif self.verify_their_kickoff(field, command):
                print("KICKOFF - Deles")
                self.change_foul_flags(field, kickoff_defensive=True)
                ball_coordinates = field.ball.get_coordinates()
                dist = (ball_coordinates.X - self.ball_x_saved_kickoff)**2 + (ball_coordinates.Y - self.ball_y_saved_kickoff)**2
                if dist > 10*10:
                    print("Atacando")
                    self.change_foul_flags(field, game_on=True)
                else:
                    print("Aguardando")
            elif command == Referee.Command.STOP:
                self.change_foul_flags(field, game_stopped=True)
                print("JOGO PARADO")
            elif command == Referee.Command.HALT:
                self.change_foul_flags(field, game_halted=True)
                print("JOGO INTERROMPIDO")

            elif command == Referee.Command.PREPARE_KICKOFF_YELLOW:
                if self.field.team == "yellow":
                    print("KICKOFF YELLOW - Nosso")
                    self.change_foul_flags(field, kickoff_offensive=True)
                else:
                    print("KICKOFF YELLOW - Deles")
                    self.change_foul_flags(field, kickoff_defensive=True)

            elif command == Referee.Command.PREPARE_KICKOFF_BLUE:
                if self.field.team == "blue":
                    print("KICKOFF BLUE - Nosso")
                    self.change_foul_flags(field, kickoff_offensive=True)
                else:
                    print("KICKOFF BLUE - Deles")
                    self.change_foul_flags(field, kickoff_defensive=True)

            elif command == Referee.Command.PREPARE_PENALTY_YELLOW:
                if self.field.team == "yellow":
                    print("PENALTY YELLOW - Nosso")
                    self.change_foul_flags(field, penalty_offensive=True)
                else:
                    print("PENALTY YELLOW - Deles")
                    self.change_foul_flags(field, penalty_defensive=True)

            elif command == Referee.Command.PREPARE_PENALTY_BLUE:
                print("PENALTY BLUE")
                if self.field.team == "blue":
                    print("PENALTY BLUE - Nosso")
                    self.change_foul_flags(field, penalty_offensive=True)
                else:
                    print("PENALTY BLUE - Deles")
                    self.change_foul_flags(field, penalty_defensive=True)

            elif command == Referee.Command.DIRECT_FREE_YELLOW:
                if self.field.team == "yellow":
                    print("FREEKICK YELLOW - Nosso")
                    self.change_foul_flags(field, free_kick_offensive=True)
                else:
                    print("FREEKICK YELLOW - Deles")
                    self.change_foul_flags(field, free_kick_defensive=True)

            elif command == Referee.Command.DIRECT_FREE_BLUE:
                if self.field.team == "blue":
                    print("FREEKICK BLUE - Nosso")
                    self.change_foul_flags(field, free_kick_offensive=True)
                else:
                    print("FREEKICK BLUE - Deles")
                    self.change_foul_flags(field, free_kick_defensive=True)
            else:
                print("Outra coisa")
                print("Comando: ", command)

            self.last_foul = command
            '''

            elif command == Referee.Command.TIMEOUT_YELLOW:
                self.game_on = False
                self.game_stopped = False
                self.game_halted = True
                self.penalty_offensive = False
                self.penalty_defensive = False
                self.game_on_but_is_penalty = False
                print("TIMEOUT YELLOW")

            elif command == Referee.Command.TIMEOUT_BLUE:
                self.game_on = False
                self.game_stopped = False
                self.game_halted = True
                self.penalty_offensive = False
                self.penalty_defensive = False
                self.game_on_but_is_penalty = False
                print("TIMEOUT BLUE")

            elif command == Referee.Command.GOAL_YELLOW:
                print("GOL YELLOW")

            elif command == Referee.Command.GOAL_BLUE:
                print("GOL BLUE")

            elif command == Referee.Command.BALL_PLACEMENT_YELLOW:
                print("BALL PLACEMENT YELLOW")
                self.game_on = False
                self.game_stopped = True
                self.game_halted = False
                self.offensive_foul = False
                self.defending_foul = False
                self.kickoff_offensive = False
                self.kickoff_defensive = False
                self.game_on_but_is_penalty = False

            elif command == Referee.Command.BALL_PLACEMENT_BLUE:
                print("BALL PLACEMENT BLUE")
                self.game_on = False
                self.game_stopped = True
                self.game_halted = False
                self.offensive_foul = False
                self.defending_foul = False
                self.kickoff_offensive = False
                self.kickoff_defensive = False
                self.game_on_but_is_penalty = False

            else:
                print(f"Comando desconhecido: {command}")
                '''

    def verify_our_free_kick(self, field, command):
        team = field.team
        if command == Referee.Command.DIRECT_FREE_BLUE:
            team_foul = 'blue'
        elif command == Referee.Command.DIRECT_FREE_YELLOW:
            team_foul = 'yellow'
        else:
            return

        our_foul = team_foul == team

        if our_foul:
            return True
        else:
            return False
        
    def verify_their_free_kick(self, field, command):
        team = field.team
        if command == Referee.Command.DIRECT_FREE_BLUE:
            team_foul = 'blue'
        elif command == Referee.Command.DIRECT_FREE_YELLOW:
            team_foul = 'yellow'
        else:
            return
        
        if self.last_foul != Referee.Command.DIRECT_FREE_BLUE and self.last_foul != Referee.Command.DIRECT_FREE_YELLOW:
            ball_coordinates = field.ball.get_coordinates()
            self.ball_x_saved_free_kick = ball_coordinates.X
            self.ball_y_saved_free_kick = ball_coordinates.Y

        their_foul = team_foul != team

        if their_foul:
            return True
        else:
            return False
        
    def verify_our_kickoff(self, field, command):
        team = field.team
        if command == Referee.Command.PREPARE_KICKOFF_BLUE:
            team_foul = 'blue'
        elif command == Referee.Command.PREPARE_KICKOFF_YELLOW:
            team_foul = 'yellow'
        else:
            return

        our_foul = team_foul == team

        self.our_kickoff = our_foul

        if our_foul:
            return True
        else:
            return False
        
    def verify_their_kickoff(self, field, command):
        team = field.team
        if command == Referee.Command.PREPARE_KICKOFF_BLUE:
            team_foul = 'blue'
        elif command == Referee.Command.PREPARE_KICKOFF_YELLOW:
            team_foul = 'yellow'
        else:
            return
        
        if command != Referee.Command.NORMAL_START:
            ball_coordinates = field.ball.get_coordinates()
            self.ball_x_saved_kickoff = ball_coordinates.X
            self.ball_y_saved_kickoff = ball_coordinates.Y

        their_foul = team_foul != team

        if their_foul:
            self.their_kickoff = True
        else:
            self.their_kickoff = False

        if their_foul:
            return True
        else:
            return False