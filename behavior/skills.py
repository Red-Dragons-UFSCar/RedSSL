from path import desvio_obstaculo
from control.PID import control_robot
import numpy as np
from entities.Robot import Robot
from entities.Target import (
    Target,
)  # Supondo que a classe Target esteja em entities/Target.py


def quadradinho(robot):
    x_target = [100, 100, 600, 600]
    y_target = [500, 100, 100, 500]
    theta_target = [-np.pi / 2, 0, np.pi / 2, np.pi]

    square_points = [
        Target(x_target[0], y_target[0], theta_target[0]),
        Target(x_target[1], y_target[1], theta_target[1]),
        Target(x_target[2], y_target[2], theta_target[2]),
        Target(x_target[3], y_target[3], theta_target[3]),
    ]

    if robot.target is None or robot.target.is_reached(robot.get_coordinates()):
        if robot.target is None:
            robot.target = square_points[0]
        else:
            current_index = square_points.index(robot.target)
            next_index = (current_index + 1) % len(square_points)
            robot.target = square_points[next_index]

        path = desvio_obstaculo(robot.target)
        control_robot(robot, path)
