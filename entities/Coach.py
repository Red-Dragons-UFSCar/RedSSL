from behavior.skills import *
from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import numpy as np
import time
from behavior.plays import estrategia_basica, estrategia_penalti_defensivo, estrategia_penalti_ofensivo
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
        self.penalty_start_time = None
        self.penalty_mode = None
        self.tempo_de_cobranca = 10 

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
        
    def situacao_de_penalti(self, referee_penalty):
        """
        verificar se é uma situação de penalti 
        """
        if referee_penalty == 0:
            return False
        else:
            if referee_penalty == 2: #penalti ofensivo
                self.penalty_mode = 2 #modo de penalty ofensivo
            else: 
                if referee_penalty == 1: #penalti defensivo
                    self.penalty_mode = 1 #modo de penalty defensivo
            return True

    def escolher_estrategia(self, robot_goleiro, robot_zagueiro, robot_atacante):
        """
        Escolhe e executa a estratégia baseada na situação do jogo.
        """
        if not self.verificar_bola_em_campo():
            # Se o jogo estiver parado, move os robôs para pontos específicos
            print("Jogo parado. Posicionando robôs.")
            posicionar_robos(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
        else:
            # Se o jogo estiver em andamento, usa a estratégia básica
            if self.game_on:
                if self.situacao_de_penalti(0):   # passando os valores manualmente para testes. 0 não ha penalti, 1, penalti defensivo, 2 ofensivo.
                    if self.penalty_start_time is None:
                        self.penalty_start_time = time.time() #assume tempo atual
            
                    #improviso apito do juiz
                    tempo_decorrido = time.time() - self.penalty_start_time
                    if tempo_decorrido <= self.tempo_de_cobranca:
                        referee_whistle = 0
                    else: 
                        referee_whistle = 1 


                    if self.penalty_mode == 1: 
                        print ("estratégia de penalti defensivo em ação")
                        estrategia_penalti_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, self.field, referee_whistle)
                    else:
                        if self.penalty_mode == 2: 
                            print ("estratégia de penalti ofensivo em ação")
                            estrategia_penalti_ofensivo(robot_goleiro, robot_zagueiro, robot_atacante, self.field, referee_whistle)
                        else: 
                            self.penalty_start_time = None # "zerando" tempo de incio do penalti após a cobrança
                else:
                    print("Estrategia basica em açao")
                    estrategia_basica(robot_goleiro, robot_zagueiro, robot_atacante, self.field)