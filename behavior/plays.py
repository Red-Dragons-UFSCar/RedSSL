from behavior.tactics import goalie, zagueiro
from behavior.skills import go_to_point


def estrategia_basica(robot_goalie, robot_zagueiro, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """
    goalie(robot_goalie, field)
    zagueiro(robot_zagueiro, field)


def posicionar_robos(robot_goalie, robot_zagueiro, field):
    """
    Posiciona os robôs em pontos específicos quando o jogo está parado.
    """
    # Defina as posições específicas para os robôs quando o jogo está parado
    print("Posicionando robô goleiro no ponto específico.")
    go_to_point(robot_goalie, 30, 150, field, 0)

    print("Posicionando robô zagueiro no ponto específico.")
    go_to_point(robot_zagueiro, 150, 150, field, 0)
