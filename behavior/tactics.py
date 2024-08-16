from behavior.skills import follow_ball_y, pursue_ball
import numpy as np

def zagueiro(robot0, field):
    """
    Função que controla o comportamento do robô zagueiro.
    O robô segue a bola no eixo Y quando a bola está no ataque,
    e persegue a bola com alinhamento ofensivo quando está na defesa.

    Parâmetros:
    - robot0: Instância do robô a ser controlado.
    - field: Instância da classe Field.
    """
    # Obtém a posição atual da bola
    offensive_line_x = 450.00  # Meio de campo
    ball_position = field.ball.get_coordinates()
    #print(f"Posição da Bola: X = {ball_position.X}, Y = {ball_position.Y}")

    # Obtém posição atual do robô
    robot_position = robot0.get_coordinates()
    #print(f"Posição do Robô: X = {robot_position.X}, Y = {robot_position.Y}")

    # Obtém a rotação atual do robô (em radianos)
    robot_rotation = robot_position.rotation
    #print(f"Rotação do Robô: {np.degrees(robot_rotation):.2f}°")

    # Calcula o ângulo do robô em relação ao eixo X (em radianos)
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    angle_to_ball = np.arctan2(delta_y, delta_x)
    #print(f"Ângulo do Robô em relação à Bola: {np.degrees(angle_to_ball):.2f}°")

    # Verifica se a bola está no lado ofensivo ou defensivo
    if ball_position.X >= offensive_line_x:
        # A bola está no lado ofensivo
        follow_ball_y(robot0, field)
        #print("Rodando follow_ball_y")
    else:
        # A bola está no lado defensivo
        pursue_ball(robot0, field, target_theta=angle_to_ball)
        #print("Rodando pursue_ball")
