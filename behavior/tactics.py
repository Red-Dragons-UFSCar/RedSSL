from behavior.skills import *
from entities.Robot import Robot
from entities.Target import Target
from entities.Obstacle import Obstacle
from path.visibilityGraph import VisibilityGraph
import random
import numpy as np
from commons import math
import time


def goleiro(robot0, field):
    
    Goalie_Chase_line = 75  # limite para considerar perto
    Goalie_Y_Enable = 300  # quando o goleiro começa a perseguir a bola

    # posição atual da bola
    ball_position = field.ball.get_coordinates()

    # Verifica se a bola está próxima à área
    if (ball_position.X <= Goalie_Chase_line) and (90 < ball_position.Y < 210):
        # A bola está perto da área
        basic_tackle(robot0, field)  # vai atrás da bola
    else:
        if ball_position.X <= Goalie_Y_Enable:
            # A bola não está na área, mas está perto
            follow_ball_y_elipse(robot0, field)  # foca em Y
        else:
            # A bola não está perto o suficiente para o goleiro se preocupar, então manda ele para o centro do gol
            stay_on_center(robot0, field)  # manda pro centro do gol


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

    # Acessando o Coach e o robô atacante
    from entities.Coach import Coach
    coach = Coach(field)
    robot_atacante = coach.robot_atacante

    # Obtendo a velocidade máxima do robô atacante
    v_max = robot_atacante.v_max

    # Adicionando os obstáculos ao mapa do robô
    for robot_field in field.yellow_robots:
        obst = Obstacle()
        obst.set_obst(robot_field.get_coordinates().X, 
                      robot_field.get_coordinates().Y, 
                      robot_field.get_coordinates().rotation)
        robot0.map_obstacle.add_obstacle(obst)
    
    # Decisões de comportamento do atacante com base na posição da bola
    if (400 < ball_position.X <= 450) and (87.5 <= ball_position.Y <= 222.5):
        follow_ball_y(robot0, field, 380)
    elif ball_position.X < 225:
        follow_ball_y(robot0, field, 300)
    else:
        shoot(robot0, field, v_max)