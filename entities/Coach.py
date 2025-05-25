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
        self.game_on = False
        self.game_stopped = True
        self.game_halted = False
        self.penalty_start_time = None
        self.penalty_mode = None
        self.tempo_cobranca = 10
        self.quantidade_robos = 3  # Número de robôs da equipe em campo

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
            return False  # Bola fora de campo
        else:
            return True  # Bola dentro de campo

    def expulsao(self):
        """
        Altera a quantidade de robôs em campo se um for expulso.

        :param referee_red_card: Flag indicando se um robô foi expulso (True ou False)
        """
        if self.field.red_card_flag == True:  # Se a flag de cartão vermelho for ativada
            if (
                self.quantidade_robos > 1
            ):  # Verifica se ainda há mais de um robô em campo
                self.quantidade_robos -= 1  # Remove um robô do campo
                print(f"Um robô foi expulso. Restam {self.quantidade_robos} robôs.")
            else:
                print("Não é possível expulsar mais robôs, só resta um em campo.")
        else:
            pass

    def escolher_estrategia(self, robot_goleiro, robot_zagueiro, robot_atacante):
        """
        Escolhe e executa a estratégia baseada na situação do jogo.
        """

        if self.field.game_halted:
            # Estratégia para quando o jogo está pausado permanentemente (halted)
            robot_goleiro.v_max = 0
            robot_zagueiro.v_max = 0
            robot_atacante.v_max = 0
            return  # Sai da função para garantir que os robôs permaneçam parados

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
            plays.posicionar_robos(
                robot_goleiro, robot_zagueiro, robot_atacante, self.field
            )
        else:

            # Se o jogo estiver em andamento, usa a estratégia básica
            if self.field.game_on and self.field.game_on_is_penalty == False:

                if self.field.allowed_robots == 0:
                    plays.estrategia_desvantagem_0(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

                elif self.field.allowed_robots == 1:
                    plays.estrategia_desvantagem_1(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

                elif self.field.allowed_robots == 2:
                    plays.estrategia_desvantagem_2(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

                elif self.field.allowed_robots == 3:
                    # Estrategia basica em ação
                    plays.estrategia_basica(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

            elif self.field.game_on and self.field.game_on_is_penalty == True:
                if self.penalty_start_time is None:
                    self.penalty_start_time = time.time()

                if self.field.penalty_defensive:
                    print("estratégia de pênalti defensivo em ação")
                    plays.estrategia_penalty_defensivo(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )
                else:
                    if self.field.penalty_offensive:
                        print("estratégia de pênalti ofensivo em ação")
                        plays.estrategia_penalty_ofensivo(
                            robot_goleiro, robot_zagueiro, robot_atacante, self.field
                        )
                    else:
                        self.penalty_start_time = (
                            None  # "Zerando" tempo de incio do pênalti após a cobrança
                        )

            elif (
                self.field.game_stopped
                and self.field.defending_foul
                and self.field.allowed_robots == 0
            ):

                plays.basic_stop_behavior_defensive_desvantagem0(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif (
                self.field.game_stopped
                and self.field.defending_foul
                and self.field.allowed_robots == 1
            ):

                plays.basic_stop_behavior_defensive_desvantagem1(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif (
                self.field.game_stopped
                and self.field.defending_foul
                and self.field.allowed_robots == 2
            ):

                plays.basic_stop_behavior_defensive_desvantagem2(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif (
                self.field.game_stopped
                and self.field.defending_foul
                and self.field.allowed_robots == 3
            ):
                plays.basic_stop_behavior_defensive(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif (
                self.field.game_stopped
                and self.field.offensive_foul == True
                and self.field.allowed_robots == 0
            ):
                # Estratégia de jogo parado em stop defensivo
                # Faz a estratégia normal e desvia da bola
                plays.basic_stop_behavior_offensive_desvantagem_0(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif (
                self.field.game_stopped
                and self.field.offensive_foul == True
                and self.field.allowed_robots == 1
            ):
                # Estratégia de jogo parado em stop defensivo
                # Faz a estratégia normal e desvia da bola
                plays.basic_stop_behavior_offensive_desvantagem_1(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif (
                self.field.game_stopped
                and self.field.offensive_foul == True
                and self.field.allowed_robots == 2
            ):
                # Estratégia de jogo parado em stop defensivo
                # Faz a estratégia normal e desvia da bola
                plays.basic_stop_behavior_offensive_desvantagem_2(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif (
                self.field.game_stopped
                and self.field.offensive_foul == True
                and self.field.allowed_robots == 3
            ):
                # Estratégia de jogo parado em stop defensivo
                # Faz a estratégia normal e desvia da bola
                plays.basic_stop_behavior_offensive(
                    robot_goleiro, robot_zagueiro, robot_atacante, self.field
                )

            elif self.field.kickoff_offensive:
                if self.field.allowed_robots == 3:
                    # Estratégia de kickoff ofensivo
                    plays.offensive_kickoff(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

                elif self.field.allowed_robots == 2:
                    plays.offensive_kickoff_2(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

                elif self.field.allowed_robots == 1:
                    plays.offensive_kickoff_1(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

            elif self.field.kickoff_defensive:
                if self.field.allowed_robots == 3:
                    # Estratégia de kickoff ofensivo
                    plays.defensive_kickoff(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

                elif self.field.allowed_robots == 2:
                    plays.defensive_kickoff_2(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

                elif self.field.allowed_robots == 1:
                    plays.defensive_kickoff_1(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )

            elif self.field.penalty_offensive or self.field.penalty_defensive:
                if self.penalty_start_time is None:
                    self.penalty_start_time = time.time()

                if self.field.penalty_defensive:
                    print("estratégia de pênalti defensivo em ação")
                    plays.estrategia_penalty_defensivo(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )
                else:
                    if self.field.penalty_offensive:
                        print("estratégia de pênalti ofensivo em ação")
                        plays.estrategia_penalty_ofensivo(
                            robot_goleiro, robot_zagueiro, robot_atacante, self.field
                        )
                    else:
                        self.penalty_start_time = (
                            None  # "Zerando" tempo de incio do pênalti após a cobrança
                        )
    
    def escolher_estrategia_real_2(self, robot_goleiro, robot_zagueiro, robot_atacante):
        """
        Escolhe e executa a estratégia baseada na situação do jogo.
        """

        # if self.field.game_halted:
        #     # Estratégia para quando o jogo está pausado permanentemente (halted)
        #     robot_goleiro.v_max = 0
        #     robot_zagueiro.v_max = 0
        #     robot_atacante.v_max = 0
        #     return  # Sai da função para garantir que os robôs permaneçam parados

        # if self.field.game_stopped:
        #     robot_goleiro.v_max = 0.75
        #     robot_zagueiro.v_max = 0.75
        #     robot_atacante.v_max = 0.75
        # else:
        #     robot_goleiro.v_max = 1.5
        #     robot_zagueiro.v_max = 1.5
        #     robot_atacante.v_max = 1.5

        if self.field.game_on:
            if self.field.allowed_robots <= 1:
                plays.estrategia_basica_real_1robo(
                            robot_goleiro, robot_zagueiro, robot_atacante, self.field
                        )
                print("Estratégia: Desvantagem")
            else:
                #plays.estrategia_basica_real(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
                plays.estrategia_block_ball_real(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
                #plays.estrategia_2_atacantes_real(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
                print("Estratégia: Normal")
        elif self.field.game_halted:
            robot_goleiro.vx = 0
            robot_goleiro.vy = 0
            robot_goleiro.w = 0

            robot_zagueiro.vx = 0
            robot_zagueiro.vy = 0
            robot_zagueiro.w = 0

            robot_atacante.vx = 0
            robot_atacante.vy = 0
            robot_atacante.w = 0

        elif self.field.kickoff_defensive or self.field.kickoff_offensive:
            print("Kickoff")
            plays.defensive_kickoff(robot_goleiro, robot_zagueiro, robot_atacante, self.field)
        elif self.field.penalty_defensive:
            plays.penalty_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, self.field, self.field.game_on_is_penalty)
        elif self.field.penalty_offensive:
            plays.penalty_ofensivo(robot_goleiro, robot_zagueiro, robot_atacante, self.field, self.field.game_on_is_penalty)
        else:
            plays.basic_stop_behavior_defensive(
                        robot_goleiro, robot_zagueiro, robot_atacante, self.field
                    )
