from behavior import plays
from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import numpy as np
import time

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
        self.quantidade_robos = 3  # Número de robôs da equipe em campo

        #flags de kickoff
        self.kickoff_attacking = False
        self.kickoff_defensive = False


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
            # self.game_stopped = True
            # self.game_on = False
            return False  # Bola fora de campo
        else:
            # self.game_stopped = False
            # self.game_on = True
            return True  # Bola dentro de campo

    def situacao_de_penalti(self, referee_penalty):
        """
        Verificar se é uma situação de pênalti 
        """
        if referee_penalty == 0:
            return False
        else:
            if referee_penalty == 2: # Pênalti ofensivo
                self.penalty_mode = 2 # Modo de penalty ofensivo
            else: 
                if referee_penalty == 1: # Pênalti defensivo
                    self.penalty_mode = 1 # Modo de penalty defensivo
            return True
        
    def expulsao(self, referee_red_card = 0):
        """
        Altera a quantidade de robôs em campo se um for expulso.

        :param referee_red_card: Flag indicando se um robô foi expulso (True ou False)
        """
        if referee_red_card == 1:  # Se a flag de cartão vermelho for ativada
            if self.quantidade_robos > 1:  # Verifica se ainda há mais de um robô em campo
                self.quantidade_robos -= 1  # Remove um robô do campo
                print(f"Um robô foi expulso. Restam {self.quantidade_robos} robôs.")
            else:
                print("Não é possível expulsar mais robôs, só resta um em campo.")
        else:
            print("Nenhum robô foi expulso.")


    def escolher_estrategia(self, robot_goleiro, robot_zagueiro, robot_atacante):
        """
        Escolhe e executa a estratégia baseada na situação do jogo.
        """
        if self.field.game_stopped:
            robot_goleiro.v_max = 0.75
            robot_zagueiro.v_max = 0.75
            robot_atacante.v_max = 0.75
        else:
            robot_goleiro.v_max = 1.5
            robot_zagueiro.v_max = 1.5
            robot_atacante.v_max = 1.5

        if not self.verificar_bola_em_campo():
            # Se o jogo estiver parado, move os robôs para pontos específicos
            # print("Bola Fora. Posicionando robôs.")
            plays.posicionar_robos(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
        else:
            # Se o jogo estiver em andamento, usa a estratégia básica
            if self.game_on:
                if self.situacao_de_penalti(0): # Passando os valores manualmente para testes. 0 não há pênalti, 1, pênalti defensivo, 2 ofensivo.
                    if self.penalty_start_time is None:
                        self.penalty_start_time = time.time() # Assume tempo atual
            
                    #improviso apito do juiz
                    tempo_decorrido = time.time() - self.penalty_start_time
                    if tempo_decorrido <= self.tempo_de_cobranca:
                        referee_whistle = 0
                    else:
                        referee_whistle = 1

                    if self.penalty_mode == 1:
                        # print ("estratégia de pênalti defensivo em ação")
                        plays.estrategia_penalti_defensivo(
                            robot_goleiro,
                            robot_zagueiro,
                            robot_atacante,
                            self.field,
                            referee_whistle,
                        )
                    else:
                        if self.penalty_mode == 2: 
                            # print ("estratégia de pênalti ofensivo em ação")
                            plays.estrategia_penalti_ofensivo(robot_goleiro, robot_zagueiro, robot_atacante, self.field, referee_whistle)
                        else: 
                            self.penalty_start_time = None # "Zerando" tempo de incio do pênalti após a cobrança
                
                elif self.quantidade_robos == 2:
                    # print("Estratégia com 1 robôs a menos em ação")
                    plays.estrategia_desvantagem_2(robot_goleiro, robot_zagueiro, robot_atacante, self.field)

                elif self.quantidade_robos == 1:
                    # print("Estratégia com 2 robôs a menos em ação")
                    plays.estrategia_desvantagem_1(robot_goleiro, robot_zagueiro, robot_atacante, self.field)

                else:
                    # print("Estrategia basica em ação")
                    plays.estrategia_basica(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
                    
            elif self.field.game_stopped and self.field.defending_foul:
                # Estratégia de jogo parado em stop defensivo
                # Faz a estratégia normal e desvia da bola
                plays.basic_stop_behavior_defensive(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif self.field.game_stopped and self.field.offensive_foul:
                # Estratégia de jogo parado em stop ofensivo
                # Calcula o angulo desejado da estrategia normal, mas para perto da bola
                plays.basic_stop_behavior_offensive(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )
            
            elif self.kickoff_attacking:
                # Estratégia de kickoff ofensivo
                plays.offensive_kickoff(robot_goleiro, robot_zagueiro, robot_atacante, self.field)

            elif self.kickoff_defensive:
                # Estratégia de kickoff defensivo
                plays.defensive_kickoff(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
