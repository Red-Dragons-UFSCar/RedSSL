from entities.KinematicBody import KinematicBody
from path.visibilityGraph import VisibilityGraph


class Target(KinematicBody):
    """Classe que representa um alvo no jogo, herdando de KinematicBody."""

    def __init__(self):
        super().__init__()
        self.visibility_graph = VisibilityGraph()  # Inicializa o grafo de visibilidade

    def set_target(self, robot, target_coordinates, field, target_rotation=0):
        """
        Define o alvo para um robô, considerando os obstáculos no campo.

        Parâmetros:
        - robot: instância do robô para o qual o alvo está sendo definido.
        - target_coordinates: tupla (x, y) com as coordenadas do alvo.
        - field: instância do campo de jogo.
        - target_rotation: rotação alvo (padrão é 0).
        """

        # Atualiza o mapa de obstáculos no grafo de visibilidade
        self.visibility_graph.create_obstacle_map(field, robot)

        # Extrai as coordenadas do alvo
        target_x, target_y = target_coordinates

        # Atualiza o alvo considerando os obstáculos
        new_target = self.visibility_graph.update_target_with_obstacles(
            robot, field, [target_x], [target_y], 0
        )

        # Define as coordenadas e a rotação do alvo
        self.set_coordinates(*new_target, target_rotation)
