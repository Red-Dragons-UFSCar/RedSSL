from behavior.skills import *
from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import numpy as np
import time
from behavior.plays import estrategia_basica
from behavior.plays import posicionar_robos


class Coach:
    def __init__(self, field):
        """
        Inicializa o Coach com a estratégia inicial e o campo.
        """
        self.estrategia_atual = None
        self.field = field
        self.game_on = True
        self.game_stopped = False

    def verificar_bola_em_campo(self):
        """
        Verifica a posição da bola e determina se ela está fora de campo.
        """
        ball_position = self.field.ball.get_coordinates()

        # Verifica se a bola está fora de campo
        if (
            ball_position.Y > 300
            or ball_position.Y < 0
            or ball_position.X > 450
            or ball_position.X < 0
        ):
            self.game_stopped = True
            self.game_on = False
            return False  # Bola fora de campo
        else:
            self.game_stopped = False
            self.game_on = True
            return True  # Bola dentro de campo

    def escolher_estrategia(self, robot_goalie, robot_zagueiro, robot_atacante):
        """
        Escolhe e executa a estratégia baseada na situação do jogo.
        """
        if not self.verificar_bola_em_campo():
            # Se o jogo estiver parado, move os robôs para pontos específicos
            #print("Jogo parado. Posicionando robôs.")
            posicionar_robos(robot_goalie, robot_zagueiro, robot_atacante, self.field)
        else:
            # Se o jogo estiver em andamento, usa a estratégia básica
            if self.game_on:
                #print("Estrategia basica em açao")
                estrategia_basica(robot_goalie, robot_zagueiro, robot_atacante, self.field)
