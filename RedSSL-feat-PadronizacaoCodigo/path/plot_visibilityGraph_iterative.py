from path.visibilityGraph import VisibilityGraph
from communication.vision import Vision
from entities.Robot import Robot
from entities.Ball import Ball
from entities.Obstacle import Obstacle
from entities.Field import Field
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import array


# Objeto de visão
visao = Vision(ip="224.5.23.2", port=10020)

# Robos azuis
robot0 = Robot(robot_id=0, actuator=None)
robot1 = Robot(robot_id=1, actuator=None)
robot2 = Robot(robot_id=2, actuator=None)

robots = [robot0, robot1, robot2]

# Robos amarelos
enemy_robot0 = Robot(robot_id=0, actuator=None)
enemy_robot1 = Robot(robot_id=1, actuator=None)
enemy_robot2 = Robot(robot_id=2, actuator=None)

enemy_robots = [enemy_robot0, enemy_robot1, enemy_robot2]

# Bola
ball = Ball()

# Field
field = Field()
field.ball = ball

# Classe de path planning
vg = VisibilityGraph()

# Timer apenas para pegar todas as informações do campo
counter = 0

# Criação do gráfico
fig = plt.figure()

def plot_path(i):
    '''
        Função para realizar o plot do campo com os robôs de obstáculo e o path
    '''

    # ------------------------------
    #  CRIAÇÃO DO GRÁFICO
    # ------------------------------

    plt.cla()
    ax = fig.gca()
    # Limites do gráfico
    ax.set_xlim(left = 000, right = 450)
    ax.set_ylim(top = 300, bottom = 000)

    # ------------------------------
    #  AQUISIÇÃO DAS INFORMAÇÕES DE VISÃO
    # ------------------------------

    counter=0
    while counter < 100:
        # Recebimento dos dados da visão
        visao.update()
        frame = visao.get_last_frame()
        # Detecção dos robôs azuis
        for detection in frame["robots_blue"]:
            for i in range(len(robots)):
                if detection["robot_id"] == i:
                    x_pos = detection["x"]
                    y_pos = detection["y"]
                    theta = detection["orientation"]
                    robots[i].set_coordinates(x_pos, y_pos, theta)
        
        # Detecção dos robôs amarelos
        for detection in frame["robots_yellow"]:
            for i in range(len(robots)):
                if detection["robot_id"] == i:
                    x_pos = detection["x"]
                    y_pos = detection["y"]
                    theta = detection["orientation"]
                    enemy_robots[i].set_coordinates(x_pos, y_pos, theta)
        
        # Detecção da bola
        ball.set_coordinates(frame["ball"]["x"], frame["ball"]["y"])
        
        # Log dos robôs
        print("Robot 0: ", robots[0].get_coordinates().X)
        print("Robot 1: ", robots[1].get_coordinates().X)
        print("Robot 2: ", robots[2].get_coordinates().X)
        print("----")

        counter=counter+1

    # ------------------------------
    #  INÍCIO E FIM DE PATH
    # ------------------------------

    # Definição de origem e target do path
    origin = array([robots[0].get_coordinates().X,
                    robots[0].get_coordinates().Y])
            
    target = array([ball.get_coordinates().X,
                    ball.get_coordinates().Y])
    robots[0].target.set_coordinates(ball.get_coordinates().X, ball.get_coordinates().Y, 0)

    # ------------------------------
    #  DEFINIÇÃO DE OBSTÁCULOS
    # ------------------------------

    vg_obstacles = []

    for robot_field in enemy_robots+robots[1:]:  # Para todos os robôs em campo tirando o 0, defini-los como obstáculo
        obst = Obstacle()
        obst.set_obst(robot_field.get_coordinates().X, 
                      robot_field.get_coordinates().Y, 
                      robot_field.get_coordinates().rotation)
        robot0.map_obstacle.add_obstacle(obst)

    obstacles = robot0.map_obstacle.get_map_obstacle()

    # Obstaculos
    for i in range(len(obstacles)):
        # Criação do triangulo obstaculo
        triangle = vg.robot_triangle_obstacle(obstacles[i], robots[0])
        pts = array(triangle)

        vg_triangle = vg.convert_to_vgPoly(pts)
        vg_obstacles.append(vg_triangle)
    
    # ------------------------------
    #  OBJETOS VISUAIS DO GRÁFICO
    # ------------------------------

    # Criação do path
    vg.update_target_with_obstacles(robot0, field, [robots[0].target.get_coordinates().X], [robots[0].target.get_coordinates().Y], 0)
    path = vg.get_path()

    robot=robots[0]

    # Criação da lista de triangulos e circulos dos obstaculos
    list_triangles = []
    list_circles = []

    for i in range(len(obstacles)):
        # Criação do triangulo obstaculo
        triangle = vg.robot_triangle_obstacle(obstacles[i], robot)
        pts = array(triangle)
        p = Polygon(pts, fill=False) # Triangulo no matplotlib
        list_triangles.append(p)

        vg_triangle = vg.convert_to_vgPoly(pts)
        vg_obstacles.append(vg_triangle)

        # Criação do circulo obstaculo
        center = (obstacles[i].get_coordinates().X,
                    obstacles[i].get_coordinates().Y) # Centro do robô (circulo)
        circle_obst = plt.Circle(center,9, fc='red',ec="red") # Circulo matplotlib
        list_circles.append(circle_obst)
    
    # Robot
    center = (origin[0],origin[1])
    circle = plt.Circle(center,9, fc='blue',ec="blue")

    # Target
    center_target = (target[0],target[1])
    circle_target = plt.Circle(center_target,3, fc='orange',ec="orange")

    # Plot dos triangulos
    for i in range(len(list_triangles)):
        ax.add_patch(list_triangles[i])

    # Plot dos circulos
    for i in range(len(list_circles)):
        ax.add_patch(list_circles[i])

    # Plot do robô base
    ax.add_patch(circle)

    # Plot do target
    ax.add_patch(circle_target)

    # Criação da linha de path
    list_points_path = []
    list_points_path_x = []
    list_points_path_y = []
    for vg_point in path:
        point = (vg_point.x, vg_point.y)
        list_points_path.append(point)
        list_points_path_x.append(vg_point.x)
        list_points_path_y.append(vg_point.y)
    line_path = plt.Line2D(list_points_path_x, list_points_path_y, color='orange')

    # Plot do path
    ax.add_line(line_path)

    robot0.map_obstacle.clear_map()

ani = FuncAnimation(plt.gcf(), plot_path, interval=100)
plt.show()