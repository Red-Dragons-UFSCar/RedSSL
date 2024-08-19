import math
import numpy as np

def go_to_point(robot0, target_x, target_y, field, target_theta):
    """
    Move o robô para as coordenadas especificadas.
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

def follow_ball_y(robot0, field, target_theta=0):
    """
    Move o robô para seguir a bola ao longo do eixo Y, mantendo uma posição fixa no eixo X.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    angle_to_ball = np.arctan2(delta_y, delta_x)

    target_x = 355  # Fixa a posição X do robô
    target_y = ball_position.Y

    go_to_point(robot0, target_x, target_y, field, angle_to_ball)

def pursue_ball(robot0, field, target_theta=0):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.
    Se a bola estiver na área do goleiro, move o robô ao longo do eixo Y com X fixo em 130.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # Verifica se a bola está na área do goleiro
    if ball_position.X <= 100 and 200 <= ball_position.Y <= 400:
        target_x = 130  # Fixa a posição X do robô
        target_y = ball_position.Y
        print("Bola na área do goleiro, seguindo ao longo do eixo Y...")
    
    else:
        # Calcula o ângulo entre o robô e a bola
        delta_x = ball_position.X - robot_position.X
        delta_y = ball_position.Y - robot_position.Y
        angle_to_ball = np.arctan2(delta_y, delta_x)

        # Define o ângulo desejado de alinhamento para atacar a bola
        robot_rotation = robot_position.rotation
        rotation_diff = abs(robot_rotation - angle_to_ball)

        if -(np.pi)/6 < angle_to_ball < (np.pi)/6 and rotation_diff <= 30:
            # O robô está alinhado para atacar
            #print("Atacar")
            target_x = ball_position.X
            target_y = ball_position.Y
            #target_theta = robot_rotation  # Mantém o ângulo atual
        else:
            # O robô se posiciona para atacar por trás da bola
            #print("Posicionar")
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
