from behavior.skills import *
from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import random
import numpy as np
from commons import math
import time


def goalie(robot0, field):

    Goalie_Chase_line = 75  # limite para considerar perto
    Goaie_Y_Enable = 300  # quando o goleiro começa a perseguir a bola

    # posição atual da bola
    ball_position = field.ball.get_coordinates()

    # Verifica se a bola está pŕoxima à área
    if (ball_position.X <= Goalie_Chase_line) and (90 < ball_position.Y < 210):
        # A bola está perto da area
        basic_tackle(robot0, field)  # vai atras

    else:
        if ball_position.X <= Goaie_Y_Enable:
            # A bola não está na área, mas está perto
            follow_ball_y_elipse(robot0, field)  # foca em y

        else:
            # a bola não está perto o suficiente para o goleiro precisar se preocupar, então manda ele pro centor do gol
            # poupar bateria e motor (não sei se é tão relevante assim)
            stay_on_center(
                robot0, field
            )  # manda pro centrofrom behavior.skills import follow_ball_y, pursue_ball


def zagueiro(robot0, field):
    """
    Função que controla o comportamento do robô zagueiro.
    O robô segue a bola no eixo Y quando a bola está no ataque,
    e persegue a bola com alinhamento ofensivo quando está na defesa.
    """
    offensive_line_x = 225.00  # Meio de campo
    ball_position = field.ball.get_coordinates()

    if ball_position.X >= offensive_line_x:
        follow_ball_y(robot0, field)
    else:
        pursue_ball(robot0, field)


def atacante(robot0, field):
    ball_position = field.ball.get_coordinates()
    if (
        (400 < ball_position.X <= 450) and (87.5 <= ball_position.Y <= 222.5)
    ) or ball_position.X < 225:
        follow_ball_y(robot0, field, 380)
    else:
        shoot(robot0, field)

    #avoid_ball_stop_game_defending(robot0, field)
