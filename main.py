from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from entities.Field import Field
from entities.Coach import Coach
import time
import threading
import json

CONTROL_FPS = 60  # FPS original para o controle de posição
CAM_FPS = 7 * CONTROL_FPS  # FPS para processar os dados da visão


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
    def __init__(self, is_right_side):
        # Abrindo e lendo o arquivo JSON
        with open('constants/network.json', 'r') as file:
            network = json.load(file)
        
        # Inicializa a comunicação com a visão e o atuador
        self.visao = Vision(ip=network['vision']['ip'], port=network['vision']['port'], is_right_side=is_right_side)
        self.actuator = Actuator(ip=network['command']['ip'], team_port=network['command']['port'])

        # Inicializa o campo de jogo
        self.field = Field()

        # Inicializa o coach
        self.coach = Coach(self.field)

        # Cria e adiciona um robô ao campo
        self.robot0 = Robot(robot_id=0, actuator=self.actuator)
        self.field.add_blue_robot(self.robot0)

        self.robot1 = Robot(robot_id=1, actuator=self.actuator)
        self.robot2 = Robot(robot_id=2, actuator=self.actuator)
        self.field.add_blue_robot(self.robot1)
        self.field.add_blue_robot(self.robot2)

        # Cria e adiciona robôs inimigos ao campo
        self.enemy_robot0 = Robot(robot_id=0, actuator=None)
        self.enemy_robot1 = Robot(robot_id=1, actuator=None)
        self.enemy_robot2 = Robot(robot_id=2, actuator=None)
        self.field.add_yellow_robot(self.enemy_robot0)
        self.field.add_yellow_robot(self.enemy_robot1)
        self.field.add_yellow_robot(self.enemy_robot2)

        # Contador para controle do loop
        self.cont = 0

        #flag para habilitar penalti: 
        self.penalty_start_time = None

    def update_coordinates(self, frame):
        # Atualiza as posições dos robôs azuis no campo com base nas informações da visão
        for detection in frame["robots_blue"]:
            self.field.update_robot_position(
                detection["robot_id"],
                detection["x"],
                detection["y"],
                detection["orientation"],
                "blue",
            )

        # Atualiza as posições dos robôs amarelos (inimigos) no campo com base nas informações da visão
        for detection in frame["robots_yellow"]:
            self.field.update_robot_position(
                detection["robot_id"],
                detection["x"],
                detection["y"],
                detection["orientation"],
                "yellow",
            )

        # Atualiza a posição da bola com base nas informações da visão
        if "ball" in frame:
            ball_detection = frame["ball"]
            self.field.update_ball_position(ball_detection["x"], ball_detection["y"])

    def send_velocities(self):
        # Envio de velocidades no sistema global
        '''
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
        '''
        # Envio de velocidades do sistema global diretamente para as rodas
        self.actuator.send_wheel_from_global(
            self.robot0, self.robot0.vx, self.robot0.vy, self.robot0.w
        )
        self.actuator.send_wheel_from_global(
            self.robot1, self.robot1.vx, self.robot1.vy, self.robot1.w
        )
        self.actuator.send_wheel_from_global(
            self.robot2, self.robot2.vx, self.robot2.vy, self.robot2.w
        )
        #'''

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
        self.vision_thread = RepeatTimer((1 / CAM_FPS), self.get_vision_frame)
        self.vision_thread.start()

    def control_loop(self):
        self.field.game_stopped = False
        self.field.game_on = True
        self.field.defending_foul = False
        self.field.ofensive_foul = False
        while True:
            t1 = time.time()
            Coach.escolher_estrategia(self.coach, self.robot0, self.robot1, self.robot2)
            self.send_velocities()
            t2 = time.time()

            self.robot0.map_obstacle.clear_map()
            self.robot1.map_obstacle.clear_map()
            self.robot2.map_obstacle.clear_map()
            

            if (t2 - t1) < 1 / CONTROL_FPS:
                time.sleep(1 / CONTROL_FPS - (t2 - t1))
                print("Tempo de execução: ", (t2 - t1) * 1000)
            else:
                print("[TIMEOUT] - Execução de controle excedida: ", (t2 - t1) * 1000)


if __name__ == "__main__":
    controller = RobotController(is_right_side=False)
    controller.start_vision_thread()
    controller.control_loop()
