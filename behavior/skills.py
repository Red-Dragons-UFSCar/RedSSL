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
