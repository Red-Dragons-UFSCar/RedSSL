from behavior.skills import follow_ball_y, pursue_ball


def zagueiro(robot0, field):
    """
    Função que controla o comportamento do robô zagueiro.
    O robô segue a bola no eixo Y quando a bola está no ataque,
    e persegue a bola com alinhamento ofensivo quando está na defesa.
    """
    offensive_line_x = 225.00  # Meio de campo
    ball_position = field.ball.get_coordinates()

    if ball_position.X >= offensive_line_x:
        follow_ball_y(robot0, field)
    else:
        pursue_ball(robot0, field)
