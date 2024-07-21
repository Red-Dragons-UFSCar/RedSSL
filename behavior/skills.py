from path.desvio_obstaculo import *
import numpy as np


from entities.Robot import Robot
from entities.Target import (
    Target,
)  # Supondo que a classe Target esteja em entities/Target.py


def quadradinho(robot0, robots, enemy_robots, vg):
    # Alvos para cada eixo coordenado
    x_target = [100, 100, 600, 600]
    y_target = [500, 100, 100, 500]
    theta_target = [-np.pi / 2, 0, np.pi / 2, np.pi]

    next_target = calcular_target(
        robot0, x_target, y_target, theta_target, robots, enemy_robots, vg
    )

    # Atualizar o target do robô
    robot0.set_target(next_target)


def atualizar_target(robot0, x_target, y_target):
    n_points = len(x_target)
    target_distance = np.sqrt(
        (robot0.get_coordinates().X - x_target[robot0.cont_target]) ** 2
        + (robot0.get_coordinates().Y - y_target[robot0.cont_target]) ** 2
    )

    if target_distance < 10:
        robot0.cont_target = (robot0.cont_target + 1) % n_points


def calcular_target(robot0, x_target, y_target, theta_target, robots, enemy_robots, vg):
    atualizar_target(robot0, x_target, y_target)

    current_position = np.array(
        [robot0.get_coordinates().X, robot0.get_coordinates().Y]
    )
    current_target = np.array(
        [
            x_target[robot0.cont_target],
            y_target[robot0.cont_target],
            theta_target[robot0.cont_target],
        ]
    )

    next_target = desvio_obstaculo(
        current_position, current_target, robots, enemy_robots, vg
    )

    # Garantir que o next_target tenha o theta
    next_target_with_theta = np.array(
        [next_target[0], next_target[1], current_target[2]]
    )

    return next_target_with_theta
