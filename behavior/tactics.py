from skills import *

def attack_behav(robot0, field):
    ball_coords = field.ball.get_coordinates()
    if (800 < ball_coords.X <= 1000) & (200 <= ball_coords.Y <= 400):
        go_to_point(robot0, 720, ball_coords.Y, field, target_theta=0)
    else:
        va = (900-ball_coords.X, 340-ball_coords.Y)
        vb = (900-ball_coords.X, 310-ball_coords.Y)
        vc = (900-ball_coords.X, 300-ball_coords.Y)
        vd = (900-ball_coords.X, 290-ball_coords.Y)
        ve = (900-ball_coords.X, 260-ball_coords.Y)
        angle1 = math.angle_between(va,vc)
        angle2 = math.angle_between(vb,vc)
        angle3 = math.angle_between(vd,vc)
        angle4 = math.angle_between(ve,vc)
        range1 = (-angle1, -angle2)
        range2 = (angle3, angle4)
        range = random.choice([range1, range2])
        target_theta = random.uniform(range[0], range[1])
        go_to_point(robot0, ball_coords.X, ball_coords.Y, field, target_theta)