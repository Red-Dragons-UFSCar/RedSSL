from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import numpy as np
import time


def quadradinho(robot0, robots, enemy_robots, vg):
    """
    Função para atualizar o alvo do robô em um percurso quadrado, considerando o desvio de obstáculos.

    Parâmetros:
    - robot0: Instância do robô atual.
    - robots: Lista de outros robôs aliados.
    - enemy_robots: Lista de robôs inimigos.
    - vg: Instância do vetor de gradiente para desvio de obstáculos.
    """

    # Definição dos alvos para cada eixo coordenado
    x_target = [100, 100, 600, 600]
    y_target = [500, 100, 100, 500]
    theta_target = [-np.pi / 2, 0, np.pi / 2, np.pi]

    # Função interna para atualizar o índice do alvo do robô
    def atualizar_target(robot0, x_target, y_target):
        n_points = len(x_target)
        target_distance = np.sqrt(
            (robot0.get_coordinates().X - x_target[robot0.cont_target]) ** 2
            + (robot0.get_coordinates().Y - y_target[robot0.cont_target]) ** 2
        )

        # Se a distância ao alvo atual for menor que 10, passa para o próximo alvo
        if target_distance < 10:
            robot0.cont_target = (robot0.cont_target + 1) % n_points

    # Função interna para calcular o próximo alvo, considerando desvio de obstáculos
    def calcular_target(
        robot0, x_target, y_target, theta_target, robots, enemy_robots, vg
    ):
        # Atualiza o alvo atual se necessário
        atualizar_target(robot0, x_target, y_target)

        # Calcula o próximo alvo considerando desvio de obstáculos
        next_target = vg.update_target_with_obstacles(
            robot0,
            robots,
            enemy_robots,
            x_target[robot0.cont_target],
            y_target[robot0.cont_target],
            robot0.cont_target,
        )

        # Garantir que o next_target inclua o theta
        next_target_with_theta = np.array(
            [next_target[0], next_target[1], theta_target[robot0.cont_target]]
        )

        return next_target_with_theta

    # Calcula o próximo alvo e atualiza o alvo do robô
    next_target = calcular_target(
        robot0, x_target, y_target, theta_target, robots, enemy_robots, vg
    )
    robot0.set_target(next_target)


def go_to(
    robot0, target_x, target_y, robots, enemy_robots, visibility_graph, target_theta=0
):
    """
    Move o robô para as coordenadas especificadas e para quando o alvo é alcançado.

     Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - robots: Lista de robôs (incluindo o robô0).
    - enemy_robots: Lista de robôs inimigos.
    - visibility_graph: Instância da classe VisibilityGraph.
    - target_theta: Ângulo alvo (opcional).
    """

    target = visibility_graph.update_target_with_obstacles(
        robot0, robots, enemy_robots, [target_x], [target_y], 0
    )
    robot0.set_target(target)
    (
        target_x,
        target_y,
    ) = target

    # Atualiza o controle PID e define a velocidade do robô
    vx, vy, w = robot0.set_robot_velocity(target_x, target_y, target_theta)

    # Opcional: Retorna as velocidades para depuração ou controle adicional
    return vx, vy, w
