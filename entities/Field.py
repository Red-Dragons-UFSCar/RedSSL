from entities.Ball import Ball
from entities.Robot import Robot
from communication.proto.ssl_gc_referee_message_pb2 import Referee


class Field:
    def __init__(self):
        self.blue_robots = []
        self.yellow_robots = []
        self.team_robots = []
        self.enemy_robots = []
        self.obstacles = []
        self.ball = Ball()
        self.width = 900  # Exemplo de largura do campo em cm
        self.height = 600  # Exemplo de altura do campo em cm
        self.game_state = None  # Dicionário para armazenar o estado do jogo
        self.yellow_team_yellow_cards_counter = 0
        self.blue_team_yellow_cards_counter = 0
        self.yellow_team_red_cards_counter = 0
        self.blue_team_red_cards_counter = 0

        # Máquina de estados do zagueiro
        self.zagueiro_current_state = "A"
        self.zagueiro_current_state = "A"

        # Máquina de estados do atacante
        self.atacante_current_state = "A"

        # Flags para estados de jogo
        self.game_on = False
        self.game_stopped = True
        self.defending_foul = True
        self.offensive_foul = False

    def add_blue_robot(self, robot):
        self.blue_robots.append(robot)

    def add_yellow_robot(self, robot):
        self.yellow_robots.append(robot)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def get_obstacles(self):
        return self.obstacles

    def get_ally_robots(self):
        return self.blue_robots

    def get_enemy_robots(self):
        return self.yellow_robots

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def update_robot_position(self, robot_id, x, y, theta, color):
        if color == "blue":
            robots = self.blue_robots
        else:
            robots = self.yellow_robots

        for robot in robots:
            if robot.vision_id == robot_id:
                robot.set_coordinates(x, y, theta)
                break

    def update_ball_position(self, x, y):
        self.ball.set_coordinates(x, y)

    def update_game_state(self, referee_state):
        """
        Atualiza o estado do jogo com base nas informações recebidas do árbitro.
        """
        command = referee_state.command
        self.game_state = command  # Adiciona o comando atual ao estado do jogo

        # Processa e imprime os eventos relevantes
        self.process_event(command, referee_state)

    def process_event(self, command, referee_state):
        """
        Processa e imprime os eventos relevantes do jogo.
        """
        if (
            command == Referee.Command.NORMAL_START
            or command == Referee.Command.FORCE_START
        ):
            self.game_on = True
            self.game_stopped = False
        elif command == Referee.Command.STOP or command == Referee.Command.HALT:
            self.game_on = False
            self.game_stopped = True

        elif command == Referee.Command.PREPARE_KICKOFF_YELLOW:
            print("KICKOFF YELLOW")

        elif command == Referee.Command.PREPARE_KICKOFF_BLUE:
            print("KICKOFF BLUE")

        elif command == Referee.Command.PREPARE_PENALTY_YELLOW:
            print("PENALTY YELLOW")

        elif command == Referee.Command.PREPARE_PENALTY_BLUE:
            print("PENALTY BLUE")

        elif command == Referee.Command.DIRECT_FREE_YELLOW:
            print("FREEKICK YELLOW.")

        elif command == Referee.Command.DIRECT_FREE_BLUE:
            print("FREEKICK BLUE")

        elif command == Referee.Command.TIMEOUT_YELLOW:
            print("TIMEOUT YELLOW")

        elif command == Referee.Command.TIMEOUT_BLUE:
            print("TIMEOUT BLUE")

        elif command == Referee.Command.GOAL_YELLOW:
            print("GOL YELLOW")

        elif command == Referee.Command.GOAL_BLUE:
            print("GOL BLUE")

        elif command == Referee.Command.BALL_PLACEMENT_YELLOW:
            print("BALL PLACEMENT YELLOW")

        elif command == Referee.Command.BALL_PLACEMENT_BLUE:
            print("BALL PLACEMENT BLUE")

        else:
            print(f"Comando desconhecido: {command}")

        self.process_cards(referee_state)

    def process_cards(self, referee_state):
        """
        Processa e imprime informações sobre cartões amarelos recebidos.
        """
        # Obtém as informações sobre os times a partir do estado do árbitro
        yellow_team_info = referee_state.yellow
        blue_team_info = referee_state.blue

        if yellow_team_info.yellow_cards > self.yellow_team_yellow_cards_counter:
            print("CARTAO PRO TIME AMARELO")

        if blue_team_info.yellow_cards > self.blue_team_yellow_cards_counter:
            print("CARTAO PRO TIME AZUL")

        self.yellow_team_yellow_cards_counter = yellow_team_info.yellow_cards
        self.blue_team_yellow_cards_counter = blue_team_info.yellow_cards

        if yellow_team_info.red_cards > self.yellow_team_red_cards_counter:
            print("CARTAO VERMELHO PRO TIME AMARELO")

        if blue_team_info.red_cards > self.blue_team_red_cards_counter:
            print("CARTAO VERMELHO PRO TIME AZUL")

        self.yellow_team_red_cards_counter = yellow_team_info.red_cards
        self.blue_team_red_cards_counter = blue_team_info.red_cards
