import math
import numpy as np

def go_to_point(robot0, target_x, target_y, field, target_theta):
    """
    Move o robô para as coordenadas especificadas.
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

def follow_ball_in_goal_area(robot0, ball_position, field):
    """
    Segue a bola ao longo do eixo Y na área do goleiro.
    """
    target_x = 292  # Fixa a posição X do robô na área do goleiro
    target_y = ball_position.Y
    print("Bola na área do goleiro, seguindo ao longo do eixo Y...")
    go_to_point(robot0, target_x, target_y, field, target_theta=0)

def attack_or_position(robot0, ball_position, field, angle_to_ball):
    """
    Ataca a bola ou se posiciona para o ataque, dependendo do alinhamento do robô.
    """
    robot_position = robot0.get_coordinates()
    robot_rotation = robot_position.rotation
    rotation_diff = abs(robot_rotation - angle_to_ball)

    if -(np.pi)/6 < angle_to_ball < (np.pi)/6:
        # O robô está alinhado para atacar
        print("Atacar")
        target_x = ball_position.X
        target_y = ball_position.Y
    else:
        # O robô se posiciona para atacar por trás da bola
        print("Posicionar")
        approach_offset = -50  # Define uma posição atrás da bola
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y

        # Ajusta o alvo para evitar a bola no 3º ou 4º quadrante
        if 90 <= np.degrees(angle_to_ball) <= 180:
            target_y -= 35
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 35

    go_to_point(robot0, target_x, target_y, field, target_theta=angle_to_ball)

def pursue_ball(robot0, field, target_theta=0):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.
    """
    ball_position = field.ball.get_coordinates()

    if ball_position.X <= 278 and 228 <= ball_position.Y <= 370:
        follow_ball_in_goal_area(robot0, ball_position, field)
    else:
        angle_to_ball = np.arctan2(ball_position.Y - robot0.get_coordinates().Y, ball_position.X - robot0.get_coordinates().X)
        attack_or_position(robot0, ball_position, field, angle_to_ball)
