from communication.vision import Vision
from communication.actuator import Actuator
from entities.Robot import Robot
from control.PID import PID
from behavior.skills import *
import time
import numpy as np

class RobotController:
    def __init__(self, vision_ip, vision_port, actuator_port):
        self.visao = Vision(ip=vision_ip, port=vision_port)
        self.actuator = Actuator(team_port=actuator_port)

        self.robot0 = Robot(robot_id=0, actuator=self.actuator)
        self.robot1 = Robot(robot_id=1, actuator=None)
        self.robot2 = Robot(robot_id=2, actuator=None)

        self.robots = [self.robot0, self.robot1, self.robot2]

        self.enemy_robot0 = Robot(robot_id=0, actuator=None)
        self.enemy_robot1 = Robot(robot_id=1, actuator=None)

        self.enemy_robots = [self.enemy_robot0, self.enemy_robot1]

        self.cont = 0

    def update_coordinates(self, frame):
        for detection in frame["robots_blue"]:
            for robot in self.robots:
                if detection["robot_id"] == robot.robot_id:
                    x_pos, y_pos, theta = detection["x"], detection["y"], detection["orientation"]
                    robot.set_coordinates(x_pos, y_pos, theta)

        for detection in frame["robots_yellow"]:
            for enemy_robot in self.enemy_robots:
                if detection["robot_id"] == enemy_robot.robot_id:
                    x_pos, y_pos, theta = detection["x"], detection["y"], detection["orientation"]
                    enemy_robot.set_coordinates(x_pos, y_pos, theta)

    def control_loop(self):
        while True:
            t1 = time.time()

            self.visao.update()
            frame = self.visao.get_last_frame()
            self.update_coordinates(frame)

            self.cont += 1

            if self.cont == 5:

                # Exlude robot 0
                other_robots = self.robots[1:]

                vx, vy, w = go_to_point(self.robot0, 100, 500, other_robots, self.enemy_robots)
                self.robot0.apply_velocity(vx, vy, w)
                self.cont = 0

            t2 = time.time()

            if (t2 - t1) < 1 / 300:
                time.sleep(1 / 300 - (t2 - t1))

if __name__ == "__main__":
    controller = RobotController(vision_ip="224.5.23.2", vision_port=10020, actuator_port=10301)
    controller.control_loop()
