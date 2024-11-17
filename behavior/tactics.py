from behavior import skills
from entities.Robot import Robot
from entities.Target import Target
from entities.Obstacle import Obstacle
from path.visibilityGraph import VisibilityGraph
import random
import numpy as np
from commons import math
import time


def goleiro(robot0, field):

    Goalie_Chase_line = 75  # Limite para considerar perto
    Goaie_Y_Enable = 300  # Quando o goleiro começa a perseguir a bola

    # Posição atual da bola
    ball_position = field.ball.get_coordinates()

    # Verifica se a bola está pŕoxima à área
    if (ball_position.X <= Goalie_Chase_line) and (90 < ball_position.Y < 210):
        # A bola está perto da area
        skills.basic_tackle(robot0, field)  # vai atras

    else:
        if ball_position.X <= Goaie_Y_Enable:
            # A bola não está na área, mas está perto
            skills.follow_ball_y_elipse(robot0, field)  # foca em y

        else:
            # a bola não está perto o suficiente para o goleiro precisar se preocupar, então manda ele pro centor do gol
            # poupar bateria e motor (não sei se é tão relevante assim)
            skills.stay_on_center(
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
        skills.follow_ball_y(robot0, field)
    else:
        skills.pursue_ball(robot0, field)


def atacante(robot0, field):
    ball_position = field.ball.get_coordinates()

    for robot_field in field.enemy_robots:
        obst = Obstacle()
        obst.set_obst(robot_field.get_coordinates().X, 
                      robot_field.get_coordinates().Y, 
                      robot_field.get_coordinates().rotation)
        robot0.map_obstacle.add_obstacle(obst)
    
    if (400 < ball_position.X <= 450) and (87.5 <= ball_position.Y <= 222.5):
        skills.follow_ball_y(robot0, field, 380)
    elif ball_position.X < 225:
        skills.follow_ball_y(robot0, field, 300)
    else:
        skills.shoot(robot0, field)

# def atacante_campo_todo(robot0, field):
#     ball_position = field.ball.get_coordinates()

#     for robot_field in field.enemy_robots:
#         obst = Obstacle()
#         obst.set_obst(robot_field.get_coordinates().X, 
#                       robot_field.get_coordinates().Y, 
#                       robot_field.get_coordinates().rotation)
#         robot0.map_obstacle.add_obstacle(obst)
    
#         skills.shoot(robot0, field)

def atacante_campo_todo(robot0, field):
    ball_position = field.ball.get_coordinates()

    for robot_field in field.enemy_robots:
        obst = Obstacle()
        obst.set_obst(robot_field.get_coordinates().X, 
                      robot_field.get_coordinates().Y, 
                      robot_field.get_coordinates().rotation)
        robot0.map_obstacle.add_obstacle(obst)
    
    if (ball_position.X > 390) and (70 <= ball_position.Y <= 240):
        skills.follow_ball_y(robot0, field, 380)
    elif (ball_position.X < 70) and (70 <= ball_position.Y <= 240):
        skills.follow_ball_y(robot0, field, 100)
    else:
        skills.attack_ball_fisico(robot0, field, robot0.robot_id)
      

def atacante_real(robot0, field):
    ball_position = field.ball.get_coordinates()

    for robot_field in field.enemy_robots:
        obst = Obstacle()
        obst.set_obst(robot_field.get_coordinates().X, 
                      robot_field.get_coordinates().Y, 
                      robot_field.get_coordinates().rotation)
        robot0.map_obstacle.add_obstacle(obst)
    
    if field.atacante_current_state[robot0.robot_id] == 'STATE_B':
        area_defense = 370
    else:
        area_defense = 390

    if (ball_position.X > 390) and (70 <= ball_position.Y <= 240):
        skills.follow_ball_y(robot0, field, 380)
    elif ball_position.X < 210:
        skills.follow_ball_y(robot0, field, 300)
    else:
        skills.attack_ball_fisico(robot0, field, robot0.robot_id)

def zagueiro_real(robot0, field):
    """
    Função que controla o comportamento do robô zagueiro.
    O robô segue a bola no eixo Y quando a bola está no ataque,
    e persegue a bola com alinhamento ofensivo quando está na defesa.
    """
    offensive_line_x = 225.00  # Meio de campo
    ball_position = field.ball.get_coordinates()

    if ball_position.X >= offensive_line_x:
        skills.follow_ball_y(robot0, field, 150)
        print("eu to tentando seguir 1")
        print("Target: ", robot0.target.get_coordinates().X)
    elif (ball_position.X < 70) and (70 <= ball_position.Y <= 240):
        skills.follow_ball_y(robot0, field, 100)
        print("eu to tentando seguir")
    else:
        skills.attack_ball_fisico(robot0, field, robot0.robot_id)

def goleiro_real(robot0, field):

    Goalie_Chase_line = 75  # Limite para considerar perto
    Goaie_Y_Enable = 300  # Quando o goleiro começa a perseguir a bola

    # Posição atual da bola
    ball_position = field.ball.get_coordinates()

    # Verifica se a bola está pŕoxima à área
    if (ball_position.X <= Goalie_Chase_line) and (90 < ball_position.Y < 210):
        # A bola está perto da area
        skills.basic_tackle(robot0, field)  # vai atras

    else:
        if ball_position.X <= Goaie_Y_Enable:
            # A bola não está na área, mas está perto
            skills.follow_ball_y_elipse(robot0, field)  # foca em y

        else:
            # a bola não está perto o suficiente para o goleiro precisar se preocupar, então manda ele pro centor do gol
            # poupar bateria e motor (não sei se é tão relevante assim)
            skills.stay_on_center(
                robot0, field
            )  # manda pro centrofrom behavior.skills import follow_ball_y, pursue_ball

def goleiro_real_2(robot0, field):

    Goalie_Chase_line = 75  # Limite para considerar perto
    Goaie_Y_Enable = 420  # Quando o goleiro começa a perseguir a bola

    # Posição atual da bola
    ball_position = field.ball.get_coordinates()


    if ball_position.X <= Goaie_Y_Enable:
        # A bola não está na área, mas está perto
        skills.follow_ball_y(robot0, field, 22, lim_sup=200, lim_inf=100)  # foca em y

    else:
        # a bola não está perto o suficiente para o goleiro precisar se preocupar, então manda ele pro centor do gol
        # poupar bateria e motor (não sei se é tão relevante assim)
        skills.stay_on_center(
            robot0, field
        )  # manda pro centrofrom behavior.skills import follow_ball_y, pursue_ball
