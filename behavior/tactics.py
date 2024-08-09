from behavior.skills import follow_ball_y, pursue_ball

def zagueiro(robot0, field):
    """
    Função que controla o comportamento do robô zagueiro.
    O robô segue a bola no eixo Y quando a bola está no ataque,
    e persegue a bola com alinhamento ofensivo quando está na defesa.

    Parâmetros:
    - robot0: Instância do robô a ser controlado.
    - field: Instância da classe Field.
    """
    # Obtém a posição atual da bola
    offensive_line_x = 450.00 #meio de campo
    ball_position = field.ball.get_coordinates()
    print(f"Posição da Bola: X = {ball_position.X}, Y = {ball_position.Y}")

    # Verifica se a bola está no lado ofensivo ou defensivo
    if ball_position.X >= offensive_line_x:
        # A bola está no lado ofensivo
        follow_ball_y(robot0, field)
        #print("rodando ball_pos_y")
    else:
        # A bola está no lado defensivo
        pursue_ball(robot0, field)
        #print("rodando pursue_ball")