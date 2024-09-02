from entities.KinematicBody import KinematicBody


class Obstacle(KinematicBody):
    """Armazena coordenadas e velocidade de um obstáculo para um robô."""

    def __init__(self):
        super().__init__()
        self.is_active = True  # Inicializa como ativo
        self.radius = 18

    def set_obst(self, x, y, rotation, radius=None):
        """Define as coordenadas do obstáculo com dados da visão."""
        self.set_coordinates(x, y, rotation)
        if radius is not None:
            self.radius=radius 

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True


class ObstacleMap():
    def __init__(self):
        self.list_obstacles = []

    def add_obstacle(self, obstacle:Obstacle):
        self.list_obstacles.append(obstacle)

    def get_map_obstacle(self):
        return self.list_obstacles
    
    def clear_map(self):
        self.list_obstacles = []
