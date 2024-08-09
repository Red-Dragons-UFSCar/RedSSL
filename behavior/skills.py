from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import math
import numpy as np
import time


def follow_ball_y(robot0, field, target_theta=0):
    """
    Move o robô para seguir a bola ao longo do eixo Y,
    mas apenas se a bola estiver no lado ofensivo do campo.
    """
    ball_position = field.ball.get_coordinates()
    target_x = 368  # Fixa posição X do robô em 133
    target_y = ball_position.Y

    # Define o alvo e atualiza a velocidade do robô
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )


def pursue_ball(robot0, field, target_theta=0):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    angle_to_ball = np.arctan2(delta_y, delta_x)

    if ball_position.X >= 0:
        target_theta = angle_to_ball
    else:
        target_theta = 0  # Direção ofensiva

    # Define o alvo e atualiza a velocidade do robô
    robot0.target.set_target(robot0, (ball_position.X, ball_position.Y), field, target_theta)
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )