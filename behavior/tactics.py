from skills import *

def attack_behav(robot0, field):
    ball_coords = field.ball.get_coordinates()
    if (400 < ball_coords.X <= 500) & (87.5 <= ball_coords.Y <= 222.5):
        go_to_point(robot0, 720, ball_coords.Y, field, target_theta=0)
    else:
        va = (450-ball_coords.X, 180-ball_coords.Y)
        vb = (450-ball_coords.X, 158-ball_coords.Y)
        vc = (450-ball_coords.X, 150-ball_coords.Y)
        vd = (450-ball_coords.X, 142-ball_coords.Y)
        ve = (450-ball_coords.X, 120-ball_coords.Y)
        angle1 = math.angle_between(va,vc)
        angle2 = math.angle_between(vb,vc)
        angle3 = math.angle_between(vd,vc)
        angle4 = math.angle_between(ve,vc)
        range1 = (-angle1, -angle2)
        range2 = (angle3, angle4)
        range = random.choice([range1, range2])
        target_theta = random.uniform(range[0], range[1])
        go_to_point(robot0, ball_coords.X, ball_coords.Y, field, target_theta)