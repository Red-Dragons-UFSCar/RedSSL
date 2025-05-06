from entities.Ball import Ball
from entities.Robot import Robot
from communication.proto.ssl_gc_referee_message_pb2 import Referee
from entities import Field, Coach
import time


class Field:
    def __init__(self, team="blue"):
        self.blue_robots = []
        self.yellow_robots = []
        self.team_robots = []
        self.enemy_robots = []
        self.enemy_vision_id = []
        self.count_enemy_id =[]
        self.count_team_id = [0,0,0]
        self.threshold_enemy_id = 100
        self.threshold_team_id = 100
        self.obstacles = []
        self.ball = Ball()
        self.width = 900  # Exemplo de largura do campo em cm
        self.height = 600  # Exemplo de altura do campo em cm
        self.game_state = None  # Dicionário para armazenar o estado do jogo

        # Máquina de estados do zagueiro
        self.zagueiro_current_state = "A"

        # Máquina de estados do atacante
        self.atacante_current_state = "A"

        # Máquina de estados do atacante real
        self.atacante_state_real = "A"
        self.enable_angular_controller_mono = False
        self.threshold_attacker_stop = [30, 30, 30]
        self.counter_attacker_stop = [0, 0, 0]

        # Define o time do robô
        self.team = team

        # Flags para estados de jogo
        self.game_on = False
        self.game_stopped = True
        self.game_halted = False
        self.defending_foul = False
        self.offensive_foul = False
        self.kickoff_offensive = False
        self.kickoff_defensive = False
        self.penalty_offensive = False
        self.penalty_defensive = False
        self.game_on_but_is_penalty = False

        # Flags para cartão e timestamp
        self.yellow_card_flag = False
        self.yellow_card_timestamp = None
        self.true_yellow_cards_counter = 0
        self.red_card_flag = False
        self.yellow_cards_counter = 0
        self.red_cards_counter = 0

        self.send_local = False

        self.allowed_robots = 3

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

    def verify_enemy_id(self, robots):
        for robot in robots:
            if robot['robot_id'] in self.enemy_vision_id:
                index = self.enemy_vision_id.index(robot['robot_id'])
                self.count_enemy_id[index] = 0
            else:
                self.enemy_vision_id.append(robot['robot_id'])
                self.count_enemy_id.append(0)

        #print("Enemies: ", self.enemy_vision_id)
        
        list_new_enemies = []
        list_new_count = []
        for i in range(len(self.count_enemy_id)):
            #print("ID robo:", self.enemy_vision_id[i])
            #print("Contagem: ", self.count_enemy_id[i])
            if self.count_enemy_id[i] < self.threshold_enemy_id:
                list_new_enemies.append(self.enemy_vision_id[i])
                list_new_count.append(self.count_enemy_id[i])

        self.enemy_vision_id = list_new_enemies
        self.count_enemy_id = list_new_count

        for i in range(len(self.count_enemy_id)):
            self.count_enemy_id[i] += 1

        #print("ID robôs inimigos: ", self.enemy_vision_id)
        #print("Robos: ", self.enemy_vision_id)
        if len(self.enemy_vision_id) < 3:
            resets = 3 - len(self.enemy_vision_id)
            for i in range(len(self.enemy_vision_id)):
                self.enemy_robots[i].vision_id = self.enemy_vision_id[i]
            for i in range(resets):
                self.enemy_robots[2-i].set_coordinates(0,0,0)
                self.enemy_robots[2-i].vision_id = None
        else:
            for i in range(3):
                self.enemy_robots[i].vision_id = self.enemy_vision_id[i]

    def verify_team_id(self, robots):
        for i in range(len(robots)):
            for j in range(len(self.team_robots)):
                if robots[i]['robot_id'] == self.team_robots[j].vision_id:
                    self.count_team_id[j] = 0
        
        for i in range(len(self.count_team_id)):
            #print("ID robo:", self.team_robots[i].vision_id)
            #print("Contagem: ", self.count_team_id[i])
            #print("Contadores: ", self.count_team_id)
            if self.count_team_id[i] > self.threshold_team_id:
                self.team_robots[i].set_coordinates(0,0,0)
            else:
                self.count_team_id[i] += 1

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
            if self.game_on and (self.penalty_offensive or self.penalty_defensive):
                self.game_on_but_is_penalty = True
                print("Jogando situacao de penalty")

            else:
                print("Game iniciado")
                self.game_on = True
                self.game_stopped = False
                self.game_halted = False
                self.kickoff_offensive = False
                self.kickoff_defensive = False
                self.game_on_but_is_penalty = False

        elif command == Referee.Command.STOP:
            self.game_on = False
            self.game_stopped = True
            self.game_halted = False
            self.defending_foul = True
            self.offensive_foul = False
            self.penalty_offensive = False
            self.penalty_defensive = False
            self.game_on_but_is_penalty = False

            print("JOGO PARADO")
        elif command == Referee.Command.HALT:
            self.game_on = False
            self.game_stopped = False
            self.game_halted = True
            self.penalty_offensive = False
            self.penalty_defensive = False
            self.game_on_but_is_penalty = False

            print("JOGO INTERROMPIDO")

        elif command == Referee.Command.PREPARE_KICKOFF_YELLOW:
            print("KICKOFF YELLOW")
            if self.team == "yellow":
                # flag do coach de kickoff ofensivo
                self.kickoff_offensive = True
                self.kickoff_defensive = False
                self.game_on = False
                self.game_stopped = False
                self.game_halted = False
                self.penalty_offensive = False
                self.penalty_defensive = False
                self.game_on_but_is_penalty = False

            else:
                # flag do coach de kickoff defensivo
                self.kickoff_offensive = False
                self.kickoff_defensive = True
                self.game_on = False
                self.game_stopped = False
                self.game_halted = False
                self.penalty_offensive = False
                self.penalty_defensive = False
                self.game_on_but_is_penalty = False

        elif command == Referee.Command.PREPARE_KICKOFF_BLUE:
            print("KICKOFF BLUE")
            if self.team == "blue":
                # flag do coach de kickoff ofensivo
                self.kickoff_offensive = True
                self.kickoff_defensive = False
                self.penalty_offensive = False
                self.penalty_defensive = False
                self.game_on_but_is_penalty = False

            else:
                # flag do coach de kickoff defensivo
                self.kickoff_offensive = False
                self.kickoff_defending = True
                self.penalty_offensive = False
                self.penalty_defensive = False
                self.game_on_but_is_penalty = False

        elif command == Referee.Command.PREPARE_PENALTY_YELLOW:
            print("PENALTY YELLOW")
            if self.team == "yellow":
                # flag do coach de kickoff ofensivo
                self.kickoff_offensive = False
                self.kickoff_defensive = False
                self.game_on = False
                self.game_stopped = False
                self.game_halted = False
                self.penalty_offensive = True
                self.penalty_defensive = False

            else:
                # flag do coach de kickoff defensivo
                self.kickoff_offensive = False
                self.kickoff_defensive = False
                self.game_on = False
                self.game_stopped = False
                self.game_halted = False
                self.penalty_offensive = False
                self.penalty_defensive = True

        elif command == Referee.Command.PREPARE_PENALTY_BLUE:
            print("PENALTY BLUE")
            if self.team == "blue":
                # flag do coach de kickoff ofensivo
                self.kickoff_offensive = False
                self.kickoff_defensive = False
                self.game_on = False
                self.game_stopped = False
                self.game_halted = False
                self.penalty_offensive = True
                self.penalty_defensive = False

            else:
                # flag do coach de kickoff defensivo
                self.kickoff_offensive = False
                self.kickoff_defensive = False
                self.game_on = False
                self.game_stopped = False
                self.game_halted = False
                self.penalty_offensive = False
                self.penalty_defensive = True

        elif command == Referee.Command.DIRECT_FREE_YELLOW:
            print("FREEKICK YELLOW.")
            self.game_on = False
            self.game_stopped = True
            self.game_halted = False
            if self.team == "yellow":
                self.offensive_foul = True
                self.defending_foul = False
            else:
                self.offensive_foul = False
                self.defending_foul = True

        elif command == Referee.Command.DIRECT_FREE_BLUE:
            print("FREEKICK BLUE")
            self.game_on = False
            self.game_stopped = True
            self.game_halted = False
            if self.team == "blue":
                self.offensive_foul = True
                self.defending_foul = False
            else:
                self.offensive_foul = False
                self.defending_foul = True

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

        self.process_cards(referee_state)

    def process_cards(self, referee_state):
        """
        Processa e imprime informações sobre cartões amarelos recebidos.
        """
        # Obtém as informações sobre os times a partir do estado do árbitro
        yellow_team_info = referee_state.yellow
        blue_team_info = referee_state.blue

        if (
            yellow_team_info.yellow_cards > self.yellow_cards_counter
            and self.team == "yellow"
        ):
            print("CARTAO PRO TIME AMARELO")
            self.yellow_card_flag = True
            self.yellow_card_timestamp = time.time()  # Registra o tempo do cartão
            self.yellow_cards_counter = yellow_team_info.yellow_cards
            self.true_yellow_cards_counter += 1

        if (
            blue_team_info.yellow_cards > self.yellow_cards_counter
            and self.team == "blue"
        ):
            print("CARTAO PRO TIME AZUL")
            self.yellow_card_flag = True
            self.yellow_card_timestamp = time.time()  # Registra o tempo do cartão
            self.yellow_cards_counter = blue_team_info.yellow_cards
            self.true_yellow_cards_counter += 1

        if (
            yellow_team_info.red_cards > self.red_cards_counter
            and self.team == "yellow"
        ):
            print("CARTAO VERMELHO PRO TIME AMARELO")
            self.red_card_flag = True
            self.red_cards_counter = yellow_team_info.red_cards

        if blue_team_info.red_cards > self.red_cards_counter and self.team == "blue":
            print("CARTAO VERMELHO PRO TIME AZUL")
            self.red_card_flag = True
            self.red_cards_counter = blue_team_info.red_cards
