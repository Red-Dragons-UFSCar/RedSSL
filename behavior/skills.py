import math
import numpy as np

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
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )

    if robot0.target_reached():
        robot0.vx = 0
        robot0.vy = 0

def follow_ball_y(robot0, field, fixed_x=None, target_theta=0):
    """
    Move o robô para seguir a bola ao longo do eixo Y, mantendo uma posição fixa no eixo X ou na área do goleiro.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - fixed_x: Coordenada X fixa (opcional).
    - target_theta: Ângulo alvo (opcional).
    """
    ball_position = field.ball.get_coordinates()

    target_x = fixed_x if fixed_x is not None else 400  # X padrão é 400, pode ser sobrescrito
    target_y = ball_position.Y

    go_to_point(robot0, target_x, target_y, field, target_theta)

def attack_ball(robot0, field, ball_position, robot_position, angle_to_ball):
    """
    Função para alinhar o robô e atacar a bola de forma estratégica.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - angle_to_ball: Ângulo entre o robô e a bola.
    """
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    angle_to_ball = np.arctan2(delta_y, delta_x)

    robot_rotation = robot_position.rotation
    rotation_diff = abs(robot_rotation - angle_to_ball)

    if -(np.pi)/2.5 < angle_to_ball < (np.pi)/2.5:
        target_x = ball_position.X
        target_y = ball_position.Y
        target_theta = angle_to_ball
    else:
        approach_offset = -50  # Define uma posição atrás da bola
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y
        target_theta = angle_to_ball  # Alinha o robô com a bola

        if 90 <= np.degrees(angle_to_ball) <= 180:
            target_y -= 20
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 20

    go_to_point(robot0, target_x, target_y, field, target_theta)

def pursue_ball(robot0, field):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    if ball_position.X <= 278 and 228 <= ball_position.Y <= 370:
        # A bola está na área do goleiro
        follow_ball_y(robot0, field, fixed_x=292, target_theta=np.pi)
    else:
        # Atacar a bola
        attack_ball(robot0, field, ball_position, robot_position, robot_position.rotation)
