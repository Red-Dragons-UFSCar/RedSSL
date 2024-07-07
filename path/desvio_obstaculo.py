import numpy as np
from entities.Robot import Robot
from entities.Target import (
    Target,
)


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


def desvio_obstaculo(current_position, current_target, robots, enemy_robots, vg):
    vg.set_origin(current_position)
    vg.set_target(current_target)

    # Adicionar obstáculos ao mapa de visibilidade
    vg_obstacles = []
    obstacles = robots[1:] + enemy_robots
    for obstacle in obstacles:
        triangle = vg.robot_triangle_obstacle(obstacle, robots[0])
        vg_triangle = vg.convert_to_vgPoly(triangle)
        vg_obstacles.append(vg_triangle)

    vg.update_obstacle_map(vg_obstacles)
    path = vg.get_path()

    if path:
        # Pega o próximo ponto no caminho gerado pelo algoritmo de visibilidade
        next_point = path[1] if len(path) > 1 else path[0]
        next_target = np.array([next_point.x, next_point.y])
    else:
        # Se não há caminho, mantém o alvo atual
        next_target = current_target

    return next_target
