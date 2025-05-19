import math
import numpy as np
from entities.Obstacle import Obstacle


def go_to_point(robot0, target_x, target_y, field, target_theta=0, threshold=10):
    """
    Move o robô para as coordenadas especificadas.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo (opcional).
    """
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )

    if robot0.target_reached(threshold):
        robot0.vx = 0
        robot0.vy = 0
        #robot0.w = 0


def go_to_point_angled(robot0, target_x, target_y, field, target_theta=0, threshold=10):
    """
    Move o robô para as coordenadas especificadas, com velocidades decompostas em x e y.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo para orientar o robô.
    """
    # Definir o alvo para o robô
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)

    # Coordenadas da bola
    ball_position = field.ball.get_coordinates()

    # Calcula o ângulo entre a bola e o alvo
    angle_ball_to_target = np.arctan2(
        target_y - ball_position.Y, target_x - ball_position.X
    )

    # Define a velocidade máxima
    v_max = 1.5
    robot0.vx = robot0.v_max * np.cos(angle_ball_to_target)
    robot0.vy = robot0.v_max * np.sin(angle_ball_to_target)

    # Verifica se o robô alcançou o alvo
    if robot0.target_reached():
        robot0.vx = 0
        robot0.vy = 0


def follow_ball_y(robot0, field, fixed_x=None, target_theta=0, offset=0):
    """
    Move o robô para seguir a bola ao longo do eixo Y, mantendo uma posição fixa no eixo X ou na área do goleiro.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - fixed_x: Coordenada X fixa (opcional).
    - target_theta: Ângulo alvo (opcional).
    """
    ball_position = field.ball.get_coordinates()

    target_x = (
        fixed_x if fixed_x is not None else 150
    )  # X padrão é 400, pode ser sobrescrito
    target_y = ball_position.Y + offset

    go_to_point(robot0, target_x, target_y, field, target_theta)


def clear_ball(robot0, field, ball_position, robot_position, angle_to_ball):
    """
    Alinha o robô para limpar a bola de forma estratégica, utilizando quatro estágios: A, B

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - angle_to_ball: Ângulo entre o robô e a bola.
    """
    # Definição dos estados
    STATE_A, STATE_B,  = "A", "B"

    # Atualiza o ângulo entre o robô e a bola
    angle_to_ball = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )

    current_state = field.zagueiro_current_state
    # print(f"Estado atual: {current_state}")

    # Define um deslocamento para se posicionar atrás da bola
    approach_offset = -30

    if current_state == STATE_A:
        # Estado A: Se posicionar atrás da bola
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y
        target_theta = 0
        robot0.v_max = 1.5

        if robot0.target_reached(8) and robot0.ytarget_reached(5):
            current_state = STATE_B
            # print("Transitando para o estado B")    

    elif current_state == STATE_B:
        # Estado C: Limpar a bola (meio-campo + 10)
        target_x = 235  # 225 + 10 (Meio campo + 10 em X)
        target_y = ball_position.Y
        target_theta = 0
        robot0.v_max = 1.5

        if robot_position.X > ball_position.X:
            current_state = STATE_A
        
    # Atualiza o estado atual do zagueiro
    field.zagueiro_current_state = current_state

    # Move o robô para o ponto alvo
    go_to_point(robot0, target_x, target_y, field, target_theta, threshold=3)


def attack_ball(robot0, field, ball_position, robot_position, target_theta, controller):
    """
    Alinha o robô para atacar a bola no gol.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - target_theta: Ângulo alvo.
    """
    # Definição dos estados
    STATE_A, STATE_B, STATE_C, STATE_D = "A", "B", "C", "D"

    # Define o alvo final (centro do gol)
    target_x_final = 450

    # Ajusta o alvo com base na posição da bola
    target_y_final = 180 if ball_position.Y < 150 else 145 

    current_state = field.atacante_current_state

    # Calcula o ângulo entre o robô e a bola
    angle_robot_to_ball = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )
    angle_ball_to_target = np.arctan2(
        target_y_final - ball_position.Y, target_x_final - ball_position.X
    )

    # Calcula a diferença angular entre o robô e a bola em relação ao alvo
    angle_diff = np.degrees(angle_ball_to_target - angle_robot_to_ball)

    approach_offset = -40
    #threshold = 2
    threshold = 8

    if current_state == STATE_A:
        # Estado A: Se posicionar atrás da bola
        target_x = ball_position.X + approach_offset * np.cos(angle_ball_to_target)
        target_y = ball_position.Y + approach_offset * np.sin(angle_ball_to_target)
        target_theta = angle_ball_to_target
        robot0.v_max = 1.35
        # print("Estado A")
        # print(f"target_x: {target_x}, target_y: {target_y}, target_theta: {target_theta}")

        if robot0.target_reached(threshold):
            current_state = STATE_B
            # print("Transitando para o estado B")

    elif current_state == STATE_B:
        # Estado B: Ir até a bola
        target_x = ball_position.X - 20 * np.cos(angle_ball_to_target)
        target_y = ball_position.Y - 20 * np.sin(angle_ball_to_target)
        target_theta = angle_ball_to_target
        robot0.v_max = 1.25
        # controller.chute(robot0, 5)
        # print("Estado B")

        if robot0.target_reached(threshold):
            
            if abs(angle_diff <= 15):
                controller.chute(robot0, 5)
                current_state = STATE_C
        else:
            current_state = STATE_A


    elif current_state == STATE_C:
        # Estado C: Chutar a bola em direção ao gol
        
        target_x = target_x_final
        target_y = target_y_final
        target_theta = angle_ball_to_target
        target_theta = 0
        


        #Faz o robo conduzir e chutar quando tiver perto do gol
        robot0.v_max = 1.25 if robot_position.X < 335 else 1.5
        controller.chute(robot0, 5)
        # print("Estado C")

        if not abs(angle_diff) <= 20:
            current_state = STATE_B
        elif (
            90 <= np.degrees(angle_robot_to_ball) <= 180
            or -180 <= np.degrees(angle_robot_to_ball) <= -90
        ):
            current_state = STATE_D

    elif current_state == STATE_D:
        # Estado D: Evitar a bola
        target_x = ball_position.X -40
        target_y = ball_position.Y 
        target_theta = angle_ball_to_target
        robot0.v_max = 1.5
        # print("Estado D")
        
        '''# desvia mais lateralmente, sempre para o lado oposto do robô
        lateral_offset = 15 if robot_position.Y < ball_position.Y else -35
        target_y = ball_position.Y + lateral_offset
        target_theta = angle_ball_to_target
        robot0.v_max = 1.5
'''


    # Atualiza o estado atual do atacante
    field.atacante_current_state = current_state

    # Ajusta a velocidade do robô se ele estiver perto do gol
    if (
        ball_position.X >= 380
        and 85 <= ball_position.Y <= 200
        and robot_position.X >= 375
    ):
        robot0.v_max = 1

    # Usa a função adequada para mover o robô
    if current_state == STATE_C:
        go_to_point_angled(robot0, target_x, target_y, field, target_theta, threshold)
    else:
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)

def pursue_ball(robot0, field, controller):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()
    midLineY = 150

    if ball_position.X <= 55 and 85 <= ball_position.Y <= 225:
        # A bola está na área do goleiro
        if ball_position.Y <= midLineY:
            follow_ball_y(robot0, field, fixed_x=85, offset=-50)
        else: 
            follow_ball_y(robot0, field, fixed_x=85, offset=50)
    else:
        # Atacar a bola
        clear_ball(
            robot0, field, ball_position, robot_position, robot_position.rotation
        )

        controller.chute(robot0, 3)



def shoot(robot0, field, controller):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    if ball_position.X >= 400 and 85 <= ball_position.Y <= 225:
        # A bola está na área do goleiro
        follow_ball_y(robot0, field, fixed_x=380, target_theta=0)
    else:
        # Atacar a bola
        attack_ball(
            robot0, field, ball_position, robot_position, robot_position.rotation, controller
        )


# implementação do goleiro
def follow_ball_y_elipse(robot0, field, target_theta=0):
    """
    Move o goleiro para acompanhar a bola ao longo do eixo Y,
    e ajusta sua posição X para seguir a curva de uma meia elipse,
    mantendo-o dentro da área estabelecida.

    :param robot0: O robô ou goleiro que deve se movimentar.
    :param field: Objeto que fornece as coordenadas da bola.
    :param target_theta: Ângulo desejado de orientação do robô.
    """

    robot0.v_max = 1.5

    center_x = 10  # posição média do goleiro no gol
    center_y = 150  # centro
    a = 40
    b = 100

    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # Máximo intervalo de y para ficar na área:
    limite_inferior_y = center_y - 60
    limite_superior_y = center_y + 60

    # Define os limites do intervalo no eixo X (para não ficar louco o robô)
    # limite_inferior_x = target_x - 10
    # limite_superior_x = target_x + 10

    if limite_inferior_y <= ball_position.Y <= limite_superior_y:
    # Bola está na faixa ideal da área: segue uma meia elipse
        target_y = ball_position.Y
        dy = target_y - center_y
        inside_sqrt = 1 - (dy ** 2) / (b ** 2)

        if inside_sqrt < 0:
            inside_sqrt = 0  # evita erro de sqrt negativo

        target_x = center_x + a * np.sqrt(inside_sqrt)  # meia elipse à direita
    else:
    # Bola nos cantos: goleiro vai para posição segura pré-definida
        target_x = center_x  # mantém x fixo
        if ball_position.Y <= limite_inferior_y:
            target_y = center_y - 35
        else:
            target_y = center_y + 35


    # manutenção do goleiro em um limiar (se necessário)
    # Verifica se o robô está dentro do intervalo
    """
    if limite_inferior_x <= robot_position.X <= limite_superior_x:
        target_x = robot_position.X  # Mantém a posição X atual
    else:
        target_x = 30  # Fixa posição X do robô em 30
    """
    # calculo do angulo para bola
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    target_theta = np.arctan2(delta_y, delta_x)

    # enviando robô para ponto alvo
    go_to_point(robot0, target_x, target_y, field, target_theta)

'''def follow_ball_y_elipse(robot, field, enemy_robots):
    ball_position = field.ball.get_coordinates()

    # Parâmetros da elipse
    position = robot.get_coordinates()
    center_x = position.X  # agora 'position' tem o X e o Y do robô
    center_y = 150
    a = 100
    b = 60

    limite_inferior_y = center_y - b
    limite_superior_y = center_y + b

    if limite_inferior_y <= ball_position.Y <= limite_superior_y:
        target_y = ball_position.Y
        dy = target_y - center_y
        inside_sqrt = 1 - (dy ** 2) / (b ** 2)
        inside_sqrt = max(inside_sqrt, 0)
        target_x = center_x + a * np.sqrt(inside_sqrt)
        target_theta = 0  # fica de frente
    else:
        # Canto: posiciona com rotação
        target_x = center_x + 30
        target_y = center_y - 35 if ball_position.Y < limite_inferior_y else center_y + 35
        target_theta = np.arctan2(0 - target_y, field.width / 2 - target_x)  # ou field.height


    # Avança se não houver inimigo por perto
    if not inimigo_proximo(ball_position, enemy_robots):
        target_x += 30

    # Aplica ao robô
    robot.target_x = target_x
    robot.target_y = target_y
    robot.target_theta = target_theta
    robot.v_max = 1.5'''



def basic_tackle(robot0, field):
    """
    função de Tackle Básico (persegue a bola em uma distancia determinada)
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # calculo do angulo para a bola

    target_theta = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )
    target_x = ball_position.X + 100 * np.cos(target_theta)
    target_y = ball_position.Y + 120 * np.sin(target_theta)

    #robot0.v_max = 1.25

    # enviando robô para ponto alvo
    go_to_point(robot0, target_x, target_y, field, target_theta)

'''def inimigo_proximo(ball_position, enemy_robots):
    for enemy in enemy_robots:
        enemy_position = enemy.get_coordinates()  
        distance = np.sqrt((enemy_position.X - ball_position.X)**2 + (enemy_position.Y - ball_position.Y)**2)
        if distance < 100:  
            return True
    return False



def posiciona_goleiro(robot, ball_position, enemy_robots, field):
    # Parâmetros da elipse padrão
    center_x = field.goal_x  # posição fixa do gol
    center_y = 0
    a = 100  # eixo maior
    b = 20   # eixo menor
    
    limite_inferior_y = -field.goal_height / 2
    limite_superior_y = +field.goal_height / 2

    # Condição: bola dentro da área lateral do gol (zona ativa da elipse)
    if limite_inferior_y <= ball_position.Y <= limite_superior_y:
        target_y = ball_position.Y
        dy = target_y - center_y
        inside_sqrt = 1 - (dy ** 2) / (b ** 2)
        inside_sqrt = max(inside_sqrt, 0)
        target_x = center_x + a * np.sqrt(inside_sqrt)
    else:
        # Canto: ir para o canto mais adequado para "bater girando"
        target_x = center_x + 30  # vai mais para frente no campo
        if ball_position.Y < limite_inferior_y:
            target_y = center_y - 35
        else:
            target_y = center_y + 35

        # Faz o goleiro rotacionar para bater mais para frente
        angle_to_center = np.arctan2(-target_y, field.length / 2 - target_x)
        robot.target_theta = angle_to_center

    # Se não houver inimigos por perto, o goleiro pode avançar mais!
    if not inimigo_proximo(ball_position, enemy_robots):
        # Aproxima ainda mais para "chutar para frente"
        target_x += 30  # avança um pouco mais no campo

    # Define o alvo final
    robot.target_x = target_x
    robot.target_y = target_y'''


def stay_on_center(robot0, field):
    go_to_point(robot0, 30, 150, field, 0)


def projection_stop_target(robot, field, kicker=False):
    """
    Faz a projeção adequada do alvo de um robô em stop. Se ele for o ,
    a projeção é em direção ao gol. Se ele não for, a projeção é em direção
    de proteger seu próprio gol.

    Parâmetros:
    - robot: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - kicker: Define se a falta é ofensiva ou defensiva
    """
    ball = field.ball
    ball_coordinates = ball.get_coordinates()

    if kicker:
        radius = 20
        ball_obstacle = 10

        goal_y = 150
        goal_x = 450

        angle_ball_to_goal = np.arctan2(
            (goal_y - ball_coordinates.Y), (goal_x - ball_coordinates.X)
        )

        target_x = ball_coordinates.X - radius * np.cos(angle_ball_to_goal)
        target_y = ball_coordinates.Y - radius * np.sin(angle_ball_to_goal)

        angle_robot = angle_ball_to_goal
    else:
        radius = 70
        ball_obstacle = 20

        goal_y = 150
        goal_x = 0

        angle_ball_to_goal = np.arctan2(
            (goal_y - ball_coordinates.Y), (ball_coordinates.X - goal_x)
        )
        angle_global = np.pi - angle_ball_to_goal

        target_x = ball_coordinates.X + radius * np.cos(angle_global)
        target_y = ball_coordinates.Y + radius * np.sin(angle_global)

        angle_robot = -angle_ball_to_goal

    obst = Obstacle()  # Configura a bola como obstáculo
    obst.set_obst(
        ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=ball_obstacle
    )
    robot.map_obstacle.add_obstacle(obst)

    robot.target.set_target(robot, (target_x, target_y), field, angle_robot)
    go_to_point(robot, target_x, target_y, field, angle_robot)


def idle_behavior_avoid_ball_stop_game(robot, field):
    """
    Faz o robô ir para o seu alvo desviando da bola.

    Parâmetros:
    - robot: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball = field.ball

    target_robot = robot.target.get_coordinates()

    ball_obst_radius = 15

    # Configura a bola como obstáculo
    obst = Obstacle()
    obst.set_obst(
        ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=ball_obst_radius
    )
    robot.map_obstacle.add_obstacle(obst)

    x_target = target_robot.X
    y_target = target_robot.Y

    # Calcula o ângulo do robô para a bola
    # O robô irá acompanhar a bola angularmente
    theta_robot = angle_ball_to_goal = np.arctan2(
        (ball.get_coordinates().Y - robot.get_coordinates().Y),
        (ball.get_coordinates().X - robot.get_coordinates().X),
    )

    go_to_point(robot, x_target, y_target, field, theta_robot)

def stop_kickoff_positioning(robot, field, attacking=False, attacker=False):

    ball = field.ball

    if attacking:
        ball_obst_radius = 15
        if attacker:
            target_x = 205
            target_y = 150

        else:
            target_x = 150
            target_y = 150

    else:
        ball_obst_radius = 15
        if attacker:
            target_x = 155
            target_y = 150

        else:
            target_x = 120
            target_y = 150

    # Configura a bola como obstáculo
    obst = Obstacle()
    obst.set_obst(
        ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=ball_obst_radius
    )
    robot.map_obstacle.add_obstacle(obst)

    go_to_point(robot, target_x, target_y, field, np.pi)


def penalty_idle_offensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Move os robôs para posições específicas para a posição de penalty idle.

    Parameters:
    skills: módulo contendo a função go_to_point para mover os robôs.
    robot_goleiro: objeto representando o robô goleiro.
    robot_zagueiro: objeto representando o robô zagueiro.
    robot_atacante: objeto representando o robô atacante.
    field: objeto representando o campo.
    """
    go_to_point(robot_goleiro, 150, 300, field, 0)
    go_to_point(robot_zagueiro, 150, 20, field, 0)
    go_to_point(robot_atacante, 0, 150, field, 0)


def penalty_idle_offensive_game_on(robot_goleiro, robot_zagueiro, field):
    """
    Move os robôs para posições específicas para a posição de penalty idle.

    Parameters:
    skills: módulo contendo a função go_to_point para mover os robôs.
    robot_goleiro: objeto representando o robô goleiro.
    robot_zagueiro: objeto representando o robô zagueiro.
    robot_atacante: objeto representando o robô atacante.
    field: objeto representando o campo.
    """
    go_to_point(robot_goleiro, 230, 300, field, 0)
    go_to_point(robot_zagueiro, 230, 20, field, 0)


def penalty_idle_defensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Move os robôs para posições específicas para a posição de penalty idle.

    Parameters:
    skills: módulo contendo a função go_to_point para mover os robôs.
    robot_goleiro: objeto representando o robô goleiro.
    robot_zagueiro: objeto representando o robô zagueiro.
    robot_atacante: objeto representando o robô atacante.
    field: objeto representando o campo.
    """
    go_to_point(robot_goleiro, 0, 150, field, 0)
    go_to_point(robot_zagueiro, 230, 300, field, 0)
    go_to_point(robot_atacante, 250, 20, field, 0)


def penalty_idle_game_on(robot_zagueiro, robot_atacante, field):
    """
    Move os robôs para posições específicas para a posição de penalty idle.

    Parameters:
    skills: módulo contendo a função go_to_point para mover os robôs.
    robot_goleiro: objeto representando o robô goleiro.
    robot_zagueiro: objeto representando o robô zagueiro.
    robot_atacante: objeto representando o robô atacante.
    field: objeto representando o campo.
    """
    go_to_point(robot_zagueiro, 230, 300, field, 0)
    go_to_point(robot_atacante, 250, 20, field, 0)

def attack_ball_fisico(robot0, field):
    """
    Alinha o robô para atacar a bola no gol.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - target_theta: Ângulo alvo.
    """
    # Definição dos estados
    STATE_A, STATE_B, STATE_C, STATE_R1 = "A", "B", "C", "R1"

    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # Define o alvo final (centro do gol)
    target_x_final = 450
    target_y_final = 150

    # Ajusta o alvo com base na posição da bola
    if 110 < ball_position.Y < 190:
        target_y_final = ball_position.Y
        # print("Bola no alvo")
    else:
        target_y_final = target_y_final + (-30 if ball_position.Y < 150 else 30)

    current_state = field.atacante_current_state

    # Calcula o ângulo entre o robô e a bola
    angle_robot_to_ball = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )
    angle_ball_to_target = np.arctan2(
        target_y_final - ball_position.Y, target_x_final - ball_position.X
    )

    # Calcula a diferença angular entre o robô e a bola em relação ao alvo
    angle_diff = np.degrees(angle_ball_to_target - angle_robot_to_ball)

    approach_offset = -20
    #threshold = 2
    threshold = 15

    print("Contador: ", field.counter_attacker_stop)
    if current_state == STATE_A:
        # Estado A: Se posicionar atrás da bola
        target_x = ball_position.X + approach_offset * np.cos(angle_ball_to_target)
        target_y = ball_position.Y + approach_offset * np.sin(angle_ball_to_target)
        target_theta = angle_ball_to_target
        #robot0.v_max = 1.25
        print("Estado A")
        #print(f"target_x: {target_x}, target_y: {target_y}, target_theta: {target_theta}")

        if robot0.target_reached(threshold):
            robot0.vx = 0
            robot0.vy = 0
            #robot0.w = 0
            field.counter_attacker_stop += 1

            if field.counter_attacker_stop > field.threshold_attacker_stop:
                current_state = STATE_R1
                field.counter_attacker_stop = 0
        elif (
            90 <= np.degrees(angle_robot_to_ball) <= 180
            or -180 <= np.degrees(angle_robot_to_ball) <= -90
        ):
            field.counter_attacker_stop = 0
            current_state = STATE_C
        else:
            field.counter_attacker_stop = 0

    elif current_state == STATE_R1:
        print("Estado R1")
        target_x = ball_position.X + approach_offset * np.cos(angle_ball_to_target)
        target_y = ball_position.Y + approach_offset * np.sin(angle_ball_to_target)
        target_theta = angle_ball_to_target
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)

        robot0.vx = 0
        robot0.vy = 0

        if not robot0.target_reached(threshold+5):
            current_state = STATE_A
        else:
            field.counter_attacker_stop += 1
            if field.counter_attacker_stop > 4*field.threshold_attacker_stop:
                current_state = STATE_B
                field.counter_attacker_stop = 0
        
    elif current_state == STATE_B:
        # Estado C: Chutar a bola em direção ao gol
        target_x = target_x_final
        target_y = target_y_final
        target_theta = angle_ball_to_target
        target_theta = 0
        #robot0.v_max = 1.5
        print("Estado B")

        if not abs(angle_diff) <= 60:
            current_state = STATE_A
            field.counter_attacker_stop = 0
        elif (
            90 <= np.degrees(angle_robot_to_ball) <= 180
            or -180 <= np.degrees(angle_robot_to_ball) <= -90
        ):
            field.counter_attacker_stop += 1
            if field.counter_atacker_stop > 5*field.threshold_attacker_stop:
                current_state = STATE_C

    elif current_state == STATE_C:
        # Estado D: Evitar a bola
        target_x = ball_position.X - 25
        target_y = ball_position.Y
        target_theta = angle_ball_to_target
        #robot0.v_max = 1.5
        print("Estado C")

        # Ajusta a posição Y do alvo para evitar a bola
        if 90 <= np.degrees(angle_robot_to_ball) <= 180:
            target_y -= 20
        elif -180 <= np.degrees(angle_robot_to_ball) <= -90:
            target_y += 20

        if robot0.target_reached(threshold):
            current_state = STATE_A

    # Atualiza o estado atual do atacante
    field.atacante_current_state = current_state

    # Ajusta a velocidade do robô se ele estiver perto do gol
    # if (
    #     ball_position.X >= 380
    #     and 85 <= ball_position.Y <= 200
    #     and robot_position.X >= 370
    # ):
    #     #robot0.v_max = 1
    field.send_local = False
    # Usa a função adequada para mover o robô
    if current_state == STATE_B:
        field.send_local = False
        robot0.vMax = 0.7
        field.send_local = True
        robot0.vx = 1.0
        robot0.vy = 0
        go_to_point_angled(robot0, target_x, target_y, field, target_theta, threshold)
    elif current_state == STATE_A:
        field.send_local = False
        robot0.vMax = 1.0
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)
        robot0.w = 0
    elif current_state == STATE_C:
        robot0.vMax = 1.0
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)
        robot0.w = 0
    else:
        field.send_local = False
        robot0.vMax = 1.0
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)
        robot0.vx = 0
        robot0.vy = 0
        if abs(robot0.get_coordinates().rotation - target_theta) < 20*np.pi/180:
            robot0.w = 0

def pursue_ball_fisico(robot0, field):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    if ball_position.X <= 70 and 70 <= ball_position.Y <= 240:
        # A bola está na área do goleiro
        follow_ball_y(robot0, field, fixed_x=190, target_theta=np.pi)
    else:
        # Atacar a bola
        attack_ball_fisico(robot0, field)
        #clear_ball(
        #    robot0, field, ball_position, robot_position, robot_position.rotation
        #)






def passe_ensaiado(zaga, ataq, field, controller, avanço=40):
            
    bola = field.ball.get_coordinates()
    dst = ataq.get_coordinates()

    alvo_theta = 0                       
        # vetor unitário nessa direção
    dir_x = np.cos(alvo_theta)
    dir_y = np.sin(alvo_theta)

    # ponto alvo fica *à frente* do atacante
    alvo_x = dst.X + avanço*dir_x
    alvo_y = dst.Y + avanço*dir_y

    #alinhar robô com a bola-alvo
    go_to_point(zaga, bola.X, bola.Y, field, alvo_theta)
    if zaga.target_reached(10):
        controller.chute(zaga, 3)     

    # atacante corre pro ponto de recepção
    go_to_point(ataq, alvo_x, alvo_y, field, alvo_theta)