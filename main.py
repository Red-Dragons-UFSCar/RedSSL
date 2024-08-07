from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from entities.Field import Field
from control.PID import PID
from behavior.skills import *
import time
import numpy as np
import threading

CONTROL_FPS = 60
CAM_FPS = 5*CONTROL_FPS

# Classe para interrupção de tempo
class RepeatTimer(threading.Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  

class RobotController:
    def __init__(self, vision_ip, vision_port, actuator_port):
        # Inicializa a comunicação com a visão e o atuador
        self.visao = Vision(ip=vision_ip, port=vision_port)
        self.actuator = Actuator(team_port=actuator_port)

        # Inicializa o campo de jogo
        self.field = Field()

        # Cria e adiciona um robô ao campo
        self.robot0 = Robot(robot_id=0, actuator=self.actuator)
        self.field.add_blue_robot(self.robot0)

        self.robot1 = Robot(robot_id=1, actuator=None)
        # self.robot2 = Robot(robot_id=2, actuator=None)
        self.field.add_blue_robot(self.robot1)
        # self.field.add_blue_robot(self.robot2)

        # Cria e adiciona robôs inimigos ao campo
        self.enemy_robot0 = Robot(robot_id=0, actuator=None)
        #self.enemy_robot1 = Robot(robot_id=1, actuator=None)
        self.field.add_yellow_robot(self.enemy_robot0)
        #self.field.add_yellow_robot(self.enemy_robot1)

        # Contador para controle do loop
        self.cont = 0

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

    def send_velocities(self):
        # Envia as velocidades armazenadas para o atuador
        robot0 = self.robot0
        self.actuator.send_globalVelocity_message(
            robot0.robot_id, robot0.vx, robot0.vy, robot0.w
        )

    def get_vision_frame(self):
        self.visao.update()
        frame = self.visao.get_last_frame()
        self.update_coordinates(frame)

    def start_vision_thread(self):
        self.vision_thread = RepeatTimer((1/CAM_FPS), self.get_vision_frame)
        self.vision_thread.start()

    def control_loop(self):
        while True:
            t1 = time.time()
            '''
            self.cont += 1

            if self.cont == 5:
                # Move o robô para as coordenadas especificadas e envia as velocidades para o atuador
                go_to_point(self.robot0, 100, 500, self.field)
                self.send_velocities()
                self.cont = 0
            '''
            go_to_point(self.robot0, 100, 500, self.field)
            self.send_velocities()
            self.cont = 0
            print(self.robot0.get_coordinates().X)
            t2 = time.time()

            if (t2 - t1) < 1 / 60:
                time.sleep(1 / 60 - (t2 - t1))


if __name__ == "__main__":

    controller = RobotController(
        vision_ip="224.5.23.2", vision_port=10020, actuator_port=10301
    )
    controller.start_vision_thread()
    controller.control_loop()
