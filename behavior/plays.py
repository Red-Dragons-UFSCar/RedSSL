from behavior import skills, tactics
from entities.Obstacle import Obstacle
import numpy as np


def estrategia_basica(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """
    tactics.goleiro(robot_goalie, field)
    tactics.zagueiro(robot_zagueiro, field)
    tactics.atacante(robot_atacante, field)

def estrategia_basica_real(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """
    tactics.goleiro_real_2(robot_goalie, field)
    tactics.zagueiro_real(robot_zagueiro, field)
    #skills.block_ball_y(robot_zagueiro, field, fixed_x=70)
    tactics.atacante_real(robot_atacante, field)
    #tactics.atacante_campo_todo(robot_atacante, field)

def estrategia_block_ball_real(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """

    fixed_point = 80
    tactics.goleiro_real_2(robot_goalie, field, fixed=10)
    skills.block_ball_y(robot_zagueiro, field, fixed_x=fixed_point)
    tactics.atacante_campo_todo_real(robot_atacante, field)

    ball_position = field.ball.get_coordinates()

def estrategia_2_atacantes_real(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """
    tactics.goleiro_real_2(robot_goalie, field, fixed=22)
    tactics.atacante_campo_todo_real(robot_zagueiro, field)
    tactics.atacante_campo_todo_real(robot_atacante, field)

def estrategia_basica_real_1robo(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """
    tactics.atacante_campo_todo(robot_atacante, field)


def posicionar_robos(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Posiciona os robôs em pontos específicos quando o jogo está parado.
    """
    # Defina as posições específicas para os robôs quando o jogo está parado
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, 0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.go_to_point(robot_zagueiro, 150, 150, field, 0)

    # print("Posicionando robô atacante no ponto específico.")
    skills.go_to_point(robot_atacante, 300, 150, field, 0)


def estrategia_penalty_ofensivo(robot_goleiro, robot_zagueiro, robot_atacante, field):

    if field.penalty_offensive == True and field.game_on_is_penalty == False:
        """
        Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
        o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
        """

        skills.penalty_idle_offensive(
            robot_goleiro, robot_zagueiro, robot_atacante, field
        )

    else:
        # chamando a função de atacante para cobrança do penalty.
        tactics.atacante(robot_atacante, field)
        skills.penalty_idle_offensive_game_on(robot_goleiro, robot_zagueiro, field)


def estrategia_penalty_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
    o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
    """
    if field.penalty_defensive == True and field.game_on_is_penalty == False:
        # Se o jogo estiver no modo penalty parado, preparacao do penalty

        skills.penalty_idle_defensive(
            robot_goleiro, robot_zagueiro, robot_atacante, field
        )

    else:
        # Quando o jogo ativar, todos se posicionam para o jogo normal
        tactics.goleiro(robot_goleiro, field)
        skills.penalty_idle_game_on(robot_zagueiro, robot_atacante, field)


def estrategia_desvantagem_2(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Quando a bola estiver na defesa, um robô se torna goleiro, o outro zagueiro.
    Quando a bola estiver no ataque, o robô que era goleiro se torna zagueiro e o outro atacante.
    """

    tactics.goleiro(robot_goalie, field)
    tactics.atacante_campo_todo(robot_zagueiro, field)
    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)


def estrategia_desvantagem_1(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Quando a bola estiver na defesa, um robô se torna goleiro, o outro zagueiro.
    Quando a bola estiver no ataque, o robô que era goleiro se torna zagueiro e o outro atacante.
    """

    tactics.atacante_campo_todo(robot_goalie, field)
    skills.go_to_point(robot_zagueiro, 120, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)


def estrategia_desvantagem_0(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Quando a bola estiver na defesa, um robô se torna goleiro, o outro zagueiro.
    Quando a bola estiver no ataque, o robô que era goleiro se torna zagueiro e o outro atacante.
    """

    skills.go_to_point(robot_goalie, 120, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_zagueiro, 150, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_atacante, 180, 360, field, np.pi / 2, 2)


def basic_stop_behavior_defensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Descrição: Comportamento básico de stop em casos de faltas defensivas, que
               precisa estar longe da bola. Um jogador cerca a ação da bola e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    tactics.goleiro(robot_goleiro, field)

    if ball.X < 450 / 2 + 30:  # Se a bola está na ação do zagueiro
        skills.projection_stop_target(robot_zagueiro, field)  # Zagueiro vai pra bola
        skills.projection_stop_target(robot_atacante, field)  # Zagueiro vai pra bola

        # # Ponto alvo do atacante no meio campo
        # x_target_atacante = 270
        # y_target_atacante = 150
        # robot_atacante.target.set_target(
        #     robot_atacante, (x_target_atacante, y_target_atacante), field, 0
        # )
        # # Vai até o ponto alvo desviando da bola
        # skills.idle_behavior_avoid_ball_stop_game(robot_atacante, field)

    else:  # Se a bola está na ação do atacante
        skills.projection_stop_target(robot_atacante, field)  # Atacante vai pra bola
        skills.projection_stop_target(robot_zagueiro, field)  # Atacante vai pra bola

        # # Ponto alvo do zagueiro no meio campo
        # x_target_zagueiro = 180
        # y_target_zagueiro = 150
        # robot_zagueiro.target.set_target(
        #     robot_zagueiro, (x_target_zagueiro, y_target_zagueiro), field, 0
        # )
        # # Vai até o ponto alvo desviando da bola
        # skills.idle_behavior_avoid_ball_stop_game(robot_zagueiro, field)


def basic_stop_behavior_defensive_desvantagem2(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Descrição: Comportamento básico de stop em casos de faltas defensivas, que
               precisa estar longe da bola. Um jogador cerca a ação da bola e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    tactics.goleiro(robot_goleiro, field)

    skills.projection_stop_target(robot_zagueiro, field)  # Zagueiro vai pra bola

    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)


def basic_stop_behavior_defensive_desvantagem1(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Descrição: Comportamento básico de stop em casos de faltas defensivas, que
               precisa estar longe da bola. Um jogador cerca a ação da bola e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    skills.projection_stop_target(robot_goleiro, field)  # Goleiro vai pra bola

    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_zagueiro, 180, 360, field, np.pi / 2, 2)


def basic_stop_behavior_defensive_desvantagem0(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Descrição: Comportamento básico de stop em casos de faltas defensivas, que
               precisa estar longe da bola. Um jogador cerca a ação da bola e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_zagueiro, 180, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_goleiro, 120, 360, field, np.pi / 2, 2)


def basic_stop_behavior_offensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Descrição: Comportamento básico de stop em casos de faltas ofensivas, que
               precisa estar longe da bola. . Um jogador vai para a cobrança e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    tactics.goleiro(robot_goleiro, field)

    if ball.X < 450 / 2:  # Se a bola está na ação do zagueiro
        skills.projection_stop_target(
            robot_zagueiro, field, kicker=True
        )  # Zagueiro vai pra bola cobrar

        # Ponto alvo do atacante no meio campo
        x_target_atacante = 300
        y_target_atacante = 150
        robot_atacante.target.set_target(
            robot_atacante, (x_target_atacante, y_target_atacante), field, 0
        )
        # Vai até o ponto alvo desviando da bola
        skills.idle_behavior_avoid_ball_stop_game(robot_atacante, field)
    else:  # Se a bola está na ação do atacante
        skills.projection_stop_target(
            robot_atacante, field, kicker=True
        )  # Atacante vai pra bola cobrar

        # Ponto alvo do zagueiro no meio campo
        x_target_zagueiro = 180
        y_target_zagueiro = 150
        robot_zagueiro.target.set_target(
            robot_zagueiro, (x_target_zagueiro, y_target_zagueiro), field, 0
        )
        # Vai até o ponto alvo desviando da bola
        skills.idle_behavior_avoid_ball_stop_game(robot_zagueiro, field)


def basic_stop_behavior_offensive_desvantagem_2(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Descrição: Comportamento básico de stop em casos de faltas ofensivas, que
               precisa estar longe da bola. . Um jogador vai para a cobrança e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    tactics.goleiro(robot_goleiro, field)

    skills.projection_stop_target(
        robot_zagueiro, field, kicker=True
    )  # Zagueiro vai pra bola cobrar

    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)


def basic_stop_behavior_offensive_desvantagem_1(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Descrição: Comportamento básico de stop em casos de faltas ofensivas, que
               precisa estar longe da bola. . Um jogador vai para a cobrança e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    skills.projection_stop_target(
        robot_goleiro, field, kicker=True
    )  # Zagueiro vai pra bola cobrar

    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_zagueiro, 180, 360, field, np.pi / 2, 2)


def basic_stop_behavior_offensive_desvantagem_0(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Descrição: Comportamento básico de stop em casos de faltas ofensivas, que
               precisa estar longe da bola. . Um jogador vai para a cobrança e
               outro espera no meio campo, a depender da posição da bola
    """
    ball = field.ball.get_coordinates()

    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_zagueiro, 180, 360, field, np.pi / 2, 2)
    skills.go_to_point(robot_goleiro, 120, 360, field, np.pi / 2, 2)


def defensive_kickoff(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff defensivo
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, 0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=False, attacker=False
    )

    # print("Posicionando robô atacante no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_atacante, field, attacking=False, attacker=True
    )


def defensive_kickoff_2(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff defensivo com um robô a menos
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, 0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=False, attacker=True
    )

    # print("Posicionando robô atacante no ponto específico.")
    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)


def defensive_kickoff_1(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff defensivo com um robô a menos
    """
    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_goalie, field, attacking=False, attacker=False
    )

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.go_to_point(robot_zagueiro, 120, 360, field, np.pi / 2, 2)

    # print("Posicionando robô atacante no ponto específico.")
    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)


def offensive_kickoff(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff ofensivo
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, 0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=True, attacker=False
    )

    # print("Posicionando robô atacante no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_atacante, field, attacking=True, attacker=True
    )

    
def defensive_kickoff_real(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff defensivo
    """
    ball = field.ball
    obst = Obstacle()  # Configura a bola como obstáculo
    obst.set_obst(
        ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=30
    )
    robot_goalie.map_obstacle.add_obstacle(obst)
    robot_zagueiro.map_obstacle.add_obstacle(obst)
    robot_atacante.map_obstacle.add_obstacle(obst)
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, 0)
    skills.go_to_point(robot_zagueiro, 100, 150, field, 0)
    skills.go_to_point(robot_atacante, 160, 150, field, 0)

'''
def penalty_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, field, game_on):
    """
    Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
    o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
    """
    if game_on:
        # Quando o jogo ativar, todos se posicionam para o jogo normal
        tactics.goleiro_real_2(robot_goleiro, field)
        skills.go_to_point(robot_zagueiro, 300, 300, field, np.pi)
        skills.go_to_point(robot_atacante, 300, 20, field, np.pi)
    else:
        skills.go_to_point(robot_goleiro, 30, 150, field, np.pi)
        skills.go_to_point(robot_zagueiro, 300, 300, field, np.pi)
        skills.go_to_point(robot_atacante, 300, 20, field, np.pi)
'''
        
def penalty_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, field, game_on):
    """
    Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
    o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
    """
    threshold = 20
    print("eieiei")
    if game_on:
        # Quando o jogo ativar, todos se posicionam para o jogo normal
        tactics.goleiro_real_2(robot_goleiro, field)
        skills.go_to_point(robot_zagueiro, 380, 230, field, np.pi, threshold)
        skills.go_to_point(robot_atacante, 380, 70, field, np.pi, threshold)

        if robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation < 15*np.pi/180:
            robot_zagueiro.w = 0
        if robot_atacante.get_coordinates().rotation - robot_atacante.target.get_coordinates().rotation < 15*np.pi/180:
            robot_atacante.w = 0

    else:
        skills.go_to_point(robot_goleiro, 30, 150, field, 0, threshold)
        skills.go_to_point(robot_zagueiro, 380, 230, field, np.pi, threshold)
        skills.go_to_point(robot_atacante, 380, 70, field, np.pi, threshold)

        if robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation < 15*np.pi/180:
            robot_zagueiro.w = 0
            print("zerei 1")
        if robot_goleiro.get_coordinates().rotation - robot_goleiro.target.get_coordinates().rotation < 15*np.pi/180:
            robot_goleiro.w = 0
            print("zerei 2")
        if robot_atacante.get_coordinates().rotation - robot_atacante.target.get_coordinates().rotation < 15*np.pi/180:
            robot_atacante.w = 0
            print("zerei 3")

def penalty_ofensivo(robot_goleiro, robot_zagueiro, robot_atacante, field, game_on):
    """
    Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
    o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
    """
    if game_on:
        # Quando o jogo ativar, todos se posicionam para o jogo normal
        tactics.atacante_campo_todo(robot_atacante, field)
        skills.go_to_point(robot_zagueiro, 100, 250, field, 0)
        if robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation < 15*np.pi/180:
            robot_zagueiro.w = 0
        skills.go_to_point(robot_goleiro, 30, 150, field, 0)
        if robot_goleiro.get_coordinates().rotation - robot_goleiro.target.get_coordinates().rotation < 15*np.pi/180:
            robot_goleiro.w = 0
    else:
        field.send_local = False
        skills.go_to_point(robot_goleiro, 30, 150, field, 0)
        skills.go_to_point(robot_zagueiro, 100, 250, field, 0)
        skills.go_to_point(robot_atacante, 100, 150, field, 0)

        if robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation < 15*np.pi/180:
            robot_zagueiro.w = 0
        if robot_goleiro.get_coordinates().rotation - robot_goleiro.target.get_coordinates().rotation < 15*np.pi/180:
            robot_goleiro.w = 0
        if robot_atacante.get_coordinates().rotation - robot_atacante.target.get_coordinates().rotation < 15*np.pi/180:
            robot_atacante.w = 0
            

def offensive_kickoff_2(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff ofensivo com um robô a menos
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, 0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=True, attacker=True
    )

    # print("Posicionando robô atacante no ponto específico.")
    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)


def offensive_kickoff_1(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff ofensivo com dois robôs a menos
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_goalie, field, attacking=True, attacker=True
    )

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.go_to_point(robot_zagueiro, 120, 360, field, np.pi / 2, 2)

    # print("Posicionando robô atacante no ponto específico.")
    skills.go_to_point(robot_atacante, 150, 360, field, np.pi / 2, 2)