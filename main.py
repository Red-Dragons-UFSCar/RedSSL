import sys
from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from entities.Field import Field
from entities.Coach import Coach
from behavior.skills import go_to_point
from behavior.plays import (
    estrategia_basica,
    estrategia_penalti_defensivo,
    estrategia_penalti_ofensivo,
)
from communication.referee import RefereeCommunication
from behavior.tactics import *
import time
import threading
import json
import os


CONTROL_FPS = 60  # FPS original para o controle de posição
CAM_FPS = 7 * CONTROL_FPS  # FPS para processar os dados da visão

REFEREE_ON = False  # Habilita a comunicação com o Referee


class RepeatTimer(threading.Timer):
    """
    Descrição:
        Classe herdada de Timer para execução paralela da thread de visão
        TODO: Verificar a utilização da biblioteca asyncio para isso.
    """

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class RobotController:
    def __init__(self):
        # Lendo os valores de IP e Porta

        with open("constants/network.json", "r") as file:
            network = json.load(file)

        with open("constants/mode_playing.json", "r") as file:
            self.mode_playing = json.load(file)

        if self.mode_playing["simulated_mode"]:
            # Lendo as configurações de jogo para simulação
            with open("constants/game.json", "r") as file:
                self.game = json.load(file)
        else:
            # Lendo as configurações de jogo para vida real
            with open("constants/game_real.json", "r") as file:
                self.game = json.load(file)
        
        with open("constants/filter_parameters.json", "r") as file:
            filter_parameters = json.load(file)

        self.team_color = self.game["team"]["color"]  # Lê a cor do time

        # Inicializa a comunicação com a visão e o atuador
        self.visao = Vision(
            ip=network["vision"]["ip"],
            port=network["vision"]["port"],
            is_right_side=(
                self.game["team"]["right_side"]
            ),  # Define como True se o time é amarelo
        )
        self.actuator = Actuator(
            ip=network["command"]["ip"], team_port=network["command"]["port"]
        )

        # Inicializa o campo de jogo
        self.field = Field(self.team_color)
        self.referee = RefereeCommunication(
            field=self.field,
            ip=network["referee"]["ip"],
            port=network["referee"]["port"],
        )

        # Inicializa o coach
        self.coach = Coach(self.field)

        # Cria e adiciona robôs ao campo com base na cor escolhida
        if self.team_color == "blue":
            self.robot0 = Robot(
                robot_id=0,
                actuator=self.actuator,
                vision_id=self.game["team"]["id_goalkeeper"],
            )
            self.robot1 = Robot(
                robot_id=1,
                actuator=self.actuator,
                vision_id=self.game["team"]["id_defender"],
            )
            self.robot2 = Robot(
                robot_id=2,
                actuator=self.actuator,
                vision_id=self.game["team"]["id_attacker"],
            )
            self.field.add_blue_robot(self.robot0)
            self.field.add_blue_robot(self.robot1)
            self.field.add_blue_robot(self.robot2)
            self.field.team_robots = [self.robot0, self.robot1, self.robot2]

            # Cria e adiciona robôs inimigos
            self.enemy_robot0 = Robot(robot_id=0, actuator=None)
            self.enemy_robot1 = Robot(robot_id=1, actuator=None)
            self.enemy_robot2 = Robot(robot_id=2, actuator=None)
            self.field.add_yellow_robot(self.enemy_robot0)
            self.field.add_yellow_robot(self.enemy_robot1)
            self.field.add_yellow_robot(self.enemy_robot2)
            self.field.enemy_robots = [
                self.enemy_robot0,
                self.enemy_robot1,
                self.enemy_robot2,
            ]
        elif self.team_color == "yellow":
            self.robot0 = Robot(
                robot_id=0,
                actuator=self.actuator,
                vision_id=self.game["team"]["id_goalkeeper"],
            )
            self.robot1 = Robot(
                robot_id=1,
                actuator=self.actuator,
                vision_id=self.game["team"]["id_defender"],
            )
            self.robot2 = Robot(
                robot_id=2,
                actuator=self.actuator,
                vision_id=self.game["team"]["id_defender"],
            )
            self.field.add_yellow_robot(self.robot0)
            self.field.add_yellow_robot(self.robot1)
            self.field.add_yellow_robot(self.robot2)
            self.field.team_robots = [self.robot0, self.robot1, self.robot2]
            # Cria e adiciona robôs inimigos
            self.enemy_robot0 = Robot(robot_id=0, actuator=None)
            self.enemy_robot1 = Robot(robot_id=1, actuator=None)
            self.enemy_robot2 = Robot(robot_id=2, actuator=None)
            self.field.add_blue_robot(self.enemy_robot0)
            self.field.add_blue_robot(self.enemy_robot1)
            self.field.add_blue_robot(self.enemy_robot2)
            self.field.enemy_robots = [
                self.enemy_robot0,
                self.enemy_robot1,
                self.enemy_robot2,
            ]
        
        self.file_simulation_data = None

        for param in filter_parameters:
            setattr(self.robot0.filter, param, np.asarray(filter_parameters[param]))
            print(getattr(self.robot0.filter, param))

    def update_coordinates(self, frame):
        if frame["frame_number"] == 0:
            return

        # Atualiza as posições dos robôs azuis no campo com base nas informações da visão
        self.field.verify_team_id(frame[f"robots_{self.team_color}"])
        for detection in frame[f"robots_{self.team_color}"]:
            # detection_pos = np.array([detection["x"], detection["y"]])
            # detection_pos_with_noise = self.add_gaussian_noise(detection_pos, 0.01, 0.08)
            # # print([detection["x"], detection["y"]])
            # # print(detection_pos_with_noise)
            # detection["x"] = detection_pos_with_noise[0]
            # detection["y"] = detection_pos_with_noise[1]

            self.field.update_robot_position(
                detection["robot_id"],
                detection["x"],
                detection["y"],
                # detection_pos_with_noise[0],
                # detection_pos_with_noise[1],
                detection["orientation"],
                self.team_color,
            )

            if detection["robot_id"] == 0:
                data = [self.visao.last_frame['frame_number'], self.robot0.robot_id, detection["x"], detection["y"], self.robot0.get_coordinates().X, self.robot0.get_coordinates().Y, self.robot0._velocities_cache[0], self.robot0._velocities_cache[1]]
            elif detection["robot_id"] == 1:
                data = [self.visao.last_frame['frame_number'], self.robot1.robot_id, detection["x"], detection["y"], self.robot1.get_coordinates().X, self.robot1.get_coordinates().Y, self.robot1._velocities_cache[0], self.robot1._velocities_cache[1]]
            elif detection["robot_id"] == 2:
                data = [self.visao.last_frame['frame_number'], self.robot2.robot_id, detection["x"], detection["y"], self.robot2.get_coordinates().X, self.robot2.get_coordinates().Y, self.robot2._velocities_cache[0], self.robot2._velocities_cache[1]]
            np.savetxt(self.file_simulation_data, np.array([data]))            

        # Atualiza as posições dos robôs inimigos no campo com base nas informações da visão
        enemy_color = "yellow" if self.team_color == "blue" else "blue"
        self.field.verify_enemy_id(frame[f"robots_{enemy_color}"])
        for detection in frame[f"robots_{enemy_color}"]:
            self.field.update_robot_position(
                detection["robot_id"],
                detection["x"],
                detection["y"],
                detection["orientation"],
                enemy_color,
            )

        # Atualiza a posição da bola com base nas informações da visão
        if frame["ball"]:
            ball_detection = frame["ball"]
            self.field.update_ball_position(ball_detection["x"], ball_detection["y"])
    
    def add_gaussian_noise(self, pos, min_sigma, max_sigma):
        field_center = [225, 150]
        upper_right_corner = [450, 300]

        dist_between_center_to_corner = np.sqrt(np.power(upper_right_corner[0] - field_center[0], 2) + np.power(upper_right_corner[1] - field_center[1], 2))
        dist_pos_to_center = np.sqrt(np.power(pos[0] - field_center[0], 2) + np.power(pos[1] - field_center[1], 2))

        k = dist_pos_to_center / dist_between_center_to_corner
        std = min_sigma + k * (max_sigma - min_sigma)
        noise1 = np.random.randn(1)*std
        noise2 = np.random.randn(1)*std

        pos_with_noise = np.array([pos[0] + noise1[0], pos[1] + noise2[0]])

        return pos_with_noise

    def send_velocities(self):
        # Envio de velocidades no sistema global
        """
        # Envia as velocidades armazenadas para o atuador
        self.actuator.send_globalVelocity_message(
            self.robot0, self.robot0.vx, self.robot0.vy, self.robot0.w
        )
        self.actuator.send_globalVelocity_message(
            self.robot1, self.robot1.vx, self.robot1.vy, self.robot1.w
        )
        self.actuator.send_globalVelocity_message(
            self.robot2, self.robot2.vx, self.robot2.vy, self.robot2.w
        )
        """
        # Envio de velocidades do sistema global diretamente para as rodas
        self.actuator.send_wheel_from_global(
            self.robot0,
            self.robot0.vx,
            self.robot0.vy,
            self.robot0.w,
            self.mode_playing["simulated_mode"],
        )
        self.actuator.send_wheel_from_global(
            self.robot1,
            self.robot1.vx,
            self.robot1.vy,
            self.robot1.w,
            self.mode_playing["simulated_mode"],
        )
        self.actuator.send_wheel_from_global(
            self.robot2,
            self.robot2.vx,
            self.robot2.vy,
            self.robot2.w,
            self.mode_playing["simulated_mode"],
        )

    def get_vision_frame(self):
        """
        Descrição:
        Função para adquirir os dados de visão e atualizar eles
        nos respectivos robôs
        """
        self.visao.update()
        frame = self.visao.get_last_frame()
        self.update_coordinates(frame)

    def start_vision_thread(self):
        """
        Descrição:
            Função que inicia a thread da visão
        """

        filename = 'dados_simulador4.txt'
        # self.file_simulation_data = open('treinamento_filtro/' + filename, 'w')
        
        if not os.path.isfile('treinamento_filtro/' + filename):
            self.file_simulation_data = open('treinamento_filtro/' + filename, 'w')
        else:
            print("Arquivo já existe!")
            exit(1)

        self.vision_thread = RepeatTimer((1 / CAM_FPS), self.get_vision_frame)
        self.vision_thread.start()

    def control_loop(self):
        while True:
            t1 = time.time()

            self.field.allowed_robots = 3

            if REFEREE_ON:
                # Recebe a mensagem do árbitro
                self.referee.get_referee_message()
                # Trata o comando do árbitro
                self.referee.handle_referee_command()
            else:
                self.field.game_on = True
                self.field.game_stopped = False

            Coach.escolher_estrategia(self.coach, self.robot0, self.robot1, self.robot2)
            self.send_velocities()

            t2 = time.time()

            self.robot0.map_obstacle.clear_map()
            self.robot1.map_obstacle.clear_map()
            self.robot2.map_obstacle.clear_map()
            print("---------------------------------------")
            print("    LOGGING DOS ROBÔS TIME     ")
            print("---------------------------------------")
            print("Robo goleiro, id=", self.robot0.vision_id)
            print("x: ", self.robot0.get_coordinates().X)
            print("y: ", self.robot0.get_coordinates().Y)
            print("r: ", self.robot0.get_coordinates().rotation)
            print("Robo zagueiro, id=", self.robot1.vision_id)
            print("x: ", self.robot1.get_coordinates().X)
            print("y: ", self.robot1.get_coordinates().Y)
            print("r: ", self.robot1.get_coordinates().rotation)
            print("Robo goleiro, id=", self.robot2.vision_id)
            print("x: ", self.robot2.get_coordinates().X)
            print("y: ", self.robot2.get_coordinates().Y)
            print("r: ", self.robot2.get_coordinates().rotation)

            print("---------------------------------------")
            print("    LOGGING DOS ROBÔS INIMIGO     ")
            print("---------------------------------------")
            print("Robo goleiro, id=", self.enemy_robot0.vision_id)
            print("x: ", self.enemy_robot0.get_coordinates().X)
            print("y: ", self.enemy_robot0.get_coordinates().Y)
            print("r: ", self.enemy_robot0.get_coordinates().rotation)
            print("Robo zagueiro, id=", self.enemy_robot1.vision_id)
            print("x: ", self.enemy_robot1.get_coordinates().X)
            print("y: ", self.enemy_robot1.get_coordinates().Y)
            print("r: ", self.enemy_robot1.get_coordinates().rotation)
            print("Robo goleiro, id=", self.enemy_robot2.vision_id)
            print("x: ", self.enemy_robot2.get_coordinates().X)
            print("y: ", self.enemy_robot2.get_coordinates().Y)
            print("r: ", self.enemy_robot2.get_coordinates().rotation)

            if (t2 - t1) < 1 / CONTROL_FPS:
                time.sleep(1 / CONTROL_FPS - (t2 - t1))
                # print("Tempo de execução: ", (t2 - t1) * 1000)
            else:
                print("[TIMEOUT] - Execução de controle excedida: ", (t2 - t1) * 1000)


if __name__ == "__main__":
    controller = RobotController()
    controller.start_vision_thread()
    controller.control_loop()
