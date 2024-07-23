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
    return vector / np.linalg.norm(vector)


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
