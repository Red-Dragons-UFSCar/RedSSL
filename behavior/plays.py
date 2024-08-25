from behavior.tactics import goalie, zagueiro


def estrategia_basica(robot_goalie, robot_zagueiro, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """
    goalie(robot_goalie, field)
    zagueiro(robot_zagueiro, field)
