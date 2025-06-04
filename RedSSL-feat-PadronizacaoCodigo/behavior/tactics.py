import random
import time 

import numpy as np

from behavior import skills 
from commons import math as commons_math
from entities.Obstacle import Obstacle
from entities.Robot import Robot 
from entities.Target import Target 
from path.visibilityGraph import VisibilityGraph 


def goleiro(robot0, field):
    """
    Define o comportamento do goleiro.

    O goleiro persegue a bola com `basic_tackle` se ela estiver muito próxima à área do gol.
    Caso contrário, se a bola estiver dentro de um certo limite em X, o goleiro
    usa `follow_ball_y_elipse`. Se a bola estiver longe, o goleiro
    permanece no centro do gol com `stay_on_center`.

    Parâmetros:
    - robot0: A instância do robô goleiro.
    - field: O objeto do campo contendo informações do jogo.
    """
    GOALIE_CHASE_LINE_X = 75  # Limite X para considerar a bola perto da área para perseguição direta.
    GOALIE_Y_TRACK_LIMIT_X = 300  # Limite X para o goleiro começar a seguir a bola em Y com elipse.

    ball_position = field.ball.get_coordinates()

    # Verifica se a bola está muito próxima à área do gol para uma interceptação direta.
    if (ball_position.X <= GOALIE_CHASE_LINE_X) and (
        90 < ball_position.Y < 210  # Faixa Y da área do gol
    ):
        skills.basic_tackle(robot0, field)  # Perseguir a bola diretamente.
    else:
        # Bola não está na zona de perseguição direta.
        if ball_position.X <= GOALIE_Y_TRACK_LIMIT_X:
            # Bola está suficientemente perto para o goleiro acompanhar em Y.
            skills.follow_ball_y_elipse(robot0, field)
        else:
            # Bola está longe; goleiro permanece no centro do gol.
            skills.stay_on_center(robot0, field)


def zagueiro(robot0, field):
    """
    Controla o comportamento do robô zagueiro.

    Se a bola está no campo de ataque (além da linha ofensiva), o zagueiro
    segue a bola no eixo Y. Caso contrário (bola na defesa), o zagueiro
    persegue a bola com alinhamento ofensivo.

    Parâmetros:
    - robot0: A instância do robô zagueiro.
    - field: O objeto do campo contendo informações do jogo.
    """
    OFFENSIVE_LINE_X = 225.0  # Linha do meio de campo.
    ball_position = field.ball.get_coordinates()

    if ball_position.X >= OFFENSIVE_LINE_X: # Bola no campo de ataque
        skills.follow_ball_y(robot0, field)
    else: # Bola no campo de defesa
        skills.pursue_ball(robot0, field)


def atacante(robot0, field):
    """
    Define o comportamento básico do robô atacante.

    Adiciona robôs inimigos como obstáculos. Se a bola estiver próxima ao gol
    adversário, o atacante se posiciona usando `follow_ball_y`. Se a bola
    estiver no campo de defesa, o atacante também usa `follow_ball_y` com um X
    diferente. Caso contrário, tenta chutar com `shoot`.

    Parâmetros:
    - robot0: A instância do robô atacante.
    - field: O objeto do campo contendo informações do jogo.
    """
    ball_position = field.ball.get_coordinates()

    for enemy_robot in field.enemy_robots:
        obst = Obstacle()
        enemy_coords = enemy_robot.get_coordinates()
        obst.set_obst(
            enemy_coords.X, enemy_coords.Y, enemy_coords.rotation
        )
        robot0.map_obstacle.add_obstacle(obst)
    
    # Condições para posicionamento ou chute.
    # Limites da área do gol adversário (aproximados)
    OPPONENT_GOAL_AREA_X_MIN = 400
    OPPONENT_GOAL_AREA_X_MAX = 450 # Largura do campo
    OPPONENT_GOAL_AREA_Y_MIN = 87.5
    OPPONENT_GOAL_AREA_Y_MAX = 222.5
    DEFENSIVE_FIELD_X_LIMIT = 225 # Meio de campo

    if (
        OPPONENT_GOAL_AREA_X_MIN < ball_position.X <= OPPONENT_GOAL_AREA_X_MAX and
        OPPONENT_GOAL_AREA_Y_MIN <= ball_position.Y <= OPPONENT_GOAL_AREA_Y_MAX
    ): # Bola na área do gol adversário
        skills.follow_ball_y(robot0, field, fixed_x=380)
    elif ball_position.X < DEFENSIVE_FIELD_X_LIMIT: # Bola no campo de defesa
        skills.follow_ball_y(robot0, field, fixed_x=300)
    else: # Bola em posição de ataque, fora da área do gol
        skills.shoot(robot0, field)


def atacante_campo_todo(robot0, field):
    """
    Define um comportamento de atacante que cobre o campo todo.

    Adiciona robôs inimigos como obstáculos e chama `shoot` repetidamente
    dentro do loop de obstáculos. (Nota: Chamar `shoot` dentro do loop
    pode ter implicações de desempenho ou lógica não intencionais,
    pois será chamado para cada robô inimigo).

    Parâmetros:
    - robot0: A instância do robô atacante.
    - field: O objeto do campo contendo informações do jogo.
    """
    # ball_position = field.ball.get_coordinates() # Variável não utilizada nesta função

    for enemy_robot in field.enemy_robots:
        obst = Obstacle()
        enemy_coords = enemy_robot.get_coordinates()
        obst.set_obst(
            enemy_coords.X, enemy_coords.Y, enemy_coords.rotation
        )
        robot0.map_obstacle.add_obstacle(obst)
        
        # Chamada de shoot DENTRO do loop, conforme código original.
        # Isso significa que a tática de chute é reavaliada para cada robô inimigo.
        skills.shoot(robot0, field)


def atacante_campo_todo_real(robot0, field):
    """
    Comportamento de atacante "real" que cobre todo o campo, com lógica específica.

    Adiciona robôs inimigos como obstáculos. Posiciona-se com `follow_ball_y`
    se a bola estiver nas extremidades X do campo (perto dos gols).
    Caso contrário, usa `attack_ball_fisico`.

    Parâmetros:
    - robot0: A instância do robô atacante.
    - field: O objeto do campo contendo informações do jogo.
    """
    ball_position = field.ball.get_coordinates()

    for enemy_robot in field.enemy_robots:
        obst = Obstacle()
        enemy_coords = enemy_robot.get_coordinates()
        obst.set_obst(
            enemy_coords.X, enemy_coords.Y, enemy_coords.rotation
        )
        robot0.map_obstacle.add_obstacle(obst)
    
    # Limites para posicionamento defensivo/ofensivo perto das áreas
    NEAR_OPPONENT_GOAL_X = 390
    NEAR_OWN_GOAL_X = 70
    GOAL_AREA_Y_MIN = 70
    GOAL_AREA_Y_MAX = 240

    if (
        ball_position.X > NEAR_OPPONENT_GOAL_X and
        GOAL_AREA_Y_MIN <= ball_position.Y <= GOAL_AREA_Y_MAX
    ): # Bola perto do gol adversário
        skills.follow_ball_y(robot0, field, fixed_x=380)
    elif (
        ball_position.X < NEAR_OWN_GOAL_X and
        GOAL_AREA_Y_MIN <= ball_position.Y <= GOAL_AREA_Y_MAX
    ): # Bola perto do próprio gol
        skills.follow_ball_y(robot0, field, fixed_x=100)
    else: # Bola no meio do campo ou em outras posições de ataque
        skills.attack_ball_fisico(robot0, field, robot0.robot_id)


def atacante_real(robot0, field):
    """
    Comportamento de atacante "real" com ajuste de área de defesa baseado no estado.

    Adiciona inimigos como obstáculos. Se a bola estiver perto do gol adversário,
    usa `follow_ball_y`. Se a bola estiver muito recuada, também usa `follow_ball_y`
    com um X diferente. Caso contrário, usa `attack_ball_fisico`.
    A `area_defense` não é usada diretamente na lógica de chamada de skills.

    Parâmetros:
    - robot0: A instância do robô atacante.
    - field: O objeto do campo contendo informações do jogo.
    """
    ball_position = field.ball.get_coordinates()

    for enemy_robot in field.enemy_robots:
        obst = Obstacle()
        enemy_coords = enemy_robot.get_coordinates()
        obst.set_obst(
            enemy_coords.X, enemy_coords.Y, enemy_coords.rotation
        )
        robot0.map_obstacle.add_obstacle(obst)
    
    # area_defense = 390 # Valor padrão
    # A lógica original para area_defense foi comentada pois não impacta as chamadas de skills.
    # if field.atacante_current_state[robot0.robot_id] == 'STATE_B':
    #     area_defense = 370

    # Limites para diferentes comportamentos
    NEAR_OPPONENT_GOAL_X = 390
    GOAL_AREA_Y_MIN = 70
    GOAL_AREA_Y_MAX = 240
    MID_FIELD_X_DEFENSIVE_THRESHOLD = 210 # Limite para considerar a bola recuada

    if (
        ball_position.X > NEAR_OPPONENT_GOAL_X and
        GOAL_AREA_Y_MIN <= ball_position.Y <= GOAL_AREA_Y_MAX
    ): # Perto do gol adversário
        skills.follow_ball_y(robot0, field, fixed_x=380)
    elif ball_position.X < MID_FIELD_X_DEFENSIVE_THRESHOLD: # Bola recuada
        skills.follow_ball_y(robot0, field, fixed_x=300)
    else: # Posição de ataque
        skills.attack_ball_fisico(robot0, field, robot0.robot_id)


def zagueiro_real(robot0, field):
    """
    Controla o comportamento "real" do robô zagueiro.

    Se a bola está no campo de ataque, o zagueiro segue a bola em Y com X fixo.
    Se a bola está perto da própria área, também segue em Y com X mais recuado.
    Caso contrário, usa `attack_ball_fisico` (o que pode ser agressivo para um zagueiro).

    Parâmetros:
    - robot0: A instância do robô zagueiro.
    - field: O objeto do campo contendo informações do jogo.
    """
    OFFENSIVE_LINE_X = 225.0  # Meio de campo.
    ball_position = field.ball.get_coordinates()

    NEAR_OWN_GOAL_X = 70
    GOAL_AREA_Y_MIN = 70
    GOAL_AREA_Y_MAX = 240

    if ball_position.X >= OFFENSIVE_LINE_X: # Bola no campo de ataque
        skills.follow_ball_y(robot0, field, fixed_x=150)
    elif (
        ball_position.X < NEAR_OWN_GOAL_X and
        GOAL_AREA_Y_MIN <= ball_position.Y <= GOAL_AREA_Y_MAX
    ): # Bola perto da própria área
        skills.follow_ball_y(robot0, field, fixed_x=100)
    else: # Bola na defesa, mas não tão perto da área, ou outra situação.
          # Chamar attack_ball_fisico para um zagueiro é uma tática agressiva.
        skills.attack_ball_fisico(robot0, field, robot0.robot_id)


def goleiro_real(robot0, field):
    """
    Define o comportamento "real" do goleiro, similar ao `goleiro` normal.

    Usa `basic_tackle` se a bola estiver muito próxima à área.
    Usa `follow_ball_y_elipse` se a bola estiver dentro de um limite X.
    Caso contrário, permanece no centro do gol.

    Parâmetros:
    - robot0: A instância do robô goleiro.
    - field: O objeto do campo contendo informações do jogo.
    """
    GOALIE_CHASE_LINE_X = 75
    GOALIE_Y_TRACK_LIMIT_X = 300

    ball_position = field.ball.get_coordinates()

    if (ball_position.X <= GOALIE_CHASE_LINE_X) and (
        90 < ball_position.Y < 210
    ):
        skills.basic_tackle(robot0, field)
    else:
        if ball_position.X <= GOALIE_Y_TRACK_LIMIT_X:
            skills.follow_ball_y_elipse(robot0, field)
        else:
            skills.stay_on_center(robot0, field)


def goleiro_real_2(robot0, field, fixed=22):
    """
    Define um comportamento alternativo "real" para o goleiro (goleiro_real_2).

    Se a bola estiver dentro de um limite X estendido, o goleiro usa
    `follow_ball_y` com um X fixo e limites Y.
    Caso contrário, permanece no centro do gol.

    Parâmetros:
    - robot0: A instância do robô goleiro.
    - field: O objeto do campo contendo informações do jogo.
    - fixed: A coordenada X fixa para o goleiro ao seguir a bola (padrão é 22).
    """
    # GOALIE_CHASE_LINE_X = 75 # Não utilizado nesta função
    GOALIE_Y_TRACK_LIMIT_X_EXTENDED = 420  # Limite X estendido para rastreio.

    ball_position = field.ball.get_coordinates()

    if ball_position.X <= GOALIE_Y_TRACK_LIMIT_X_EXTENDED:
        # Bola dentro do limite estendido: seguir em Y com X fixo.
        skills.follow_ball_y(
            robot0, field, fixed_x=fixed, lim_sup=200, lim_inf=100
        )
    else:
        # Bola longe: goleiro permanece no centro do gol.
        skills.stay_on_center(robot0, field)