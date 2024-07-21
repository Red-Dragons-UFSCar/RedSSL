import numpy as np
from entities.Robot import Robot
from entities.Target import (
    Target,
)


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
