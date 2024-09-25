import math
import numpy as np

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

    angle_to_ball = np.arctan2(ball_position.Y - robot_position.Y,
                               ball_position.X - robot_position.X) 

    current_state = field.zagueiro_current_state

    print(f"Estado atual {current_state}")
    # Define uma posição atrás da bola
    approach_offset = -40  

    if current_state == STATE_A:
        # Estágio A: Se posicionar atrás da bola
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y
        target_theta = 0

        # Se o robô está alinhado com a bola, transita para o estado B
        if robot0.target_reached(8):
            current_state = STATE_B
            print("Transitando para B")
        elif 90 <= np.degrees(angle_to_ball) <= 180 or -180 <= np.degrees(angle_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_B:
        # Estágio B: Ir até a bola
        target_x = ball_position.X - 20
        target_y = ball_position.Y
        target_theta = 0
        robot0.v_max=1.25
        
        # Se o robô alcança a bola, transita para o estado C
        if robot0.target_reached(8):
            current_state = STATE_C
        elif 90 <= np.degrees(angle_to_ball) <= 180 or -180 <= np.degrees(angle_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_C:
        # Estágio C: Limpar a bola, movendo-a para o meio campo
        target_x = 225 + 10  # Meio campo + 10 em X
        target_y = ball_position.Y  # Mantém o Y da bola
        target_theta = 0
        robot0.v_max=1.25

        # Se o robô não está mais alinhado com a bola, volta para o estado B
        if not (-(np.pi) / 6 < angle_to_ball < (np.pi) / 6):
            current_state = STATE_B
        elif 90 <= np.degrees(angle_to_ball) <= 180 or -180 <= np.degrees(angle_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_D:
        # Estágio D: Evitar a bola nos 2º ou 3º quadrantes
        target_x = ball_position.X - 25
        target_y = ball_position.Y
        target_theta = 0

        # Evitar a bola ajustando a posição Y do alvo
        if 90 <= np.degrees(angle_to_ball) <= 180:
            target_y -= 20  # Mover o alvo para baixo
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 20  # Mover o alvo para cima

        # Verifica se o robô pode transitar de volta para A ou B
        if robot0.target_reached():
            current_state = STATE_B

    field.zagueiro_current_state = current_state

    # Move o robô para o ponto alvo
    go_to_point(robot0, target_x, target_y, field, target_theta)


def attack_ball(robot0, field, ball_position, robot_position, angle_to_ball):
    """
    Função para alinhar o robô e "chutar" a bola no gol.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - angle_to_ball: Ângulo entre o robô e a bola.
    """
    STATE_A = "A"  # Se posicionar atrás da bola
    STATE_B = "B"  # Avançar na bola
    STATE_C = "C"  # Avançar até o alvo (gol)
    STATE_D = "D"  # Desviar da bola

    # Ângulo entre o robô e a bola
    angle_robot_to_ball = np.arctan2(ball_position.Y - robot_position.Y,
                                     ball_position.X - robot_position.X)

    # Alvo inicial: centro do gol
    target_x_final = 450  # X do centro do gol
    target_y_final = 150  # Y do centro do gol
    
    # Verifica a posição da bola em relação à largura do gol (800 unidades)
    if 110 < ball_position.Y < 190:
        # Se a bola estiver dentro da largura do gol
        target_y_final = ball_position.Y
        print("bola no alvo")
    else:
        # Se a bola estiver fora da largura do gol, mira no lado mais próximo com distância de 50 unidades
        if ball_position.Y < 150:
            target_y_final = target_y_final - 40 + 10  # Mira 10 unidades acima da trave superior
        elif ball_position.Y > 150:
            target_y_final = target_y_final + 40 - 10  # Mira 10 unidades abaixo da trave inferior

    angle_ball_to_target = np.arctan2(target_y_final - ball_position.Y,
                                      target_x_final - ball_position.X)

    current_state = field.atacante_current_state

    angle_diff = np.degrees(angle_ball_to_target - angle_robot_to_ball)

    # Define uma posição atrás da bola
    approach_offset = -100  

    if current_state == STATE_A:
        # Estágio A: Se posicionar atrás da bola
        target_x = ball_position.X + approach_offset * np.cos(angle_ball_to_target)
        target_y = ball_position.Y + approach_offset * np.sin(angle_ball_to_target)
        target_theta = angle_ball_to_target
        print("Estado A")

        # Se o robô está alinhado com a bola, transita para o estado B
        if robot0.target_reached(6):
            current_state = STATE_B
            print("Transitando para B")
        elif 90 <= np.degrees(angle_robot_to_ball) <= 180 or -180 <= np.degrees(angle_robot_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_B:
        # Estágio B: Ir até a bola
        target_x = ball_position.X - 20 * np.cos(angle_ball_to_target)
        target_y = ball_position.Y - 20 * np.sin(angle_ball_to_target)
        target_theta = angle_ball_to_target
        robot0.v_max = 1.5
        print("Estado B")

        # Se o robô alcança a bola, transita para o estado C
        if robot0.target_reached(6):
            current_state = STATE_C
        elif 90 <= np.degrees(angle_robot_to_ball) <= 180 or -180 <= np.degrees(angle_robot_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_C:
        # Estágio C: chutar a bola, movendo-a para o gol
        target_x = target_x_final
        target_y = target_y_final
        target_theta = angle_ball_to_target
        robot0.v_max = 1.5
        print("Estado C")
        
        # Se o robô não está mais alinhado com a bola, volta para o estado B
        if not abs(angle_diff) <= 30:
            current_state = STATE_B
        elif 90 <= np.degrees(angle_robot_to_ball) <= 180 or -180 <= np.degrees(angle_robot_to_ball) <= -90:
            current_state = STATE_D

    elif current_state == STATE_D:
        # Estágio D: Evitar a bola nos 2º ou 3º quadrantes
        target_x = ball_position.X - 25
        target_y = ball_position.Y
        target_theta = angle_ball_to_target
        print("Estado D")

        # Evitar a bola ajustando a posição Y do alvo
        if 90 <= np.degrees(angle_robot_to_ball) <= 180:
            target_y -= 20  # Mover o alvo para baixo
        elif -180 <= np.degrees(angle_robot_to_ball) <= -90:
            target_y += 20  # Mover o alvo para cima

        # Verifica se o robô pode transitar de volta para A ou B
        if robot0.target_reached():
            current_state = STATE_B

    # Atualiza o estado atual do atacante
    field.atacante_current_state = current_state

    if ball_position.X >= 380 and 85 <= ball_position.Y <= 200 and robot_position.X >= 370:
        robot0.v_max = 1


    # Move o robô para o ponto alvo
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
        clear_ball(
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
        follow_ball_y(robot0, field, fixed_x=380, target_theta=0)
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

