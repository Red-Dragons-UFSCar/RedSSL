import numpy as np


def rotate_vector(v, theta):
    """
    Descrição:
            Função que recebe um vetor v e o rotaciona em theta graus
    Entradas:
            v:      Vetor numpy [1x2]
            theta:  Angulo de rotação do vetor
    """
    # Matriz de rotação
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))

    # Rotação do vetor
    v_rotated = np.matmul(R, v)

    return v_rotated


def unit_vector(vector):
    """
    Descrição:
            Função de normalização de um vetor
    Entradas:
            v:      Vetor numpy [1x2]
    Saídas:
            v_unit: Vetor normalizado numpy [1x2]
    """
    if np.linalg.norm(vector) == 0:
        value = vector
    else:
        value = vector / np.linalg.norm(vector)
    return value


def angle_between(v1, v2):
    """
    Descrição:
            Função que calcula o angulo entre dois vetores
    Entradas:
            v1:     Vetor numpy [1x2]
            v2:     Vetor numpy [1x2]
    Saídas:
            theta:  Angulo entre os dois vetores
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def get_dif(points, dt=1 / 60):
    dif = []

    for i in range(points.shape[0] - 1):
        d_x = (points[i + 1, 0] - points[i, 0]) / dt
        d_y = (points[i + 1, 1] - points[i, 1]) / dt
        dif.append([d_x, d_y])

    return np.array(dif)


def convert_coordinates(robots_blue, robots_yellow, balls, length, width, is_right_side):
    """
    Descrição:
            Função que converte as coordenadas dos robôs e da bola, se necessário, 
            de acordo com o lado do campo (direito ou esquerdo).
    Entradas:
            robots_blue:        Lista de robôs azuis com atributos x, y e orientation.
            robots_yellow:      Lista de robôs amarelos com atributos x, y e orientation.
            balls:              Lista de bolas com atributos x e y.
            length:             Comprimento do campo de jogo.
            width:              Largura do campo de jogo.
            is_right_side:      Booleano que indica se o time está do lado direito do campo.
            convert_coordinates: Booleano que indica se a conversão de coordenadas deve ser realizada.
    Saídas:
            Nenhuma. A função altera os valores das coordenadas dos robôs e da bola diretamente.
    """

    correction_position_x = length / 2
    correction_position_y = width / 2

    if is_right_side:
        for robot in robots_blue + robots_yellow:
            robot.x = (correction_position_x - robot.x) / 10
            robot.y = (correction_position_y - robot.y) / 10   
            robot.orientation = (robot.orientation + np.pi) % (2 * np.pi)

        if balls:
            balls[0].x = (correction_position_x - balls[0].x) / 10
            balls[0].y = (correction_position_y - balls[0].y) / 10

    else:
        for robot in robots_blue + robots_yellow:
            robot.x = (robot.x + correction_position_x) / 10
            robot.y = (robot.y + correction_position_y) / 10

        if balls:
            balls[0].x = (balls[0].x + correction_position_x) / 10
            balls[0].y = (balls[0].y + correction_position_y) / 10


def dot_product(v1, v2):
    """
    Descrição:
            Calcula o produto escalar entre dois vetores
    Entradas:
            v1:     Vetor numpy (1x2) com coordenadas (x,y) do vetor v1 
            v2:     Vetor numpy (1x2) com coordenadas (x,y) do vetor v2
    Saídas:
            v1*v2:  Vetor numpy (1x2) com o produto escalar v1*v2
    """
    return v1[0]*v2[0] + v1[1]*v2[1]


def ortogonal_projection(p_origin, p_line, p_to_project):
    """
    Descrição:
            Calcula a projeção do vetor u = (p_to_project - p_origin) na reta formada
            pelo vetor v = (p_line - p_origin). A sua projeção final é dada pela
            Equação proj = (u*v)/(v*v) . v, sendo * o produto escalar
    Entradas:
            p_origin:           Vetor numpy (1x2) com coordenadas (x,y) do ponto de origem 
            p_line:             Vetor numpy (1x2) com coordenadas (x,y) do ponto formador da reta
            p_to_project:       Vetor numpy (1x2) com coordenadas (x,y) do ponto a ser projetado
    Saídas:
            p_proj:             Vetor numpy (1x2) com coordenadas (x,y) do ponto projetado
            t:                  Fator de projeção 
    """
    v = p_line - p_origin
    u  = p_to_project - p_origin

    t = dot_product(u, v)/dot_product(v, v) 
    p = t * v

    p_proj = p_origin + p

    return p_proj, t