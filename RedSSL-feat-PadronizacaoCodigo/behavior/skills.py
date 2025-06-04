import math
import numpy as np

from entities.Obstacle import Obstacle


def go_to_point(robot0, target_x, target_y, field, target_theta=0, threshold=10):
    """
    Move o robô para as coordenadas especificadas.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo (opcional, padrão é 0).
    - threshold: Limiar de distância para considerar o alvo alcançado (opcional, padrão é 10).
    """
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)
    robot0.set_robot_velocity(
        robot0.target.get_coordinates().X,
        robot0.target.get_coordinates().Y,
        target_theta,
    )

    if robot0.target_reached(threshold):
        robot0.vx = 0
        robot0.vy = 0
        # robot0.w = 0 # Comentário original mantido


def go_to_point_angled(
    robot0, target_x, target_y, field, target_theta=0, threshold=10
):
    """
    Move o robô para as coordenadas especificadas, com velocidades decompostas.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - target_x: Coordenada X do alvo.
    - target_y: Coordenada Y do alvo.
    - field: Instância da classe Field.
    - target_theta: Ângulo alvo para orientar o robô (opcional, padrão é 0).
    - threshold: Limiar de distância para considerar o alvo alcançado (opcional, padrão é 10).
    """
    # Definir o alvo para o robô
    robot0.target.set_target(robot0, (target_x, target_y), field, target_theta)

    # Coordenadas da bola (Nota: 'ball_position' é calculado mas não usado para definir vx, vy diretamente)
    ball_position = field.ball.get_coordinates()

    # Calcula o ângulo entre a POSIÇÃO ATUAL DO ROBÔ (implícito) e o alvo XY
    # A lógica original usava 'angle_ball_to_target' para decompor a velocidade do robô,
    # o que pode ser intencional se o robô deve se mover na direção da bola para o alvo.
    # Se a intenção é mover-se diretamente para (target_x, target_y) a partir da posição atual do robô,
    # o ângulo deveria ser calculado a partir de robot0.get_coordinates().
    angle_to_move = np.arctan2(
        target_y - robot0.get_coordinates().Y, target_x - robot0.get_coordinates().X
    )
    
    # v_max = 1.5 # Esta linha define v_max localmente.
    # Se robot0.v_max é um atributo, a linha acima é desnecessária.
    # Usando robot0.v_max conforme a linha original:
    robot0.vx = robot0.v_max * np.cos(angle_to_move) # Usando angle_to_move
    robot0.vy = robot0.v_max * np.sin(angle_to_move) # Usando angle_to_move

    # Verifica se o robô alcançou o alvo
    if robot0.target_reached(threshold): # Adicionado threshold
        robot0.vx = 0
        robot0.vy = 0


def follow_ball_y(
    robot0, field, fixed_x=None, target_theta=0, lim_sup=300, lim_inf=0
):
    """
    Move o robô para seguir a bola ao longo do eixo Y,
    mantendo uma posição X fixa ou na área do goleiro.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - fixed_x: Coordenada X fixa (opcional, padrão é 150).
    - target_theta: Ângulo alvo (opcional, padrão é 0).
    - lim_sup: Limite superior da coordenada Y para o robô.
    - lim_inf: Limite inferior da coordenada Y para o robô.
    """
    ball_position = field.ball.get_coordinates()

    # Define a coordenada X alvo para o robô
    target_x_robot = fixed_x if fixed_x is not None else 150

    # Define a coordenada Y alvo, limitada por lim_sup e lim_inf
    if ball_position.Y > lim_sup:
        target_y_robot = lim_sup
    elif ball_position.Y < lim_inf:
        target_y_robot = lim_inf
    else:
        target_y_robot = ball_position.Y
    
    # target_y = ball_position.Y # Linha original comentada, mantida

    go_to_point(robot0, target_x_robot, target_y_robot, field, target_theta)

    if robot0.target_reached(15): # Threshold específico de 15
        robot0.vx = 0
        robot0.vy = 0
        robot0.w = 0


def block_ball_y(
    robot0, field, fixed_x=None, target_theta=0, lim_sup=300, lim_inf=0
):
    """
    Move o robô para interceptar a bola ao longo do eixo Y, considerando uma projeção.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - fixed_x: Coordenada X fixa para o robô (opcional, padrão é 150).
    - target_theta: Ângulo alvo (opcional, padrão é 0).
    - lim_sup: Limite superior (não usado diretamente nesta lógica).
    - lim_inf: Limite inferior (não usado diretamente nesta lógica).
    """
    ball_position = field.ball.get_coordinates()
    
    # Coordenada X alvo do robô
    robot_target_x = fixed_x if fixed_x is not None else 150

    # Ponto de referência no gol (para cálculo de ângulo e projeção)
    goal_reference_y = 150
    goal_reference_x = 0 # Assumindo que o gol está em X=0

    # angle_ball_to_goal = np.arctan2( # Não usado diretamente na lógica final
    #     (goal_reference_y - ball_position.Y), (ball_position.X - goal_reference_x)
    # )
    # angle_global = np.pi - angle_ball_to_goal # Variável não utilizada
    # print("Angulo: ", angle_global) # angle_global não está definido aqui

    # Lógica de cálculo do target_y com projeção
    projected_target_y = goal_reference_y # Valor padrão
    final_robot_x = robot_target_x # X do robô pode mudar baseado na lógica

    try:
        if ball_position.X < robot_target_x and ball_position.Y < 100:
            projected_target_y = 60
            final_robot_x = ball_position.X + 10
        elif ball_position.X < robot_target_x and ball_position.Y > 150: # Original era > 150
            projected_target_y = 240
            final_robot_x = ball_position.X + 10
        else:
            if ball_position.X == 0: # Evitar divisão por zero
                projected_target_y = goal_reference_y # Ou outra lógica de fallback
            else:
                # Projeção para interceptar a bola na linha X do robô
                projected_target_y = (
                    (ball_position.X - robot_target_x) / ball_position.X * (goal_reference_y - ball_position.Y) + ball_position.Y
                )
            # final_robot_x permanece robot_target_x neste caso
    except Exception as e: # Capturar exceção de forma mais genérica ou específica
        print(f"Erro no cálculo de block_ball_y: {e}")
        projected_target_y = goal_reference_y # Fallback
        final_robot_x = robot_target_x

    print(f"Block_ball_y - Target Y: {projected_target_y}") # Debug print

    # angle_robot = -angle_ball_to_goal # Comentário original mantido

    go_to_point(robot0, final_robot_x, projected_target_y, field, target_theta)

    if robot0.target_reached(15):
        robot0.vx = 0
        robot0.vy = 0
        robot0.w = 0


def clear_ball(robot0, field, ball_position, robot_position, initial_angle_to_ball):
    """
    Alinha o robô para limpar a bola de forma estratégica, usando uma máquina de estados.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field (contém zagueiro_current_state).
    - ball_position: Coordenadas atuais da bola (objeto com .X, .Y).
    - robot_position: Coordenadas atuais do robô (objeto com .X, .Y).
    - initial_angle_to_ball: Ângulo inicial do robô para a bola (pode ser recalculado).
    """
    STATE_A, STATE_B, STATE_C, STATE_D = "A", "B", "C", "D"

    # Recalcula o ângulo atual do robô para a bola
    current_angle_to_ball = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )

    current_state = field.zagueiro_current_state
    # print(f"Clear Ball - Estado atual: {current_state}")

    approach_offset = -40  # Deslocamento para se posicionar atrás da bola
    
    # Inicializa variáveis de alvo para evitar UnboundLocalError
    target_x, target_y, target_theta = robot_position.X, robot_position.Y, robot_position.rotation

    if current_state == STATE_A:
        # Estado A: Posicionar-se atrás da bola, olhando para frente.
        target_x = ball_position.X + approach_offset
        target_y = ball_position.Y
        target_theta = 0  # Olhar para a direção X positiva
        robot0.v_max = 1.5

        if robot0.target_reached(8):
            current_state = STATE_B
            # print("Clear Ball: A -> B")
        elif (
            90 <= np.degrees(current_angle_to_ball) <= 180 or
            -180 <= np.degrees(current_angle_to_ball) <= -90
        ): # Se a bola estiver atrás do robô
            current_state = STATE_D # Ir para estado de evasão/reposicionamento
            # print("Clear Ball: A -> D (bola atrás)")

    elif current_state == STATE_B:
        # Estado B: Aproximar-se da bola para preparo do chute/limpeza.
        target_x = ball_position.X - 20  # Ponto próximo à bola
        target_y = ball_position.Y
        target_theta = 0 # Manter orientação para frente ou para a bola
        robot0.v_max = 1.25

        if robot0.target_reached(8):
            current_state = STATE_C # Transição corrigida para STATE_C (tentar limpar)
            # print("Clear Ball: B -> C")
        elif (
            90 <= np.degrees(current_angle_to_ball) <= 180 or
            -180 <= np.degrees(current_angle_to_ball) <= -90
        ): # Se a bola estiver atrás
            current_state = STATE_D
            # print("Clear Ball: B -> D (bola atrás)")

    elif current_state == STATE_C: # Corrigido de STATE_B (lógica anterior)
        # Estado C: Limpar a bola (chutar para o meio-campo).
        target_x = 235  # Ex: field.width / 2 + 10
        target_y = ball_position.Y # Chutar reto na direção Y da bola
        target_theta = 0 # Orientar para o campo adversário
        robot0.v_max = 1.25

        # Se não estiver bem alinhado com a bola para o chute, voltar a se posicionar
        if not (-np.pi / 6 < current_angle_to_ball < np.pi / 6):
            current_state = STATE_A # Voltar para A para realinhar
            # print("Clear Ball: C -> A (desalinhado)")
        elif (
            90 <= np.degrees(current_angle_to_ball) <= 180 or
            -180 <= np.degrees(current_angle_to_ball) <= -90
        ): # Se a bola estiver atrás
            current_state = STATE_D
            # print("Clear Ball: C -> D (bola atrás)")
        # Se alinhado, e após o "chute", poderia transitar para A ou um estado de espera.
        # A lógica atual mantém em C se alinhado, o que pode não ser ideal.

    elif current_state == STATE_D:
        # Estado D: Evitar a bola / Reposicionar-se.
        target_x = ball_position.X - 25 # Posição ao lado ou atrás da bola
        target_y = ball_position.Y
        target_theta = 0 # Olhar para frente
        robot0.v_max = 1.5

        # Ajusta Y para contornar a bola se estiver diretamente atrás
        if 90 <= np.degrees(current_angle_to_ball) <= 180: # Bola atrás e à esquerda (do robô)
            target_y -= 20 # Mover "para baixo" do robô
        elif -180 <= np.degrees(current_angle_to_ball) <= -90: # Bola atrás e à direita
            target_y += 20 # Mover "para cima" do robô
        
        if robot0.target_reached(10): # Usar um threshold adequado
            current_state = STATE_A # Tentar se posicionar novamente
            # print("Clear Ball: D -> A")

    field.zagueiro_current_state = current_state
    go_to_point(robot0, target_x, target_y, field, target_theta, threshold=3)


def attack_ball(robot0, field, ball_position, robot_position, current_robot_theta):
    """
    Alinha o robô para atacar a bola em direção ao gol adversário.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field (contém atacante_current_state).
    - ball_position: Coordenadas atuais da bola.
    - robot_position: Coordenadas atuais do robô.
    - current_robot_theta: Ângulo de orientação atual do robô (pode ser usado para target_theta inicial).
    """
    STATE_A, STATE_B, STATE_C, STATE_D = "A", "B", "C", "D"

    # Define o alvo final (centro do gol adversário)
    goal_target_x = 450  # Assumindo X do gol adversário
    goal_target_y_center = 150 # Y central do gol

    # Ajusta o Y do alvo no gol com base na posição da bola para chutes angulados
    if 110 < ball_position.Y < 190: # Se bola na faixa central Y em relação ao gol
        effective_goal_y = ball_position.Y # Chutar reto em Y
        # print("Attack Ball: Mirando Y da bola")
    else:
        # Ajusta o Y para mirar um pouco acima ou abaixo do centro do gol
        effective_goal_y = goal_target_y_center + (-30 if ball_position.Y < goal_target_y_center else 30)

    current_state = field.atacante_current_state

    angle_robot_to_ball = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )
    angle_ball_to_goal = np.arctan2(
        effective_goal_y - ball_position.Y, goal_target_x - ball_position.X
    )

    # Diferença angular para verificar alinhamento robô -> bola -> gol
    # angle_diff_robot_ball_goal = np.degrees(angle_ball_to_goal - angle_robot_to_ball) # Não usado diretamente aqui
    
    approach_offset = -50  # Distância para se posicionar atrás da bola
    kick_approach_offset = -20 # Distância para se aproximar para o "chute"
    threshold = 15         # Limiar para target_reached

    # Inicializar variáveis de alvo
    target_x, target_y, target_theta = robot_position.X, robot_position.Y, current_robot_theta

    if current_state == STATE_A:
        # Estado A: Posicionar-se atrás da bola, alinhado com o gol.
        target_x = ball_position.X + approach_offset * np.cos(angle_ball_to_goal)
        target_y = ball_position.Y + approach_offset * np.sin(angle_ball_to_goal)
        target_theta = angle_ball_to_goal # Robô olha para o gol através da bola
        robot0.v_max = 1.25
        # print("Attack Ball: Estado A")

        if robot0.target_reached(threshold):
            current_state = STATE_B
            # print("Attack Ball: A -> B")
        elif (
            90 <= np.degrees(angle_robot_to_ball) <= 180 or
            -180 <= np.degrees(angle_robot_to_ball) <= -90
        ): # Bola atrás do robô
            current_state = STATE_D # Reposicionar
            # print("Attack Ball: A -> D (bola atrás)")

    elif current_state == STATE_B:
        # Estado B: Aproximar-se da bola para chutar.
        target_x = ball_position.X + kick_approach_offset * np.cos(angle_ball_to_goal)
        target_y = ball_position.Y + kick_approach_offset * np.sin(angle_ball_to_goal)
        target_theta = angle_ball_to_goal
        robot0.v_max = 1.5
        # print("Attack Ball: Estado B")

        if robot0.target_reached(threshold):
            current_state = STATE_C # Pronto para "chutar"
            # print("Attack Ball: B -> C")
        elif (
            90 <= np.degrees(angle_robot_to_ball) <= 180 or
            -180 <= np.degrees(angle_robot_to_ball) <= -90
        ): # Bola atrás
            current_state = STATE_D
            # print("Attack Ball: B -> D (bola atrás)")

    elif current_state == STATE_C:
        # Estado C: "Chutar" a bola em direção ao gol.
        target_x = goal_target_x # Alvo é o próprio gol
        target_y = effective_goal_y
        target_theta = angle_ball_to_goal # Manter orientação para o gol
        # target_theta = 0 # Linha original que zerava theta, pode ser intencional para um tipo de chute
        robot0.v_max = 1.5 # Velocidade máxima para o chute
        # print("Attack Ball: Estado C (Chute)")

        # Verifica se o alinhamento Robô->Bola->Gol se perdeu
        # A lógica original usava 'angle_diff' (robot_ball vs ball_target),
        # aqui verificamos o alinhamento direto do robô com a bola para o gol.
        # Uma condição melhor seria se a bola foi chutada ou se o robô precisa se realinhar.
        # Esta transição é um pouco simplista.
        if not abs(np.degrees(angle_ball_to_goal - angle_robot_to_ball)) <= 30: # Se desalinhado
            current_state = STATE_A # Voltar a se posicionar
            # print("Attack Ball: C -> A (desalinhado para chute)")
        elif (
            90 <= np.degrees(angle_robot_to_ball) <= 180 or
            -180 <= np.degrees(angle_robot_to_ball) <= -90
        ): # Bola atrás
            current_state = STATE_D
            # print("Attack Ball: C -> D (bola atrás)")
        # Idealmente, após o "chute", transitar para um estado de espera ou volta para A.

    elif current_state == STATE_D:
        # Estado D: Evitar a bola / Reposicionar-se.
        # Similar a STATE_A, mas pode ser usado para sair de uma situação ruim.
        target_x = ball_position.X + (approach_offset - 25) * np.cos(angle_robot_to_ball)
        target_y = ball_position.Y + (approach_offset - 25) * np.sin(angle_robot_to_ball)
        target_theta = angle_robot_to_ball # Orientar-se para a bola
        robot0.v_max = 1.5
        # print("Attack Ball: Estado D")

        if robot0.target_reached(threshold + 5): # Um pouco mais de tolerância para sair de D
            current_state = STATE_A # Tentar se posicionar novamente
            # print("Attack Ball: D -> A")

    field.atacante_current_state = current_state

    # Ajusta a velocidade máxima se perto do gol adversário (para precisão)
    if (
        ball_position.X >= 380 and
        85 <= ball_position.Y <= 200 and # Faixa Y do gol
        robot_position.X >= 370
    ):
        robot0.v_max = 1 # Reduzir velocidade

    # Mover o robô
    if current_state == STATE_C: # Se está "chutando"
        go_to_point_angled(robot0, target_x, target_y, field, target_theta, threshold)
    else:
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)


def pursue_ball(robot0, field):
    """
    Faz com que o robô zagueiro persiga a bola ou se posicione para limpá-la.

    Parâmetros:
    - robot0: Instância do robô (zagueiro).
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    if ball_position.X <= 55 and 85 <= ball_position.Y <= 225:
        # Bola na área do goleiro (nosso gol): zagueiro se posiciona para ajudar.
        follow_ball_y(robot0, field, fixed_x=190, target_theta=np.pi) # Ex: linha defensiva
    else:
        # Bola fora da área do goleiro: tentar limpar.
        clear_ball(
            robot0, field, ball_position, robot_position, robot_position.rotation
        )


def shoot(robot0, field):
    """
    Faz com que o robô atacante persiga a bola e tente chutar ao gol.

    Parâmetros:
    - robot0: Instância do robô (atacante).
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # A lógica original de "if ball_position.X >= 400..." com follow_ball_y parecia
    # mais um comportamento defensivo ou de espera se a bola já estivesse muito avançada.
    # Para uma função chamada 'shoot', é mais provável que sempre tente 'attack_ball'.
    # Se um comportamento diferente é desejado quando a bola está na área do gol adversário,
    # a função 'attack_ball' deveria internamente lidar com isso ou uma nova skill.
    attack_ball(
        robot0, field, ball_position, robot_position, robot_position.rotation
    )


def follow_ball_y_elipse(robot0, field, target_theta_initial=0):
    """
    Move o goleiro para acompanhar a bola no eixo Y, ajustando X em uma meia elipse.

    Parâmetros:
    - robot0: O robô goleiro.
    - field: Objeto do campo com informações da bola.
    - target_theta_initial: Ângulo de orientação inicial (será recalculado).
    """
    # robot0.v_max = 1.5 # Descomentar se necessário definir velocidade aqui

    center_x_goal_area = 10  # Posição X de referência central da área do gol
    center_y_goal_area = 150 # Posição Y central da área do gol
    ellipse_a_radius = 40    # Semi-eixo X da elipse (profundidade no gol)
    ellipse_b_radius = 100   # Semi-eixo Y da elipse (largura de cobertura)

    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # Limites de Y para o goleiro se manter na área principal de cobertura
    goal_area_y_min = center_y_goal_area - 60
    goal_area_y_max = center_y_goal_area + 60

    target_y_robot = ball_position.Y
    target_x_robot = center_x_goal_area # Default X

    if goal_area_y_min <= ball_position.Y <= goal_area_y_max:
        # Bola dentro da faixa principal de Y: calcular X na elipse.
        target_y_robot = ball_position.Y
        # Termo dentro da raiz quadrada para a equação da elipse
        sqrt_term = 1 - ((target_y_robot - center_y_goal_area) ** 2) / (ellipse_b_radius ** 2)
        
        if sqrt_term >= 0:
            target_x_robot = center_x_goal_area + ellipse_a_radius * np.sqrt(sqrt_term)
        else:
            # Se, devido a flutuações, target_y_robot estiver fora da elipse verticalmente,
            # manter o X no limite da elipse (ou no centro).
            target_x_robot = center_x_goal_area # Ou o X na borda da elipse (ex: center_x + a)
    else:
        # Bola fora da faixa Y principal (nos "cantos" ou além): posicionar nos limites.
        target_x_robot = center_x_goal_area # Manter X central
        if ball_position.Y < goal_area_y_min:
            target_y_robot = center_y_goal_area - 35 # Limite inferior ajustado
        else: # ball_position.Y > goal_area_y_max
            target_y_robot = center_y_goal_area + 35 # Limite superior ajustado

    # Comentários originais sobre limites em X foram removidos pois a lógica da elipse define X.
    # """
    # if limite_inferior_x <= robot_position.X <= limite_superior_x:
    #     target_x = robot_position.X
    # else:
    #     target_x = 30
    # """

    # Goleiro deve olhar para a bola
    delta_x_to_ball = ball_position.X - robot_position.X
    delta_y_to_ball = ball_position.Y - robot_position.Y
    final_target_theta = np.arctan2(delta_y_to_ball, delta_x_to_ball)

    go_to_point(robot0, target_x_robot, target_y_robot, field, final_target_theta)

    robot0.w = 0 # Forçar parada de rotação; pode ser indesejado se go_to_point já lida com isso.

    if robot0.target_reached(15):
        robot0.vx = 0
        robot0.vy = 0
        robot0.w = 0


def basic_tackle(robot0, field):
    """
    Função de Tackle Básico: robô se posiciona a uma distância da bola, olhando para ela.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    # Ângulo do robô para a bola
    angle_robot_to_ball = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )

    # Distância para se posicionar em relação à bola
    # Original: 100 * np.cos/sin(target_theta), o que posiciona em um círculo de raio 100 *ao redor da bola*.
    # Para um tackle, geralmente se aproxima por trás ou ao lado.
    # Vamos manter a lógica original de posicionar a 100 unidades na direção da bola (o que é estranho).
    # Se a intenção é estar a 100 unidades da bola, o cálculo seria diferente.
    # Assumindo que 'target_theta' é 'angle_robot_to_ball':
    offset_distance = 30 # Distância desejada da bola para o tackle (exemplo)
    target_x = ball_position.X - offset_distance * np.cos(angle_robot_to_ball) # Posição atrás da bola
    target_y = ball_position.Y - offset_distance * np.sin(angle_robot_to_ball)
    target_theta_final = angle_robot_to_ball # Olhar para a bola

    # robot0.v_max = 1.25 # Descomentar para definir velocidade máxima

    go_to_point(robot0, target_x, target_y, field, target_theta_final)


def stay_on_center(robot0, field):
    """
    Move o robô para uma posição central (ex: centro da área do gol) e para.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    # Coordenadas do centro da área do gol (exemplo)
    center_goal_x = 30
    center_goal_y = 150
    
    go_to_point(robot0, center_goal_x, center_goal_y, field, target_theta=0)
    
    if robot0.target_reached(15):
        robot0.vx = 0
        robot0.vy = 0
        robot0.w = 0


def projection_stop_target(robot, field, kicker=False):
    """
    Calcula e define o alvo para um robô em situação de bola parada (stop).

    Se 'kicker' é True (falta ofensiva), projeta o alvo para chutar ao gol adversário.
    Se 'kicker' é False (falta defensiva), projeta para proteger o próprio gol.

    Parâmetros:
    - robot: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - kicker: Booleano, True se o robô é o cobrador da falta.
    """
    ball = field.ball
    ball_coords = ball.get_coordinates()

    # Raio para posicionamento em relação à bola e raio do obstáculo da bola
    positioning_radius = 0
    ball_obstacle_radius = 0
    target_x, target_y, robot_orientation = 0, 0, 0

    if kicker:  # Falta Ofensiva: Robô se posiciona para chutar
        positioning_radius = 20  # Distância atrás da bola para o chute
        ball_obstacle_radius = 10

        opponent_goal_y = 150  # Y do centro do gol adversário
        opponent_goal_x = 450  # X do centro do gol adversário

        angle_ball_to_opponent_goal = np.arctan2(
            (opponent_goal_y - ball_coords.Y), (opponent_goal_x - ball_coords.X)
        )

        target_x = ball_coords.X - positioning_radius * np.cos(angle_ball_to_opponent_goal)
        target_y = ball_coords.Y - positioning_radius * np.sin(angle_ball_to_opponent_goal)
        robot_orientation = angle_ball_to_opponent_goal  # Olhar para o gol adversário
    else:  # Falta Defensiva: Robô forma barreira ou protege o gol
        positioning_radius = 80  # Distância da bola para formar barreira
        ball_obstacle_radius = 20

        # Lógica de quadrantes (originalmente forçada para False, precisa de revisão ou remoção)
        # is_quadrant1 = ball_coords.Y > 230 and ball_coords.X > 300
        # is_quadrant2 = ball_coords.Y < 70 and ball_coords.X > 300
        # is_quadrant1 = False
        # is_quadrant2 = False

        own_goal_y = 150  # Y do centro do próprio gol
        own_goal_x = 0    # X do centro do próprio gol

        # if is_quadrant1:
        #     defense_aim_y, defense_aim_x = 300, 225
        # elif is_quadrant2:
        #     defense_aim_y, defense_aim_x = 0, 225
        # else:
        defense_aim_y, defense_aim_x = own_goal_y, own_goal_x
        
        # Ângulo da bola para o ponto de defesa (nosso gol)
        angle_ball_to_defense_aim = np.arctan2(
            (defense_aim_y - ball_coords.Y), (defense_aim_x - ball_coords.X)
        )
        
        # Robô se posiciona na linha entre a bola e nosso gol, a 'positioning_radius' da bola
        target_x = ball_coords.X + positioning_radius * np.cos(angle_ball_to_defense_aim)
        target_y = ball_coords.Y + positioning_radius * np.sin(angle_ball_to_defense_aim)
        robot_orientation = angle_ball_to_defense_aim + np.pi # Olhar para a bola (de frente)

    # Configura a bola como obstáculo
    obstacle_ball = Obstacle()
    obstacle_ball.set_obst(
        ball_coords.X, ball_coords.Y, 0, radius=ball_obstacle_radius
    )
    robot.map_obstacle.add_obstacle(obstacle_ball)

    # Define o alvo e move o robô
    # A chamada robot.target.set_target pode ser redundante se go_to_point já faz isso.
    # robot.target.set_target(robot, (target_x, target_y), field, robot_orientation)
    go_to_point(robot, target_x, target_y, field, robot_orientation)

    if robot.target_reached(15):
        robot.vx = 0
        robot.vy = 0
        robot.w = 0


def idle_behavior_avoid_ball_stop_game(robot, field):
    """
    Faz o robô ir para seu alvo (previamente definido em robot.target),
    desviando da bola, que é configurada como obstáculo.

    Parâmetros:
    - robot: Instância do robô a ser movido.
    - field: Instância da classe Field.
    """
    ball = field.ball
    target_coords_from_robot = robot.target.get_coordinates() # Alvo já definido no robô

    ball_obstacle_radius = 15

    obstacle_ball = Obstacle()
    obstacle_ball.set_obst(
        ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=ball_obstacle_radius
    )
    robot.map_obstacle.add_obstacle(obstacle_ball) # Path planner usará isso

    target_x_final = target_coords_from_robot.X
    target_y_final = target_coords_from_robot.Y

    # Orientação do robô: Originalmente olhava para a bola.
    # Pode ser melhor olhar para o alvo final ou manter orientação atual.
    orientation_theta = np.arctan2(
        (ball.get_coordinates().Y - robot.get_coordinates().Y),
        (ball.get_coordinates().X - robot.get_coordinates().X),
    )
    # Outra opção:
    # orientation_theta = np.arctan2(
    # (target_y_final - robot.get_coordinates().Y),
    # (target_x_final - robot.get_coordinates().X),
    # )

    go_to_point(robot, target_x_final, target_y_final, field, orientation_theta)

    if robot.target_reached(15):
        robot.vx = 0
        robot.vy = 0
        robot.w = 0


def stop_kickoff_positioning(robot, field, attacking=False, attacker=False):
    """
    Posiciona o robô para uma situação de kickoff, configurando a bola como obstáculo.

    Parâmetros:
    - robot: Instância do robô.
    - field: Instância do campo.
    - attacking: Booleano, True se é kickoff ofensivo para o time do robô.
    - attacker: Booleano, True se este robô é o principal "atacante" no kickoff.
    """
    ball = field.ball
    ball_obstacle_radius = 15  # Raio para evitar a bola

    target_x_pos, target_y_pos = 0, 0

    if attacking:  # Nosso time ataca
        if attacker:  # Robô posicionado para possível chute/avanço
            target_x_pos = 180
            target_y_pos = 150
        else:  # Outro robô em posição de suporte
            target_x_pos = 150
            target_y_pos = 150
    else:  # Nosso time defende
        if attacker:  # Robô mais avançado da defesa (ainda atrás da linha permitida)
            target_x_pos = 155
            target_y_pos = 150
        else:  # Robô mais recuado da defesa
            target_x_pos = 120
            target_y_pos = 150

    obstacle_ball = Obstacle()
    obstacle_ball.set_obst(
        ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=ball_obstacle_radius
    )
    robot.map_obstacle.add_obstacle(obstacle_ball)

    go_to_point(robot, target_x_pos, target_y_pos, field, target_theta=0) # Orientação neutra

    # Para rotação se já estiver orientado (comparação de ângulos)
    angle_diff_rad = robot.get_coordinates().rotation - robot.target.get_coordinates().rotation
    if abs(angle_diff_rad) < (15 * np.pi / 180): # Usar abs e converter para radianos
        robot.w = 0


def penalty_idle_offensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Move os robôs para posições de preparação para um pênalti ofensivo.

    Parâmetros:
    - robot_goleiro: Objeto do robô goleiro.
    - robot_zagueiro: Objeto do robô zagueiro.
    - robot_atacante: Objeto do robô atacante (cobrador).
    - field: Objeto do campo.
    (Nota: 'skills' no docstring original não é um parâmetro direto)
    """
    go_to_point(robot_goleiro, 150, 300, field, target_theta=0)
    go_to_point(robot_zagueiro, 150, 20, field, target_theta=0)
    go_to_point(robot_atacante, 0, 150, field, target_theta=0) # Posição do cobrador


def penalty_idle_offensive_game_on(robot_goleiro, robot_zagueiro, field):
    """
    Move goleiro e zagueiro durante um pênalti ofensivo já em andamento.
    (Atacante é controlado por outra lógica).

    Parâmetros:
    - robot_goleiro: Objeto do robô goleiro.
    - robot_zagueiro: Objeto do robô zagueiro.
    - field: Objeto do campo.
    """
    go_to_point(robot_goleiro, 230, 300, field, target_theta=0)
    go_to_point(robot_zagueiro, 230, 20, field, target_theta=0)


def penalty_idle_defensive(robot_goleiro, robot_zagueiro, robot_atacante, field):
    """
    Move os robôs para posições de preparação para um pênalti defensivo.

    Parâmetros:
    - robot_goleiro: Objeto do robô goleiro.
    - robot_zagueiro: Objeto do robô zagueiro.
    - robot_atacante: Objeto do robô atacante (em posição defensiva).
    - field: Objeto do campo.
    """
    go_to_point(robot_goleiro, 0, 150, field, target_theta=0)  # Goleiro no gol
    go_to_point(robot_zagueiro, 230, 300, field, target_theta=0) # Jogadores fora da área
    go_to_point(robot_atacante, 250, 20, field, target_theta=0)


def penalty_idle_game_on(robot_zagueiro, robot_atacante, field):
    """
    Move zagueiro e atacante durante um pênalti defensivo já em andamento.
    (Goleiro é controlado por outra lógica).

    Parâmetros:
    - robot_zagueiro: Objeto do robô zagueiro.
    - robot_atacante: Objeto do robô atacante.
    - field: Objeto do campo.
    """
    go_to_point(robot_zagueiro, 230, 300, field, target_theta=0)
    go_to_point(robot_atacante, 250, 20, field, target_theta=0)


def attack_ball_fisico(robot0, field, index):
    """
    Alinha o robô (físico) para atacar a bola no gol, usando máquina de estados.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field (contém estados e contadores).
    - index: Índice do robô (para acesso a estados/contadores específicos).
    (Nota: ball_position, robot_position, target_theta não são params diretos, são calculados)
    """
    STATE_A, STATE_B, STATE_C, STATE_R1 = "A", "B", "C", "R1" # Aproximação, Rotação, Chute, Evasão/Reset

    ball_position = field.ball.get_coordinates()
    robot_position = robot0.get_coordinates()

    goal_x_final = 450  # X do gol adversário
    goal_y_center = 150 # Y central do gol

    # Ajusta Y do alvo no gol para chutes angulados
    if 110 < ball_position.Y < 190:
        effective_goal_y = ball_position.Y
    else:
        effective_goal_y = goal_y_center + (-30 if ball_position.Y < goal_y_center else 30)

    # print(f"Atacante States Array: {field.atacante_current_state}") # Debug
    current_state = field.atacante_current_state[index]
    # print(f"Robô {index} - Estado Atual: {current_state}") # Debug

    angle_robot_to_ball = np.arctan2(
        ball_position.Y - robot_position.Y, ball_position.X - robot_position.X
    )
    angle_ball_to_goal = np.arctan2(
        effective_goal_y - ball_position.Y, goal_x_final - ball_position.X
    )

    # angle_diff_degrees = np.degrees(angle_ball_to_goal - angle_robot_to_ball) # Não usado diretamente

    approach_offset = -20  # Distância para se posicionar atrás da bola
    threshold = 10         # Limiar para target_reached
    angle_alignment_threshold_rad = 25 * np.pi / 180 # Tolerância para alinhamento de ângulo

    # Inicializar variáveis de alvo
    target_x, target_y, target_theta = robot_position.X, robot_position.Y, robot_position.rotation

    # print(f"Robô {index} - Contador Stop: {field.counter_attacker_stop[index]}") # Debug

    if current_state == STATE_A:  # Posicionar atrás da bola
        target_x = ball_position.X + approach_offset * np.cos(angle_ball_to_goal)
        target_y = ball_position.Y + approach_offset * np.sin(angle_ball_to_goal)
        target_theta = angle_ball_to_goal
        # robot0.v_max = 1.25
        # print(f"Robô {index} - Estado A: target_x={target_x:.2f}, target_y={target_y:.2f}")

        if robot0.target_reached(threshold):
            robot0.vx = robot0.vy = 0 # Parar movimento translacional
            field.counter_attacker_stop[index] += 1
            if field.counter_attacker_stop[index] > field.threshold_attacker_stop[index]:
                # print(f"Robô {index}: A -> R1 (limite do contador atingido)")
                current_state = STATE_R1
                field.counter_attacker_stop[index] = 0
        elif (
            90 <= np.degrees(angle_robot_to_ball) <= 180 or
            -180 <= np.degrees(angle_robot_to_ball) <= -90
        ): # Bola atrás do robô
            field.counter_attacker_stop[index] = 0
            current_state = STATE_C # Ir para estado de recuo/reposicionamento
            # print(f"Robô {index}: A -> C (bola atrás)")
        else: # Ainda se movendo para o alvo, resetar contador
            field.counter_attacker_stop[index] = 0
    
    elif current_state == STATE_R1:  # Rotacionar para alinhar
        # print(f"Robô {index} - Estado R1: Rotação")
        # Idealmente, o robô para de transladar e apenas rotaciona.
        # Manter posição atual para rotação no lugar.
        target_x = robot_position.X
        target_y = robot_position.Y
        
        # Ajuste de ângulo (lógica original mantida)
        add_angle_rad = 0
        if ball_position.Y > 130:
            add_angle_rad = 10 * np.pi / 180
        target_theta = angle_ball_to_goal + add_angle_rad # Alinhar com o gol + ajuste

        robot0.vx = 0 # Forçar parada de translação
        robot0.vy = 0

        # Verifica se o robô se moveu demais (deveria estar parado)
        # A condição `not robot0.target_reached(threshold+20)` original era para um alvo diferente.
        # Aqui, verificamos se ele se manteve na posição.
        current_pos_tuple = (robot_position.X, robot_position.Y)
        target_pos_tuple = (target_x, target_y) # Que é a própria posição
        # Esta checagem de target_reached pode não ser ideal para rotação no lugar.
        
        # Checa se a orientação está correta
        current_orientation_error = abs(robot_position.rotation - target_theta)
        # Normalizar o erro angular para o intervalo [-pi, pi] se necessário
        # current_orientation_error = abs(np.arctan2(np.sin(robot_position.rotation - target_theta), np.cos(robot_position.rotation - target_theta))))

        if current_orientation_error < angle_alignment_threshold_rad:
            robot0.w = 0 # Parar rotação
            field.counter_attacker_stop[index] += 1
            if field.counter_attacker_stop[index] > 3 * field.threshold_attacker_stop[index]:
                # print(f"Robô {index}: R1 -> B (orientado)")
                current_state = STATE_B # Avançar para o chute
                field.counter_attacker_stop[index] = 0
        else: # Ainda rotacionando ou desalinhado
            field.counter_attacker_stop[index] = 0
            # A chamada go_to_point abaixo pode ser para forçar o controle de rotação.
            # Se o robô tem um controle de rotação separado, seria melhor usá-lo.
            # print(f"Robô {index} em R1 - Ainda rotacionando. Erro: {current_orientation_error*180/np.pi:.1f} deg")

    elif current_state == STATE_B:  # Chutar a bola
        # print(f"Robô {index} - Estado B: Chute")
        target_x = goal_x_final
        target_y = effective_goal_y
        target_theta = angle_ball_to_goal # Manter orientação para o gol
        # robot0.v_max = 1.7 # Definir velocidade de chute

        # Lógica de transição original para C (que era Evasão)
        # Após o "chute", o robô deveria ir para um estado de espera ou recuo.
        # A condição de ball_distance < 40 pode ser para verificar se o robô "tocou" a bola.
        ball_distance_to_robot = np.sqrt(
            (ball_position.X - robot_position.X)**2 + (ball_position.Y - robot_position.Y)**2
        )
        if ball_distance_to_robot < 15: # Se muito perto da bola (após o impacto)
            field.counter_attacker_stop[index] += 1
            if field.counter_attacker_stop[index] > 5 * field.threshold_attacker_stop[index]:
                # print(f"Robô {index}: B -> C (após chute, recuar)")
                current_state = STATE_C # Ir para estado de recuo/reset
                # robot0.v_max = 0.5 # Reduzir velocidade
                field.counter_attacker_stop[index] = 0
        else: # Se a bola está longe, mas está em estado de "chute", algo não ocorreu como esperado.
              # Poderia voltar para A para tentar novamente.
            # print(f"Robô {index}: B -> A (bola longe durante estado de chute)")
            current_state = STATE_A
            field.counter_attacker_stop[index] = 0
            
    elif current_state == STATE_C:  # Estado de Evasão / Recuo / Reset
        # print(f"Robô {index} - Estado C: Evasão/Reset")
        # Afastar-se da bola ou de uma posição congestionada
        target_x = robot_position.X - 30 * np.cos(angle_robot_to_ball + np.pi) # Recuar
        target_y = robot_position.Y - 30 * np.sin(angle_robot_to_ball + np.pi)
        target_theta = angle_ball_to_goal # Manter olhando para o gol
        # robot0.v_max = 1.0

        if robot0.target_reached(threshold + 5): # Se chegou ao ponto de recuo
            # print(f"Robô {index}: C -> A (recuo completo)")
            current_state = STATE_A # Voltar ao estado inicial de posicionamento

    field.atacante_current_state[index] = current_state
    field.send_local = False # Default: usar path planning normal

    # Movimentação baseada no estado
    if current_state == STATE_B: # Chute
        field.send_local = True # Habilitar controle direto de velocidade para o chute
        # robot0.v_max é definido no estado B
        # As velocidades vx, vy devem ser calculadas e enviadas se send_local=True
        # A lógica original tinha go_to_point_angled aqui, mas também definia vx,vy direto.
        # Se send_local = True, o sistema de controle do robô deve usar vx, vy diretamente.
        robot0.vx = robot0.v_max * np.cos(target_theta)
        robot0.vy = robot0.v_max * np.sin(target_theta)
        # robot0.w = 0 # Rotação já deve estar alinhada
        # Não chamar go_to_point se vx, vy são diretos.
        # A chamada go_to_point_angled na original é confusa com a definição direta de vx, vy.
        # Se for para definir um alvo e deixar o controlador decompor, send_local não faria sentido.
        # Assumindo que com send_local=True, vx,vy são os comandos finais.
    elif current_state == STATE_A:
        # robot0.v_max = 1.0
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)
        robot0.w = 0 # Parar rotação se atingiu o alvo
    elif current_state == STATE_C: # Evasão/Reset
        # robot0.v_max = 1.0
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)
        robot0.w = 0
    elif current_state == STATE_R1: # Rotação
        # robot0.v_max = 1.0 # Não deveria transladar
        # vx, vy já estão zerados neste estado.
        # go_to_point aqui é para forçar a orientação.
        go_to_point(robot0, target_x, target_y, field, target_theta, threshold)
        if abs(robot_position.rotation - target_theta) < angle_alignment_threshold_rad:
             robot0.w = 0 # Para de rotacionar se alinhado


def pursue_ball_fisico(robot0, field, index): # Adicionado 'index' que faltava na chamada a attack_ball_fisico
    """
    Faz com que o robô (físico) persiga a bola, usando 'attack_ball_fisico'.
    Se a bola estiver na área do goleiro aliado, o robô se posiciona defensivamente.

    Parâmetros:
    - robot0: Instância do robô a ser movido.
    - field: Instância da classe Field.
    - index: Índice do robô, necessário para `attack_ball_fisico`.
    """
    ball_position = field.ball.get_coordinates()
    # robot_position = robot0.get_coordinates() # Não usado diretamente nesta função

    # Condição para bola na área do goleiro (aliado)
    if ball_position.X <= 70 and 70 <= ball_position.Y <= 240:
        # Bola na nossa área de defesa: atacante se posiciona preventivamente.
        follow_ball_y(robot0, field, fixed_x=190, target_theta=np.pi) # Ex: linha de meio-campo
    else:
        # Bola em outra parte do campo: atacar.
        attack_ball_fisico(robot0, field, index)
        # clear_ball( # clear_ball é geralmente para zagueiros, não atacantes.
        #     robot0, field, ball_position, robot_position, robot_position.rotation
        # )