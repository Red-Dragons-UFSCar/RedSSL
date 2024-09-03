import math
import numpy as np

STATE_A = "A"  # Se posicionar atrás da bola
STATE_B = "B"  # Avançar na bola
STATE_C = "C"  # Avançar até o alvo
STATE_D = "D"  # Desviar da bola

def go_to_point(robot0, target_x, target_y, field, target_theta=0):
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

    if robot0.target_reached():
        robot0.vx = 0
        robot0.vy = 0


def follow_ball_y(robot0, field, fixed_x=None, target_theta=0):
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
    target_y = ball_position.Y

    go_to_point(robot0, target_x, target_y, field, target_theta)


def clear_ball(robot0, field, ball_position, robot_position, angle_to_ball):
    """
    Função para alinhar o robô e limpar a bola de forma estratégica,
    utilizando quatro estágios: A, B, C e D. O alvo no estágio C será o meio campo + 10 em X e a posição Y da bola.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - angle_to_ball: Ângulo entre o robô e a bola.
    """
    STATE_A = "A"  # Se posicionar atrás da bola
    STATE_B = "B"  # Avançar na bola
    STATE_C = "C"  # Avançar até o alvo
    STATE_D = "D"  # Desviar da bola

    current_state = STATE_A

    angle_to_ball = np.arctan2(ball_position.Y - robot_position.Y,
                               ball_position.X - robot_position.X)

    # Define uma posição atrás da bola
    approach_offset = -20  

    print(f"Estado atual (zagueiro): {current_state}")

    if current_state == STATE_A:
        # Estágio A: Se posicionar atrás da bola
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y
        target_theta = angle_to_ball

        # Se o robô está alinhado com a bola, transita para o estado B
        if robot0.target_reached():
            current_state = STATE_B
        elif 90 <= np.degrees(angle_to_ball) <= 180 or -180 <= np.degrees(angle_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_B:
        # Estágio B: Ir até a bola
        target_x = ball_position.X - 10
        target_y = ball_position.Y
        target_theta = angle_to_ball

        # Se o robô alcança a bola, transita para o estado C
        if robot0.target_reached():
            current_state = STATE_C
        elif 90 <= np.degrees(angle_to_ball) <= 180 or -180 <= np.degrees(angle_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_C:
        # Estágio C: Limpar a bola, movendo-a para o meio campo
        target_x = 225 + 10  # Meio campo + 10 em X
        target_y = ball_position.Y  # Mantém o Y da bola
        target_theta = angle_to_ball


        # Se o robô não está mais alinhado com a bola, volta para o estado B
        if not (-(np.pi) / 6 < angle_to_ball < (np.pi) / 6):
            current_state = STATE_B
        elif 90 <= np.degrees(angle_to_ball) <= 180 or -180 <= np.degrees(angle_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_D:
        # Estágio D: Evitar a bola nos 2º ou 3º quadrantes
        target_x = ball_position.X - 25
        target_y = ball_position.Y
        target_theta = angle_to_ball

        # Evitar a bola ajustando a posição Y do alvo
        if 90 <= np.degrees(angle_to_ball) <= 180:
            target_y -= 20  # Mover o alvo para baixo
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 20  # Mover o alvo para cima

        # Verifica se o robô pode transitar de volta para A ou B
        if robot0.target_reached():
            current_state = STATE_B

    # Move o robô para o ponto alvo
    go_to_point(robot0, target_x, target_y, field, target_theta)



def attack_ball(robot0, field, ball_position, robot_position, angle_to_ball):
    """
    Função para alinhar o robô e atacar a bola de forma estratégica.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - angle_to_ball: Ângulo entre o robô e a bola.
    """
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    angle_to_ball = np.arctan2(delta_y, delta_x)

    approach_offset = -20  # Define uma posição atrás da bola

    # Condição para atacar a bola com um ângulo que force a bola para dentro do campo
    if ball_position.Y < 50:
        # Bola está no lado inferior do campo (1º quadrante)
        if (np.pi) / 6 < angle_to_ball < (np.pi) / 3:
            target_x = ball_position.X
            target_y = ball_position.Y
            target_theta = angle_to_ball
        else:
            target_x = ball_position.X + approach_offset
            target_y = (
                ball_position.Y - 20
            )  # Força o ataque em direção ao centro do campo
            target_theta = angle_to_ball  # Alinha o robô com a bola

        # Ajusta a posição y do robô com base no ângulo
        if (
            90 <= np.degrees(angle_to_ball) <= 180
        ):  # Não é o ideal ter um if desse pra cada condição, mas por algum motivo que meu cérebro é incapaz de compreender (ou apenas sono), o código não respeita essa condição no fim da função, então botei sapoha pra cada posição de y. Lidem com isso.
            target_y -= 20
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 20

        go_to_point(robot0, target_x, target_y, field, target_theta)

    elif ball_position.Y > 250:
        # Bola está no lado superior do campo (4º quadrante)
        if -(np.pi) / 3 < angle_to_ball < -(np.pi) / 6:
            target_x = ball_position.X
            target_y = ball_position.Y
            target_theta = angle_to_ball
        else:
            target_x = ball_position.X + approach_offset
            target_y = (
                ball_position.Y + 20
            )  # Força o ataque em direção ao centro do campo
            target_theta = angle_to_ball  # Alinha o robô com a bola

        # Ajusta a posição y do robô com base no ângulo
        if 90 <= np.degrees(angle_to_ball) <= 180:
            target_y -= 20
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 20

        go_to_point(robot0, target_x, target_y, field, target_theta)

    # Parte da função que deve ser executada apenas quando ball_position.Y não está nos intervalos especiais
    else:
        if -(np.pi) / 6 < angle_to_ball < (np.pi) / 6:
            target_x = ball_position.X
            target_y = ball_position.Y
            target_theta = angle_to_ball
        else:
            target_x = ball_position.X + approach_offset
            target_y = ball_position.Y
            target_theta = angle_to_ball  # Alinha o robô com a bola

        # Ajusta a posição y do robô com base no ângulo
    if 90 <= np.degrees(angle_to_ball) <= 180:
        target_y -= 20
    elif -180 <= np.degrees(angle_to_ball) <= -90:
        target_y += 20

    go_to_point(robot0, target_x, target_y, field, target_theta)


def pursue_ball(robot0, field):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    if ball_position.X <= 55 and 85 <= ball_position.Y <= 225:
        # A bola está na área do goleiro
        follow_ball_y(robot0, field, fixed_x=190, target_theta=np.pi)
    else:
        # Atacar a bola
        attack_ball(
            robot0, field, ball_position, robot_position, robot_position.rotation
        )


def shoot(robot0, field):
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
        follow_ball_y(robot0, field, fixed_x=190, target_theta=np.pi)
    else:
        # Atacar a bola
        attack_ball(
            robot0, field, ball_position, robot_position, robot_position.rotation
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
    center_x = 5  # posição média do goleiro no gol
    center_y = 150  # centro
    a = 40
    b = 100

    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # Maximmo intervalo de y para ficar na àrea:
    limite_inferior_y = center_y - 60
    limite_superior_y = center_y + 60

    # Define os limites do intervalo no eixo X (para não ficar louco o robô)
    # limite_inferior_x = target_x - 10
    # limite_superior_x = target_x + 10

    if (
        limite_inferior_y <= ball_position.Y <= limite_superior_y
    ):  # caso a bola esteja nas condiçẽos ideais para seguir em y (dentro dos limites da area)
        target_y = ball_position.Y  # assume mesmo y da bola
        target_x = center_x + a * np.sqrt(
            1 - ((target_y - center_y) ** 2) / b**2
        )  # x assume forma de meia elipse de eixo maior 100 e eixo menor 20
    else:
        # a bola "está nos cantos"
        target_x = center_x  # goleiro fica na posição fixa x
        if ball_position.Y <= limite_inferior_y:
            target_y = center_y - 50  # se mantendo no canto mas não sobre a trave
        else:
            target_y = center_y + 50  # se mantendo no canto mas não sobre a trave

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


def basic_tackle(robot0, field):
    """
    função de Tackle Básico (persegue a bola em uma distancia determinada)
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # calculo do angulo para a bola

    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    target_theta = np.arctan2(delta_y, delta_x)

    # enviando robô para ponto alvo
    go_to_point(robot0, ball_position.X, ball_position.Y, field, target_theta)


def stay_on_center(robot0, field):
    go_to_point(robot0, 30, 150, field, 0)

def avoid_ball_stop_game_defending(robot, field):
    '''
    Altera o target do robô para ficar longe da bola segundo as regras do SSL-EL.
    Caso o target do robô esteja em um raio d_limiar da bola, esse alvo é espelhado
    radialmente para fora do circulo de raio d_limiar.

    Parâmetros:
    - robot: Instância do robô a ser movido.
    - field: Instância da classe Field.
    '''
    ball = field.ball

    target_robot = robot.target.get_coordinates()

    x_target = target_robot.X
    y_target = target_robot.Y

    dist_ball = np.sqrt( (ball.get_coordinates().X - x_target)**2 +
                         (ball.get_coordinates().Y - y_target)**2 )

    angle_to_ball = np.arctan2((ball.get_coordinates().Y - y_target),
                               (ball.get_coordinates().X - x_target))
    
    d_limiar = 60

    if dist_ball < d_limiar-10:

        d_avoid_ball = d_limiar - dist_ball

        d_target_x = d_avoid_ball * np.cos(angle_to_ball)
        d_target_y = d_avoid_ball * np.sin(angle_to_ball)

        new_x = x_target - d_target_x
        new_y = y_target - d_target_y

        dist_ball_robot = np.sqrt( (ball.get_coordinates().X - robot.get_coordinates().X )**2 +
                         (ball.get_coordinates().Y - robot.get_coordinates().Y)**2 )

        go_to_point(robot, new_x, new_y, field, target_robot.rotation)

