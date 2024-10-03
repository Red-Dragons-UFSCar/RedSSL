from behavior.tactics import goleiro, zagueiro, atacante
from behavior.skills import go_to_point
import behavior.skills as skills


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
        Posciona zagueiro e goleiro em posições fixas no campo de defesa e
        o atacante para cobrar o penalti, em seguida chamadno a função de atacante para cobrança.
        """
        go_to_point(robot_goleiro, 30, 150, field, 0)

        go_to_point(robot_zagueiro, 150, 150, field, 0)

        go_to_point(robot_atacante, 220, 150, field, 0)

    else :
        #chamando a função de atacante para cobrança do penalti.
        atacante(robot_atacante, field)


def estrategia_penalti_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, field, enable):
    """
    Posciona zagueiro e goleiro em posições fixas no campo de defesa e
    o atacante para cobrar o penalti, em seguida chamadno a função de atacante para cobrança.
    """
    if enable == 0:
        #posicionamento inicial:
        go_to_point(robot_goleiro, 30, 150, field, 0)

        go_to_point(robot_zagueiro, 230, 150, field, 0)

        go_to_point(robot_atacante, 250, 150, field, 0)
    else :
        #chamando a função de goleiro para defender o penalti
        goleiro(robot_goleiro, field)


def basic_stop_behaviour_defensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Descrição: Comportamento básico de stop em casos de faltas defensivas, que 
               precisa estar longe da bola. Os robôs desviam da bola e mudam o target
               se estiver perto da bola
    """
    estrategia_basica(robot_goleiro, robot_zagueiro, robot_atacante, field)
    skills.avoid_ball_stop_game(robot_goleiro, field)
    skills.avoid_ball_stop_game(robot_zagueiro, field)
    skills.avoid_ball_stop_game(robot_atacante, field)

def basic_stop_behaviour_ofensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Descrição: Comportamento básico de stop em casos de faltas ofensivas, que 
               precisa estar longe da bola. Os robôs desviam da bola e mudam o target
               se estiver perto da bola. A depender da posição da bola, um robô ou 
               outro vai até a cobrança (kicker)
    """
    estrategia_basica(robot_goleiro, robot_zagueiro, robot_atacante, field)

    ball = field.ball

    skills.avoid_ball_stop_game(robot_goleiro, field)
    if ball.get_coordinates().X < 450/2:
        skills.avoid_ball_stop_game(robot_zagueiro, field, kicker=True)
        skills.avoid_ball_stop_game(robot_atacante, field)
    else:
        skills.avoid_ball_stop_game(robot_zagueiro, field)
        skills.avoid_ball_stop_game(robot_atacante, field, kicker=True)

    


