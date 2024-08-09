from entities.Ball import Ball
from entities.Robot import Robot

class Field:
    def __init__(self):
        self.blue_robots = []
        self.yellow_robots = []
        self.obstacles = []
        self.ball = Ball()
        self.width = 900  # Exemplo de largura do campo em cm
        self.height = 600  # Exemplo de altura do campo em cm

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
            if robot.robot_id == robot_id:
                robot.set_coordinates(x, y, theta)
                break

    def update_ball_position(self, x, y):
        self.ball.set_coordinates(x, y)
