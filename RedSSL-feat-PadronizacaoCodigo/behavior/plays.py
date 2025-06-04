import numpy as np

from behavior import skills, tactics  
from entities.Obstacle import Obstacle  


def estrategia_basica(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Combina as estratégias básicas do goleiro, zagueiro e atacante.

    Chama as respectivas funções de táticas para controlar os três robôs.
    """
    tactics.goleiro(robot_goalie, field)
    tactics.zagueiro(robot_zagueiro, field)
    tactics.atacante(robot_atacante, field)


def estrategia_basica_real(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Combina estratégias para goleiro, zagueiro e atacante no modo "real".

    Utiliza táticas específicas (_real) para cada robô.
    """
    tactics.goleiro_real_2(robot_goalie, field)
    tactics.zagueiro_real(robot_zagueiro, field)
    tactics.atacante_real(robot_atacante, field)


def estrategia_block_ball_real(
    robot_goalie, robot_zagueiro, robot_atacante, field
):
    """
    Estratégia "real" com foco em bloqueio de bola e ataque em campo todo.

    O goleiro assume uma posição fixa, o zagueiro bloqueia a bola em um X fixo,
    e o atacante cobre o campo todo.
    """
    fixed_point = 80  # Ponto X fixo para o zagueiro bloquear
    tactics.goleiro_real_2(robot_goalie, field, fixed=10)
    skills.block_ball_y(robot_zagueiro, field, fixed_x=fixed_point)
    tactics.atacante_campo_todo_real(robot_atacante, field)

    # A linha abaixo atribui a posição da bola, mas a variável não é usada posteriormente na função.
    # Considere remover se não for necessária para depuração ou lógica futura.
    ball_position = field.ball.get_coordinates()


def estrategia_2_atacantes_real(
    robot_goalie, robot_zagueiro, robot_atacante, field
):
    """
    Estratégia "real" utilizando dois robôs como atacantes em campo todo.

    O goleiro mantém uma posição fixa, enquanto os outros dois robôs
    (originalmente zagueiro e atacante) atuam como atacantes.
    """
    tactics.goleiro_real_2(robot_goalie, field, fixed=22)
    tactics.atacante_campo_todo_real(robot_zagueiro, field)  # Zagueiro como atacante
    tactics.atacante_campo_todo_real(robot_atacante, field) # Atacante


def estrategia_basica_real_1robo(
    robot_goalie, robot_zagueiro, robot_atacante, field
):
    """
    Estratégia "real" focada em um único robô atuando como atacante em campo todo.

    Parâmetros robot_goalie e robot_zagueiro não são utilizados diretamente nesta função,
    mas são mantidos para consistência da interface da estratégia.
    """
    tactics.atacante_campo_todo(robot_atacante, field)


def posicionar_robos(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Posiciona os robôs em pontos específicos pré-definidos no campo.

    Usado geralmente quando o jogo está parado ou para um setup inicial.
    """
    # Posições específicas para os robôs quando o jogo está parado
    # print("Posicionando robô goleiro no ponto específico.") # Comentário original mantido
    skills.go_to_point(robot_goalie, 30, 150, field, target_theta=0)

    # print("Posicionando robô zagueiro no ponto específico.") # Comentário original mantido
    skills.go_to_point(robot_zagueiro, 150, 150, field, target_theta=0)

    # print("Posicionando robô atacante no ponto específico.") # Comentário original mantido
    skills.go_to_point(robot_atacante, 300, 150, field, target_theta=0)


def estrategia_penalty_ofensivo(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Gerencia o posicionamento dos robôs durante uma cobrança de pênalti ofensivo.

    Se o pênalti está para ser cobrado (não em andamento), posiciona os robôs
    de forma estática. Caso contrário (jogo em andamento após cobrança ou outra situação),
    o atacante executa sua tática e os defensores se posicionam.
    """
    if (
        field.penalty_offensive is True  # Use 'is True' para booleans
        and field.game_on_but_is_penalty is False # Use 'is False'
    ):
        # Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
        # o atacante para cobrar o pênalti.
        skills.penalty_idle_offensive(
            robot_goleiro, robot_zagueiro, robot_atacante, field
        )
    else:
        # Jogo em andamento durante ou após o pênalti.
        tactics.atacante(robot_atacante, field)
        skills.penalty_idle_offensive_game_on(
            robot_goleiro, robot_zagueiro, field
        )


def estrategia_penalty_defensivo(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Gerencia o posicionamento dos robôs durante uma defesa de pênalti.

    Se o pênalti está para ser cobrado (não em andamento), posiciona os robôs
    de forma estática para a defesa. Caso contrário (jogo em andamento),
    o goleiro executa sua tática e os outros jogadores se posicionam.
    """
    if (
        field.penalty_defensive is True
        and field.game_on_but_is_penalty is False
    ):
        # Jogo no modo pênalti parado, preparação para a defesa.
        skills.penalty_idle_defensive(
            robot_goleiro, robot_zagueiro, robot_atacante, field
        )
    else:
        # Jogo ativado, robôs se posicionam para o jogo normal ou continuação do pênalti.
        tactics.goleiro(robot_goleiro, field)
        skills.penalty_idle_game_on(robot_zagueiro, robot_atacante, field)


def estrategia_desvantagem_2(
    robot_goalie, robot_zagueiro, robot_atacante, field
):
    """
    Estratégia para situação de desvantagem numérica com 2 robôs ativos.

    O goleiro se mantém, o zagueiro atua como atacante em todo o campo,
    e o atacante original é posicionado em um ponto fixo.
    """
    tactics.goleiro(robot_goalie, field)
    tactics.atacante_campo_todo(robot_zagueiro, field)  # Zagueiro como atacante
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )


def estrategia_desvantagem_1(
    robot_goalie, robot_zagueiro, robot_atacante, field
):
    """
    Estratégia para situação de desvantagem numérica com 1 robô ativo.

    O goleiro original atua como atacante em todo o campo,
    e os outros dois robôs são posicionados em pontos fixos.
    """
    tactics.atacante_campo_todo(robot_goalie, field)  # Goleiro como atacante
    skills.go_to_point(
        robot_zagueiro, 120, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )


def estrategia_desvantagem_0(
    robot_goalie, robot_zagueiro, robot_atacante, field
):
    """
    Estratégia para situação de desvantagem numérica sem robôs de linha ativos.
    (Assumindo que os robôs ainda podem ser movidos para posições fixas).

    Todos os três robôs são movidos para pontos fixos específicos.
    """
    skills.go_to_point(
        robot_goalie, 120, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_zagueiro, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_atacante, 180, 360, field, target_theta=np.pi / 2, threshold=2
    )


def basic_stop_behavior_defensive(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento básico de parada em faltas defensivas.

    Um jogador cerca a ação da bola e outro espera no meio campo,
    a depender da posição da bola.
    """
    ball_coords = field.ball.get_coordinates() # Renomeado para clareza

    tactics.goleiro(robot_goleiro, field)

    # Se a bola está na metade defensiva do campo (ajustar '450 / 2 + 30' conforme dimensão do campo)
    if ball_coords.X < (field.width / 2 + 30):  # Assumindo field.width existe
        skills.projection_stop_target(robot_zagueiro, field)
        skills.projection_stop_target(robot_atacante, field) # Ambos vão para a bola? Lógica a revisar.

        # # Lógica comentada para posicionar um robô no meio-campo
        # x_target_idle = 270
        # y_target_idle = 150
        # robot_idle = robot_atacante # Ou robot_zagueiro dependendo de quem não foi à bola
        # robot_idle.target.set_target(
        #     robot_idle, (x_target_idle, y_target_idle), field, 0
        # )
        # skills.idle_behavior_avoid_ball_stop_game(robot_idle, field)
    else:  # Se a bola está na metade ofensiva do campo
        skills.projection_stop_target(robot_atacante, field)
        skills.projection_stop_target(robot_zagueiro, field) # Ambos vão para a bola? Lógica a revisar.

        # # Lógica comentada para posicionar um robô no meio-campo
        # x_target_idle = 180
        # y_target_idle = 150
        # robot_idle = robot_zagueiro # Ou robot_atacante
        # robot_idle.target.set_target(
        #     robot_idle, (x_target_idle, y_target_idle), field, 0
        # )
        # skills.idle_behavior_avoid_ball_stop_game(robot_idle, field)


def basic_stop_behavior_defensive_desvantagem2(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento de parada defensiva em desvantagem de 2 jogadores.
    """
    # ball_coords = field.ball.get_coordinates() # Variável não utilizada

    tactics.goleiro(robot_goleiro, field)
    skills.projection_stop_target(robot_zagueiro, field)  # Zagueiro vai para a bola
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )


def basic_stop_behavior_defensive_desvantagem1(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento de parada defensiva em desvantagem de 1 jogador.
    """
    # ball_coords = field.ball.get_coordinates() # Variável não utilizada

    skills.projection_stop_target(robot_goleiro, field)  # Goleiro vai para a bola
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_zagueiro, 180, 360, field, target_theta=np.pi / 2, threshold=2
    )


def basic_stop_behavior_defensive_desvantagem0(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento de parada defensiva em desvantagem de 0 jogadores.
    """
    # ball_coords = field.ball.get_coordinates() # Variável não utilizada

    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_zagueiro, 180, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_goleiro, 120, 360, field, target_theta=np.pi / 2, threshold=2
    )


def basic_stop_behavior_offensive(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento básico de parada em faltas ofensivas.

    Um jogador vai para a cobrança e outro espera no meio campo,
    dependendo da posição da bola.
    """
    ball_coords = field.ball.get_coordinates() # Renomeado para clareza

    tactics.goleiro(robot_goleiro, field)

    if ball_coords.X < (field.width / 2):  # Assumindo field.width e que a bola está no campo de defesa/meio
        kicker_robot = robot_zagueiro
        idle_robot = robot_atacante
        idle_target_x = 300
    else:  # Bola no campo de ataque
        kicker_robot = robot_atacante
        idle_robot = robot_zagueiro
        idle_target_x = 180
    
    skills.projection_stop_target(kicker_robot, field, kicker=True)

    # Ponto alvo do robô inativo no meio campo
    idle_target_y = 150 # Centro Y do campo
    idle_robot.target.set_target(
        idle_robot, (idle_target_x, idle_target_y), field, target_theta=0
    )
    skills.idle_behavior_avoid_ball_stop_game(idle_robot, field)


def basic_stop_behavior_offensive_desvantagem_2(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento de parada ofensiva em desvantagem de 2 jogadores.
    """
    # ball_coords = field.ball.get_coordinates() # Variável não utilizada

    tactics.goleiro(robot_goleiro, field)
    skills.projection_stop_target(
        robot_zagueiro, field, kicker=True
    )  # Zagueiro cobra
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    ) # Atacante em posição fixa


def basic_stop_behavior_offensive_desvantagem_1(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento de parada ofensiva em desvantagem de 1 jogador.
    """
    # ball_coords = field.ball.get_coordinates() # Variável não utilizada

    skills.projection_stop_target(
        robot_goleiro, field, kicker=True
    )  # Goleiro cobra
    # Outros robôs em posições fixas
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_zagueiro, 180, 360, field, target_theta=np.pi / 2, threshold=2
    )


def basic_stop_behavior_offensive_desvantagem_0(
    robot_goleiro, robot_zagueiro, robot_atacante, field
):
    """
    Comportamento de parada ofensiva em desvantagem de 0 jogadores.

    Todos os robôs são posicionados em pontos fixos. Um deles (ex: atacante)
    poderia ser designado como cobrador se a lógica de `projection_stop_target`
    fosse adaptada para um robô fixo.
    """
    # ball_coords = field.ball.get_coordinates() # Variável não utilizada

    # Aqui, todos vão para pontos fixos. A cobrança real precisaria de lógica adicional.
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_zagueiro, 180, 360, field, target_theta=np.pi / 2, threshold=2
    )
    skills.go_to_point(
        robot_goleiro, 120, 360, field, target_theta=np.pi / 2, threshold=2
    )


def defensive_kickoff(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de posicionamento para kickoff defensivo.
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, target_theta=0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=False, attacker=False
    )

    # print("Posicionando robô atacante no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_atacante, field, attacking=False, attacker=True
    )


def defensive_kickoff_2(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff defensivo com um robô a menos (2 ativos).
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, target_theta=0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=False, attacker=True # Zagueiro como "attacker" defensivo
    )

    # print("Posicionando robô atacante no ponto específico.") (robô ausente/fixo)
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )


def defensive_kickoff_1(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff defensivo com dois robôs a menos (1 ativo).
    """
    # print("Posicionando robô 'goleiro' (agora jogador de linha) no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_goalie, field, attacking=False, attacker=False # Goleiro como jogador defensivo
    )

    # Robôs zagueiro e atacante em posições fixas (representando ausência)
    # print("Posicionando robô zagueiro no ponto específico.")
    skills.go_to_point(
        robot_zagueiro, 120, 360, field, target_theta=np.pi / 2, threshold=2
    )
    # print("Posicionando robô atacante no ponto específico.")
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )


def offensive_kickoff(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de posicionamento para kickoff ofensivo.
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, target_theta=0)

    # print("Posicionando robô zagueiro no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=True, attacker=False # Zagueiro de suporte
    )

    # print("Posicionando robô atacante no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_atacante, field, attacking=True, attacker=True # Atacante principal
    )


def defensive_kickoff_real(
    robot_goalie, robot_zagueiro, robot_atacante, field
):
    """
    Estratégia de kickoff defensivo "real", configurando a bola como obstáculo.
    """
    ball = field.ball
    obst = Obstacle()  # Configura a bola como obstáculo
    obst.set_obst(
        ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=30
    )
    robot_goalie.map_obstacle.add_obstacle(obst)
    robot_zagueiro.map_obstacle.add_obstacle(obst)
    robot_atacante.map_obstacle.add_obstacle(obst)

    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, target_theta=0)
    skills.go_to_point(robot_zagueiro, 100, 150, field, target_theta=0)
    skills.go_to_point(robot_atacante, 160, 150, field, target_theta=0)


'''
# Bloco de código comentado original mantido para referência.
def penalty_defensivo(robot_goleiro, robot_zagueiro, robot_atacante, field, game_on):
    """
    Posiciona zagueiro e goleiro em posições fixas no campo de defesa e
    o atacante para cobrar o pênalti, em seguida chamando a função de atacante para cobrança.
    """
    if game_on:
        # Quando o jogo ativar, todos se posicionam para o jogo normal
        tactics.goleiro_real_2(robot_goleiro, field)
        skills.go_to_point(robot_zagueiro, 300, 300, field, np.pi)
        skills.go_to_point(robot_atacante, 300, 20, field, np.pi)
    else:
        skills.go_to_point(robot_goleiro, 30, 150, field, np.pi)
        skills.go_to_point(robot_zagueiro, 300, 300, field, np.pi)
        skills.go_to_point(robot_atacante, 300, 20, field, np.pi)
'''


def penalty_defensivo(
    robot_goleiro, robot_zagueiro, robot_atacante, field, game_on
):
    """
    Gerencia o posicionamento dos robôs para defesa de pênalti, com ajustes de rotação.

    Parâmetros:
    - robot_goleiro: Robô goleiro.
    - robot_zagueiro: Robô zagueiro.
    - robot_atacante: Robô atacante.
    - field: Objeto do campo.
    - game_on: Booleano indicando se o jogo está em andamento (após a cobrança).
    """
    threshold = 20
    print("eieiei")  # Debug print, manter se útil

    angle_threshold_rad = 15 * np.pi / 180  # Limiar de ângulo para parar rotação

    if game_on:
        # Jogo em andamento após a cobrança
        tactics.goleiro_real_2(robot_goleiro, field)
        skills.go_to_point(
            robot_zagueiro, 380, 230, field, target_theta=np.pi, threshold=threshold
        )
        skills.go_to_point(
            robot_atacante, 380, 70, field, target_theta=np.pi, threshold=threshold
        )

        # Parar rotação se o robô estiver orientado
        if abs(robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_zagueiro.w = 0
        if abs(robot_atacante.get_coordinates().rotation - robot_atacante.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_atacante.w = 0
    else:
        # Preparação para a cobrança do pênalti
        skills.go_to_point(
            robot_goleiro, 30, 150, field, target_theta=0, threshold=threshold
        )
        skills.go_to_point(
            robot_zagueiro, 380, 230, field, target_theta=np.pi, threshold=threshold
        )
        skills.go_to_point(
            robot_atacante, 380, 70, field, target_theta=np.pi, threshold=threshold
        )

        # Parar rotação se orientado
        if abs(robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_zagueiro.w = 0
            print("zerei 1")  # Debug print
        if abs(robot_goleiro.get_coordinates().rotation - robot_goleiro.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_goleiro.w = 0
            print("zerei 2")  # Debug print
        if abs(robot_atacante.get_coordinates().rotation - robot_atacante.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_atacante.w = 0
            print("zerei 3")  # Debug print


def penalty_ofensivo(
    robot_goleiro, robot_zagueiro, robot_atacante, field, game_on
):
    """
    Gerencia o posicionamento dos robôs para cobrança de pênalti ofensivo.

    Parâmetros:
    - robot_goleiro: Robô goleiro.
    - robot_zagueiro: Robô zagueiro.
    - robot_atacante: Robô cobrador.
    - field: Objeto do campo.
    - game_on: Booleano indicando se o jogo está em andamento (durante/após a cobrança).
    """
    angle_threshold_rad = 15 * np.pi / 180  # Limiar de ângulo para parar rotação

    if game_on:
        # Jogo em andamento, atacante executa sua tática
        tactics.atacante_campo_todo(robot_atacante, field)
        skills.go_to_point(robot_zagueiro, 100, 250, field, target_theta=0)
        if abs(robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_zagueiro.w = 0
        
        skills.go_to_point(robot_goleiro, 30, 150, field, target_theta=0)
        if abs(robot_goleiro.get_coordinates().rotation - robot_goleiro.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_goleiro.w = 0
    else:
        # Preparação para a cobrança do pênalti
        field.send_local = False # Supõe-se que isso afeta o modo de envio de comandos
        skills.go_to_point(robot_goleiro, 30, 150, field, target_theta=0)
        skills.go_to_point(robot_zagueiro, 100, 250, field, target_theta=0)
        skills.go_to_point(robot_atacante, 100, 150, field, target_theta=0) # Posição do cobrador

        # Parar rotação se orientado
        if abs(robot_zagueiro.get_coordinates().rotation - robot_zagueiro.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_zagueiro.w = 0
        if abs(robot_goleiro.get_coordinates().rotation - robot_goleiro.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_goleiro.w = 0
        if abs(robot_atacante.get_coordinates().rotation - robot_atacante.target.get_coordinates().rotation) < angle_threshold_rad:
            robot_atacante.w = 0


def offensive_kickoff_2(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff ofensivo com um robô a menos (2 ativos).
    """
    # print("Posicionando robô goleiro no ponto específico.")
    skills.go_to_point(robot_goalie, 30, 150, field, target_theta=0)

    # print("Posicionando robô 'zagueiro' (agora atacante principal) no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_zagueiro, field, attacking=True, attacker=True
    )

    # print("Posicionando robô 'atacante' (ausente/fixo) no ponto específico.")
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )


def offensive_kickoff_1(robot_goalie, robot_zagueiro, robot_atacante, field):
    """
    Estratégia de kickoff ofensivo com dois robôs a menos (1 ativo).
    """
    # print("Posicionando robô 'goleiro' (agora atacante principal) no ponto específico.")
    skills.stop_kickoff_positioning(
        robot_goalie, field, attacking=True, attacker=True
    )

    # Robôs zagueiro e atacante em posições fixas (representando ausência)
    # print("Posicionando robô zagueiro no ponto específico.")
    skills.go_to_point(
        robot_zagueiro, 120, 360, field, target_theta=np.pi / 2, threshold=2
    )
    # print("Posicionando robô atacante no ponto específico.")
    skills.go_to_point(
        robot_atacante, 150, 360, field, target_theta=np.pi / 2, threshold=2
    )