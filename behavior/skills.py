import math
import numpy as np

def go_to_point(robot0, target_x, target_y, field, target_theta):
    """
    Move o robô para as coordenadas especificadas.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo (opcional).

    Descrição:
    O robô é movido para o ponto alvo definido por `target_x` e `target_y` no campo.
    O ângulo de orientação do robô pode ser ajustado com `target_theta`.
    """
    # Define o alvo e atualiza o mapa de obstáculos
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)

    # Atualiza o controle PID e define a velocidade do robô
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )

    # Para o robô ao atingir o alvo
    if robot0.target_reached():
        robot0.vx = 0
        robot0.vy = 0

def follow_ball_y(robot0, field, target_x):
    """
    Move o robô para seguir a bola ao longo do eixo Y, mantendo uma posição fixa no eixo X.

    Parâmetros:
    - robot0: O robô que será controlado.
    - field: O campo de jogo, incluindo a bola e outros robôs.
    - target_x: A posição X que o robô deve manter ao longo do eixo Y.

    Descrição:
    A função faz com que o robô siga a bola ao longo do eixo Y, mantendo uma posição fixa no eixo X.
    Pode ser usada tanto para seguir a bola na área do goleiro quanto para seguir a bola no lado ofensivo do campo.
    """
    ball_position = field.ball.get_coordinates()
    target_y = ball_position.Y

    go_to_point(robot0, target_x, target_y, field, 0)

def attack_ball(robot0, field):
    """
    Alinha o robô para atacar a bola, movendo-o para uma posição estratégica para empurrar a bola para o lado ofensivo.

    Parâmetros:
    - robot0: O robô que será controlado.
    - field: O campo de jogo, incluindo a bola e outros robôs.

    Descrição:
    A função calcula a posição da bola e alinha o robô de forma que ele possa atacar a bola
    e empurrá-la para o lado ofensivo do campo.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    angle_to_ball = np.arctan2(delta_y, delta_x)

    # Verifica o alinhamento do robô com a bola
    robot_rotation = robot_position.rotation
    rotation_diff = abs(robot_rotation - angle_to_ball)

    if -(np.pi)/6 < angle_to_ball < (np.pi)/6:
        # O robô está alinhado para atacar
        target_x = ball_position.X
        target_y = ball_position.Y
    else:
        # O robô se posiciona para atacar por trás da bola
        approach_offset = -50  # Define uma posição atrás da bola
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y
        target_theta = angle_to_ball  # Ajusta a orientação para alinhar com a bola

        # Ajusta o alvo para evitar a bola no 3º ou 4º quadrante
        if 90 <= np.degrees(angle_to_ball) <= 180:
            target_y -= 35
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 35

    go_to_point(robot0, target_x, target_y, field, target_theta)

def pursue_ball(robot0, field):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.

    Parâmetros:
    - robot0: O robô que será controlado.
    - field: O campo de jogo, incluindo a bola e outros robôs.

    Descrição:
    Se a bola estiver na área do goleiro, move o robô ao longo do eixo Y com X fixo em 130.
    Caso contrário, o robô é alinhado para atacar a bola ou se posicionar para um ataque.
    """
    ball_position = field.ball.get_coordinates()

    # Verifica se a bola está na área do goleiro
    if ball_position.X <= 278 and 228 <= ball_position.Y <= 370:
        # Segue a bola na área do goleiro
        follow_ball_y(robot0, field, target_x=292)
        print("Bola na área do goleiro, seguindo ao longo do eixo Y...")
    else:
        # Ataca ou se posiciona para atacar a bola
        attack_ball(robot0, field)