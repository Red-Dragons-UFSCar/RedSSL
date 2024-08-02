from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import numpy as np
import time

def go_to_point(robot0, target_x, target_y, field, target_theta=0):
    """
    Move o robô para as coordenadas especificadas.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo (opcional).
    """

    # Define o alvo (inclui a atualização do mapa de obstáculos)
    robot0.target.set_target(
        robot0, (target_x, target_y), field, target_theta
    )

    # Atualiza o controle PID e define a velocidade do robô
    vx, vy, w = robot0.calculate_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )

    # Opcional: Imprimir as velocidades para depuração
    print(f"Velocidades definidas: vx={vx}, vy={vy}, w={w}")

    # Retorna as velocidades para depuração ou controle adicional
    return vx, vy, w
