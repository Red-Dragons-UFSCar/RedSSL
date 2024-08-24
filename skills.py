from entities.Robot import Robot
from entities.Target import Target
from path.visibilityGraph import VisibilityGraph
import numpy as np
import time


def go_to_point(robot0, target_x, target_y, field, target_theta):
    """
    Move o robô para as coordenadas especificadas.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo (opcional).
    """

    # Define o alvo (inclui a atualização do mapa de obstáculos)
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)

    # Atualiza o controle PID e define a velocidade do robô
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )

    if robot0.target_reached():
        robot0.vx = 0
        robot0.vy = 0

#def follow_ball_y(robot0, field):
#    go_to_point(robot0, 0,  field.ball.get_coordinates().Y, field)

def follow_ball_y(robot0, field, target_theta=0):

    """
    Move o goleiro para acompanhar a bola ao longo do eixo Y,
    e ajusta sua posição X para seguir a curva de uma meia elipse,
    mantendo-o dentro da área estabelecida.

    :param robot0: O robô ou goleiro que deve se movimentar.
    :param field: Objeto que fornece as coordenadas da bola.
    :param target_theta: Ângulo desejado de orientação do robô.
    """
    center_x = 250 # posição média do goleiro no gol
    center_y = 300 #centro 
    a = 40
    b = 80

    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()
    
    # Maximmo intervalo de y para ficar na àrea: 
    limite_inferior_y = center_y - 50
    limite_superior_y = center_y + 50

    # Define os limites do intervalo no eixo X (para não ficar louco o robô)
    #limite_inferior_x = target_x - 10
    #limite_superior_x = target_x + 10

    if limite_inferior_y <= ball_position.Y <= limite_superior_y:
        target_y = ball_position.Y #assume mesmo y da bola
    else:
        if ball_position.Y <= limite_inferior_y:
            target_y =  265 #se mantendo no canto mas não sobre a trave
        else:
            target_y = 335 #se mantendo no canto mas não sobre a trave

    #ajustando target_x:

    # Calcula a posição X usando a equação da meia elipse
    if limite_inferior_y <= target_y <= limite_superior_y:
        target_x = center_x + a * np.sqrt(1 - ((target_y - center_y) ** 2) / b**2)
    else:
        # Se fora do intervalo permitido, ajusta X para um valor fixo
        target_x = center_x  # Ou um valor fixo apropriado, se necessário

    """
    função antiga que só anda de lado no gol
    # Verifica se o robô está dentro do intervalo
    if limite_inferior_x <= robot_position.X <= limite_superior_x:
        target_x = robot_position.X  # Mantém a posição X atual
    else:
        target_x = 30  # Fixa posição X do robô em 30
    """

    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    target_theta = np.arctan2(delta_y, delta_x)
    # enviando robô para ponto alvo

    go_to_point(robot0, target_x, target_y, field, target_theta)
    

"""   
função que acompanha na elipse implementada separadamente, mas não está sendo utilizada no momento
def move_goalkeeper(robot0, field, target_theta=0):
  
    # Definindo o centro da área e os parâmetros da meia elipse
    center_x = 35  # Centro da área no eixo X
    center_y = 300  # Centro da área no eixo Y
    a = 10  # Semieixo maior da elipse (variável X)
    b = 70  # Semieixo menor da elipse (variável Y)
    
    # Coordenadas da bola e do robô
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()
    
    # Limites da área de movimento do goleiro
    limite_inferior_y = center_y - b
    limite_superior_y = center_y + b
    
    # Ajusta a posição Y do goleiro
    if limite_inferior_y <= ball_position.Y <= limite_superior_y:
        target_y = ball_position.Y
    else:
        target_y = 270 if ball_position.Y < limite_inferior_y else 330

    # Calcula a posição X usando a equação da meia elipse
    if limite_inferior_y <= target_y <= limite_superior_y:
        target_x = center_x + a * np.sqrt(1 - ((target_y - center_y) ** 2) / b**2)
    else:
        # Se fora do intervalo permitido, ajusta X para um valor fixo
        target_x = center_x  # Ou um valor fixo apropriado, se necessário

    # Calcula o ângulo para orientar o robô
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    target_theta = np.arctan2(delta_y, delta_x)

    # Move o robô para o ponto alvo
    go_to_point(robot0, target_x, target_y, field, target_theta)
"""

def Basic_Tackle(robot0, field):
    """
    função de Tackle Básico (persegue a bola em uma distancia determinada)
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    #calculo do angulo para a bola
    
    delta_x = ball_position.X - robot_position.X
    delta_y = ball_position.Y - robot_position.Y
    target_theta = np.arctan2(delta_y, delta_x)
    
    # enviando robô para ponto alvo 
    go_to_point(robot0, ball_position.X, ball_position.Y, field, target_theta)

def Stay_On_Center(robot0, field):
   go_to_point(robot0, 30, 300, field, 0)