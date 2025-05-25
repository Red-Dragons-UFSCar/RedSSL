import numpy as np
import entities.Robot as Robot


class PID:
    def __init__(self, KP, KD, KI, saturation) -> None:
        """
        Descrição:
                Classe responsável pelo algoritmo de controle
                Proporcional, Integral e Derivativo (PID)
        Entradas:
                KP:     float
                KI:     float
                KD:     float

        TODO: Sincronizar fps com o código da estratégia
        """
        # Constantes do controlador
        self.KP = KP
        self.KD = KD
        self.KI = KI

        # Variaveis para controle
        self.target = 0
        self.actual_value = 0

        # Variaveis para erro
        self.error = 0
        self.last_error = 0
        self.sum_error = 0

        # Framerate do ciclo de controle.
        self.fps = 60

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
        self.actual_value = value


    def set_target(self, target: float) -> None:
        """
        Descrição:
                Função responsável por definir o valor de set point,
                ou seja, o valor de entrada/referência.
        Entradas:
                target:     float
        """
        self.target = target


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
        """
        self.error = self.target - self.actual_value

        u = (
            self.KP * self.error
            + self.KD * (self.error - self.last_error) / (1 / self.fps)
            + self.KI * self.sum_error
        )
        u = self.saturate_control_signal(u)

        self.last_error = self.error
        self.sum_error = self.sum_error + self.error

        self.sum_error = self.saturate_control_signal(self.sum_error)
        return u


    def update_angular(self):
        """
        Descrição:
                Função responsável por calcular a ação de controle angular
                por meio de um controlador PID analógico
        Saídas:
                u:    float

        TODO: Repensar esse controlador, alguns problemas em -180 ocorrem nele
        """


    def update_angular(self):
        """
        Descrição:
                Função responsável por calcular a ação de controle angular
                por meio de um controlador PID analógico
        Saídas:
                u:    float

        TODO: Repensar esse controlador, alguns problemas em -180 ocorrem nele
        """
        # Forma matemática de manter o angulo no intervalo [-pi, pi]
        sin_error = np.sin(self.target - self.actual_value)
        cos_error = np.cos(self.target - self.actual_value)
        self.error = np.arctan2(sin_error, cos_error)

        u = (
            self.KP * self.error
            + self.KD * (self.error - self.last_error) / (1 / self.fps)
            + self.KI * self.sum_error
        )
        u = self.saturate_control_signal(u)

        self.last_error = self.error
        self.sum_error = self.sum_error + self.error
        return u


    def inicializar_controladores_PID(self):
        self.control_PID_x = PID(self.KP, self.KD, self.KI, saturation=2)
        self.control_PID_y = PID(self.KP, self.KD, self.KI, saturation=2)
        self.control_PID_theta = PID(self.KP, self.KD, self.KI, saturation=1)


    def setRobotVelocity(self, robot0):
        if robot0.target is None:
            return 0, 0, 0

        self.control_PID_x.set_target(robot0.target[0])
        self.control_PID_y.set_target(robot0.target[1])
        self.control_PID_theta.set_target(robot0.target[2])

        self.control_PID_x.set_actual_value(robot0.get_coordinates().X)
        vx = self.control_PID_x.update()

        self.control_PID_y.set_actual_value(robot0.get_coordinates().Y)
        vy = self.control_PID_y.update()

        self.control_PID_theta.set_actual_value(robot0.get_coordinates().rotation)
        w = self.control_PID_theta.update_angular()

        robot0.sim_set_global_vel(vx, vy, w)
        return vx, vy, w
