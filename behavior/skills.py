import math
import numpy as np

def go_to_point(robot0, target_x, target_y, field, target_theta):
    """
    Move o robô para as coordenadas especificadas.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo (opcional).

    O robô atualiza sua posição utilizando controle PID e para quando atinge o alvo.
    """
    
    # Define o alvo (inclui a atualização do mapa de obstáculos)
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)

    # Atualiza o controle PID e define a velocidade do robô
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )

    # Para o robô ao atingir o alvo
    if robot0.target_reached():
        robot0.vx = 0
        robot0.vy = 0

def follow_ball_y(robot0, field, target_theta=0):
    """
    Move o robô para seguir a bola ao longo do eixo Y,
    mantendo uma posição fixa no eixo X.

    O robô segue a bola somente se ela estiver no lado ofensivo do campo.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    target_x = 355  # Fixa a posição X do robô

    # O robô segue a bola no eixo Y
    target_y = ball_position.Y

    # Define o alvo e atualiza a velocidade do robô
    go_to_point(robot0, target_x, target_y, field, target_theta)

def pursue_ball(robot0, field, target_theta=0):
    """
    Faz com que o robô persiga a bola e se alinhe para o lado ofensivo do campo.
    O robô se aproxima da bola por trás e, em seguida, a transforma em seu alvo.

    - Se o ângulo do robô em relação à bola estiver entre -45° e 45°,
      ele avança 10 unidades além da bola para atacá-la.
    - Caso contrário, ele se posiciona atrás da bola, ajustando sua posição
      para evitar a bola se o robô estiver nos 3º ou 4º quadrantes.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # Calcula o ângulo entre o robô e a bola
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    angle_to_ball = np.arctan2(delta_y, delta_x)

    if -(np.pi)/4 < angle_to_ball < (np.pi)/4:  # Ativado se o ângulo para a bola for entre -45° e 45°
        # O robô avança para atacar a bola, movendo-se 10 unidades além da bola
        print("Atacando a bola!!")
        target_x = ball_position.X  # Avançar 10 unidades além da bola
        target_y = ball_position.Y

        # Aponta diretamente para a bola com o ângulo configurado
        go_to_point(robot0, target_x, target_y, field, angle_to_ball)

    else:
        # O robô se aproxima por trás da bola
        approach_offset = -100  # Define a distância "atrás" da bola
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y

        # Ajusta o alvo para evitar a bola se o robô estiver no 3º ou 4º quadrante
        if 90 <= np.degrees(angle_to_ball) <= 180:
            target_y -= 20  # Desloca o alvo no eixo Y para evitar a bola
            print("Evitando a bola...")
        elif -180 <= np.degrees(angle_to_ball) <= -90:
            target_y += 20  # Desloca o alvo no eixo Y para evitar a bola
            print("Evitando a bola...")

        # Move o robô em direção ao ponto "por trás" da bola
        go_to_point(robot0, target_x, target_y, field, angle_to_ball)