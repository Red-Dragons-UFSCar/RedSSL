from behavior.tactics import goleiro, zagueiro, atacante, atacante_campo_todo
from behavior.skills import go_to_point


def estrategia_basica(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Função que combina as estratégias do goleiro e do zagueiro.
    Chama as funções goalie e zagueiro para controlar os dois robôs.
    """
    goleiro(robot_goalie, field)
    zagueiro(robot_zagueiro, field)
    atacante(robot_atacante, field)


def posicionar_robos(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Posiciona os robôs em pontos específicos quando o jogo está parado.
    """
    # Defina as posições específicas para os robôs quando o jogo está parado
    #print("Posicionando robô goleiro no ponto específico.")
    go_to_point(robot_goalie, 30, 150, field, 0)

    #print("Posicionando robô zagueiro no ponto específico.")
    go_to_point(robot_zagueiro, 150, 150, field, 0)

    #print("Posicionando robô atacante no ponto específico.")
    go_to_point(robot_atacante, 300, 150, field, 0)

def estrategia_penalti_ofensivo(robot_goleiro, robot_zagueiro, robot_atacante, field, enable):

    if enable == 0 : #posição inicial, antes da cobrança 
        """
        Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
        o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
        """
        go_to_point(robot_goleiro, 30, 150, field, 0)

        go_to_point(robot_zagueiro, 150, 150, field, 0)

        go_to_point(robot_atacante, 220, 150, field, 0)

    else :
        #chamando a função de atacante para cobrança do penalti.
        atacante(robot_atacante, field)


def estrategia_penalti_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, field, enable):
    """
    Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
    o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
    """
    if enable == 0:
        #posicionamento inicial:
        go_to_point(robot_goleiro, 30, 150, field, 0)

        go_to_point(robot_zagueiro, 230, 150, field, 0)

        go_to_point(robot_atacante, 250, 150, field, 0)
    else :
        #chamando a função de goleiro para defender o penalti
        goleiro(robot_goleiro, field)


def estrategia_desvantagem_2(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Quando a bola estiver na defesa, um robô se torna goleiro, o outro zagueiro.
    Quando a bola estiver no ataque, o robô que era goleiro se torna zagueiro e o outro atacante.
    """
    
    goleiro(robot_goalie, field)
    atacante_campo_todo(robot_zagueiro, field)

def estrategia_desvantagem_1(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Quando a bola estiver na defesa, um robô se torna goleiro, o outro zagueiro.
    Quando a bola estiver no ataque, o robô que era goleiro se torna zagueiro e o outro atacante.
    """
    
    goleiro(robot_goalie, field)
