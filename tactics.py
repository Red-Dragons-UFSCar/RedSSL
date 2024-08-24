from behavior.skills import *
from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import numpy as np
import time

def Goalie(robot0, field):

    Goalie_Chase_line = 140 #limite para considerar perto
    Goaie_Y_Enable = 300 #quando o goleiro começa a perseguir a bola

    # posição atual da bola
    ball_position = field.ball.get_coordinates()
   

    # Verifica se a bola está pŕoxima à área
    if (ball_position.X <= Goalie_Chase_line) and (150< ball_position.Y<450):
        # A bola está perto da area 
        Basic_Tackle(robot0, field) #vai atras 

    else:
        if (ball_position.X <= Goaie_Y_Enable):
            # A bola não está na área, mas está perto
            follow_ball_y(robot0, field) #foca em y
            
        else: 
            #a bola não está perto o suficiente para o goleiro precisar se preocupar, então manda ele pro centor do gol
            #poupar bateria e motor (não sei se é tão relevante assim)
            Stay_On_Center(robot0, field) #manda pro centro
