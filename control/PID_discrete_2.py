import numpy as np


class PID_discrete:
    def __init__(self, Kp, Kd, Ki, saturation, N=1) -> None:
        """
        Descrição:
                Classe responsável pelo algoritmo de controle
                Proporcional, Integral e Derivativo discreto
                com filtro (PID-F)
        Entradas:
                Kp:     float
                Ki:     float
                Kd:     float
                saturation:     float
                N:      float

        TODO: Sincronizar fps com o código da estratégia
        """
        # Constantes do controlador
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki

        # Variaveis para controle
        self.target = 0
        self.actual_value = 0

        # Variaveis para erro
        self.error = 0
        self.error_k1 = 0
        self.error_k2 = 0

        # Variaveis de acao de controle
        self.c = 0
        self.c_k1 = 0

        # Framerate do ciclo de controle.
        self.fps = 60
        self.Ts = 1 / 60

        # Valores de saruração do controlador
        self.saturation = saturation

    def set_actual_value(self, value: float) -> None:
        """
        Descrição:
                Função responsável por definir o valor atual da planta
                controlada, ou seja, sua realimentação
        Entradas:
                value:     float
        """
        self.actual_value = value / 100

    def set_target(self, target: float) -> None:
        """
        Descrição:
                Função responsável por definir o valor de set point,
                ou seja, o valor de entrada/referência.
        Entradas:
                target:     float
        """
        self.target = target / 100

    def saturate_control_signal(self, u: float) -> float:
        """
        Descrição:
                Função responsável por saturar a ação de controle, ou seja,
                define a ação de controle máxima como self.saturation.
        Entradas:
                u:              float
        Saídas:
                u_saturated:    float
        """
        if u > self.saturation:
            u_saturated = self.saturation
        elif u < -self.saturation:
            u_saturated = -self.saturation
        else:
            u_saturated = u
        return u_saturated

    def update(self) -> float:
        """
        Descrição:
                Função responsável por calcular a ação de controle linear
                por meio de um controlador PID analógico
        Saídas:
                u:    float

        #TODO: Colocar a parcela integrativa na equação discreta
        """
        self.error = self.target - self.actual_value

        # Constantes para calculo da ação de controle
        self.q0 = self.Kp + self.Kd /self.Ts  + self.Ki * self.Ts
        self.q1 = -self.Kp - 2*self.Kd / self.Ts
        self.q2 = self.Kd / self.Ts

        # Ação de controle
        self.c = self.c_k1 + self.q0*self.error + self.q1*self.error_k1 + self.q2*self.error_k2 
        self.c = self.saturate_control_signal(self.c)

        # Atualização de variaveis
        self.error_k2 = self.error_k1
        self.error_k1 = self.error
        self.c_k1 = self.c

        return self.c

    def update_angular(self):
        """
        Descrição:
                Função responsável por calcular a ação de controle angular
                por meio de um controlador PID analógico
        Saídas:
                u:    float
        """
        # Forma matemática de manter o erro angular no intervalo [-pi, pi]
        sin_error = np.sin(self.target - self.actual_value)
        cos_error = np.cos(self.target - self.actual_value)
        self.error = np.arctan2(sin_error, cos_error)

        # Constantes para calculo da ação de controle
        a1 = self.Kp + self.Kd * self.N
        a2 = self.N * self.Ts - 1 - self.N * self.Kd
        a3 = self.N * self.Ts - 1

        # Ação de controle
        self.c = a1 * self.error + a2 * self.error_k1 - a3 * self.c_k1
        self.c = self.saturate_control_signal(self.c)

        # Atualização de variaveis
        self.error_k2 = self.error_k1
        self.error_k1 = self.error
        self.c_k1 = self.c

        return self.c

    def set_robot_velocity(robot0, control_PID_x, control_PID_y, control_PID_theta):
        if robot0.target is None:
            return 0, 0, 0

        control_PID_x.set_target(robot0.target[0])
        control_PID_y.set_target(robot0.target[1])
        control_PID_theta.set_target(robot0.target[2])

        control_PID_x.set_actual_value(robot0.get_coordinates().X)
        vx = control_PID_x.update()

        control_PID_y.set_actual_value(robot0.get_coordinates().Y)
        vy = control_PID_y.update()

        control_PID_theta.set_actual_value(robot0.get_coordinates().rotation)
        w = control_PID_theta.update_angular()

        robot0.sim_set_global_vel(vx, vy, w)

        return vx, vy, w
