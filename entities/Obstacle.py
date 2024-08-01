from entities.KinematicBody import KinematicBody


class Obstacle(KinematicBody):
    """Armazena coordenadas e velocidade de um obstáculo para um robô."""

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.is_active = True  # Inicializa como ativo

    def set_obst(self, x, y, rotation):
        """Define as coordenadas do obstáculo com dados da visão."""
        self.set_coordinates(x, y, rotation)

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True
