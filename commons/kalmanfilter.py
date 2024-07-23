import numpy as np
from numpy import power, sqrt

"""
@brief Classe que implementa um Filtro de Kalman para filtrar os dados de posição da bola e dos robôs
"""


class KalmanFilter:

    def __init__(self, print_attr=False):
        """
        @brief Construtor da classe
        """
        # # Atributos Kalman ------------------------------------------------------------------
        # # Variáveis de Estado escolhidas

        # self.posX # Posição em X [m]
        # self.posY # Posição em Y [m]
        # self.velX # Velocidade em X [m/s]
        # self.velY # Velocidade em Y [m/s]

        # self.dt # Intervalo de tempo entre as amostras [s]

        # # Esses ângulos são utilizados para resetar o filtro caso o objeto mude
        # # repentinamente de trajetória, e.g. a bola rebater em algum robô.
        # self.dAngAtual    # Ângulo da direção atual do objeto
        # self.dAngAnterior # Ângulo da direção anterior do objeto

        # self.vtVelocidade # Vetor com a velocidade do objeto.

        # self.x      # Vetor de Estados
        # self.P      # Ganho de Kalman
        # self.x_k_1  # x(k-1) Estado anterior
        # self.P_k_1  # P(k-1) Ganho no tempo anterior
        # self.K      # Kk Ganho de Kalman

        # self.xPred # Matriz de Transicao
        # self.pPred # Matriz de Transicao

        # self.varX # Variacao da posicao em X
        # self.varY # Variacao da posicao em Y

        # # self.ident # Matriz identidade

        # self.A # Matriz de Transicao
        # self.B # Matriz de Controle
        # self.Q # Matriz da covariancia do ruido do processo
        # self.R # Matriz da covariancia do ruida da medicao
        # self.H # Matriz Jacobiana do modelo
        # self.u # Matriz dos coeficientes de desaceleracao(atrito)

        # self.start_parameters()

        # def start_parameters(self):

        self.dt = 1.0 / 60.0  # Intervalo de tempo entre as amostras [s]
        dt = self.dt

        # Matriz de Transicao
        self.A = np.array([[1, 0, dt, 0],
                           [0, 1, 0, dt],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

        self.varX = np.array([0.1])  # Variacao da posicao em X
        self.varY = np.array([0.1])  # Variacao da posicao em Y

        # Matriz dos coeficientes de desaceleracao(atrito)
        self.u = np.array([[-0.05],
                           [-0.05]])

        # Matriz de Controle
        self.B = np.array([[0.5 * (dt * dt), 0],
                           [0, 0.5 * (dt * dt)],
                           [dt, 0],
                           [0, dt]])

        # Matriz da covariancia do ruido do processo
        self.Q = np.array([[(1.0 / 4) * (power(dt, 4)), 0, (1.0 / 2) * (power(dt, 3)), 0],
                           [0, (1.0 / 4) * (power(dt, 4)), 0, (1.0 / 2) * (power(dt, 3))],
                           [(1.0 / 2) * (power(dt, 3)), 0, power(dt, 2), 0],
                           [0, (1.0 / 2) * (power(dt, 3)), 0, power(dt, 2)]])

        # Matriz da covariancia do ruida da medicao
        self.R = np.array([[0.1, 0],
                           [0, 0.1]])

        # Matriz Jacobiana do modelo
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])

        self.posX = 0.0  # Posição em X [m]
        self.posY = 0.0  # Posição em Y [m]
        self.velX = 0.5  # Velocidade em X [m/s]
        self.velY = 0.5  # Velocidade em Y [m/s]
        # posX, posY, velX, velY = self.posX, self.posY, self.velX, self.velY

        # Ganho de Kalman
        # self.P = self.Q.copy()
        self.P = np.eye(4) * 500.

        # Vetor de Estados
        self.x = np.array([[self.posX],
                           [self.posY],
                           [self.velX],
                           [self.velY]])

        # x(k-1) Estado anterior
        self.x_k_1 = np.zeros([4, 1])

        # print(self.x_k_1)

        # P(k-1) Ganho no tempo anterior
        self.P_k_1 = np.identity(4)

        # print(self.P_k_1)

        # Matriz identidade
        # self.ident = np.identity(4)

        # Matriz de Transicao
        self.xPred = self.x.copy()

        # Matriz de Transicao
        self.pPred = self.P.copy()

        self.dAngAtual = 0.0  # Ângulo da direção atual do objeto
        self.dAngAnterior = 0.0  # Ângulo da direção anterior do objeto

        self.vtVelocidade = np.array([[0.0, 0.0]])  # Vetor com a velocidade do objeto

        self.K = np.zeros([4, 2])  # Ganho de Kalman

        if print_attr:
            members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
            for member in members:
                print(f'{member} = {getattr(self, member)}')

    def v_reset_kalman(self, _vt2d_ultima_pos):

        """
        @brief Reseta o Filtro de Kalman

        @param _vt2d_ultima_pos - Última posição do objeto sendo filtrado (robô/bola)
        """

        # _vt2dUltimaPos /= 1e3;
        # x(0,0) = (double)_vt2dUltimaPos.x();
        # x(1,0) = (double)_vt2dUltimaPos.y();

        # print(_vt2dUltimaPos)

        # _vt2dUltimaPos = _vt2dUltimaPos / 1e3
        # self.x[0, 0] = _vt2dUltimaPos.x # <- usando namedtuple
        # self.x[1, 0] = _vt2dUltimaPos.y # <- usando namedtuple
        self.x[0, 0] = _vt2d_ultima_pos[0]  # <- usando numpy.array
        self.x[1, 0] = _vt2d_ultima_pos[1]  # <- usando numpy.array

        # QVector2D vt_aux;
        # double d_modulo = sqrt(pow(x(2),2) + pow(x(3),2));

        # vt_aux.setX(_vt2dUltimaPos.x()-x(0));
        # vt_aux.setY(_vt2dUltimaPos.y()-x(1));

        d_modulo = sqrt(power(self.x[2, 0], 2) + power(self.x[3, 0], 2))

        # vt_aux = vector2d(_vt2dUltimaPos.x - self.x[0, 0], _vt2dUltimaPos.y - self.x[1, 0]) # <- usando namedtuple
        vt_aux = np.array([_vt2d_ultima_pos[0] - self.x[0, 0], _vt2d_ultima_pos[1] - self.x[1, 0]])  # <- usando numpy.array

        # x(2)= (vt_aux*d_modulo).x();
        # x(3)= (vt_aux*d_modulo).y();

        # self.x[2, 0] = (vt_aux * d_modulo).x # <- usando namedtuple
        # self.x[3, 0] = (vt_aux * d_modulo).y # <- usando namedtuple
        self.x[2, 0] = (vt_aux * d_modulo)[0]  # <- usando numpy.array
        self.x[3, 0] = (vt_aux * d_modulo)[1]  # <- usando numpy.array

        # R(0,0) = 1.0;
        # R(1,1) = 1.0;

        self.R[0, 0] = 1.
        self.R[1, 1] = 1.

        # P = ident;

        self.P = np.identity(4)

    def v_atualiza_kalman(self, _vt2d_posicao_atual, print_attr=False):
        """
        @brief Executa o passo de atualização do Filtro de Kalman

        @param _vt2d_posicao_atual - Posição atual do objeto
        @param print_attr - logging
        """

        # Eigen::Matrix<double, 2, 2> sk;
        # Eigen::Matrix<double, 2, 1> zk, yk;

        # sk = np.zeros([2, 2])
        # zk = np.zeros([2, 1])
        # yk = np.zeros([2, 1])

        # _vt2dPosicaoAtual /= 1e3;
        # zk << (double)_vt2dPosicaoAtual.x(),(double)_vt2dPosicaoAtual.y();

        # _vt2dPosicaoAtual = _vt2dPosicaoAtual / 1e3
        # zk = np.array([[float(_vt2dPosicaoAtual.x)], [float(_vt2dPosicaoAtual.y)]]) # <- usando namedtuple
        # zk = np.array([[float(_vt2dPosicaoAtual[0])], [float(_vt2dPosicaoAtual[1])]]) # <- usando numpy.array
        zk = np.array([[_vt2d_posicao_atual[0]],
                       [_vt2d_posicao_atual[1]]])  # <- usando numpy.array

        # yk = zk - H*x_k_1;
        # sk = H*P_k_1*(H.transpose()) + R;
        # K = P_k_1*(H.transpose())*(sk.inverse());
        # x  = x_k_1 + K*yk;
        # P  = (ident - K*H)*P_k_1;

        yk = zk - np.matmul(self.H, self.x_k_1)
        sk = np.matmul(np.matmul(self.H, self.P_k_1), self.H.T) + self.R
        self.K = np.matmul(np.matmul(self.P_k_1, self.H.T), np.linalg.inv(sk))
        self.x = self.x_k_1 + np.matmul(self.K, yk)
        self.P = np.matmul(np.identity(4) - np.matmul(self.K, self.H), self.P_k_1)

        if print_attr:
            print(f'_vt2dPosicaoAtual = {_vt2d_posicao_atual}')
            print(f'zk = {zk}')
            print(f'yk = {yk}')
            # print(f'sk = {sk}')
            print(f'self.H = {self.H}')
            print(f'self.x_k_1 = {self.x_k_1}')

        # if(x(0)+x(1)+x(2)+x(3) > 10e9 || !qIsFinite(x(0)+x(1)+x(2)+x(3)))
        # {
        #     vResetKalman(QVector2D(0,0));
        # }

        if self.x[0, 0] + self.x[1, 0] + self.x[2, 0] + self.x[3, 0] > 10e9:
            # self.vResetKalman(vector2d(0, 0))
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            self.v_reset_kalman(np.array([0.0, 0.0]))
            
    def v_prediz_kalman(self):
        """
        @brief Executa o passo de predição do Filtro de Kalman
        """

        # x_k_1 = A*x + B*u;
        # P_k_1 = (A*P)*A.transpose() + Q;

        self.x_k_1 = np.matmul(self.A, self.x) + np.matmul(self.B, self.u)
        self.P_k_1 = np.matmul(np.matmul(self.A, self.P), self.A.T) + self.Q

    def v_atualiza_matrizes(self, _delta_t):
        """
        @brief Atualiza as matrizes do Filtro de Kalman

        @param _delta_t - Intervalo de tempo entre as amostras [s]
        """

        # dt = _deltaT;
        # A(0,2) = dt;
        # A(1,3) = dt;

        self.dt = _delta_t
        self.A[0, 2] = self.dt
        self.A[1, 3] = self.dt

        # B(0,0) = (0.5)*(dt*dt);
        # B(1,1) = (0.5)*(dt*dt);
        # B(2,0) = dt;
        # B(3,1) = dt;

        self.B[0, 0] = 0.5 * (self.dt * self.dt)
        self.B[1, 1] = 0.5 * (self.dt * self.dt)
        self.B[2, 0] = self.dt
        self.B[3, 1] = self.dt

        # Q(0,0) = (1.0/4)*(pow(dt,4));
        # Q(0,2) = (1.0/2)*(pow(dt,3));
        # Q(1,1) = (1.0/4)*(pow(dt,4));
        # Q(1,3) = (1.0/2)*(pow(dt,3));
        # Q(2,0) = (1.0/2)*(pow(dt,3));
        # Q(2,2) = (pow(dt,2));
        # Q(3,1) = (1.0/2)*(pow(dt,3));
        # Q(3,3) = (pow(dt,2));

        self.Q[0, 0] = (1.0 / 4) * (power(self.dt, 4))
        self.Q[0, 2] = (1.0 / 2) * (power(self.dt, 3))
        self.Q[1, 1] = (1.0 / 4) * (power(self.dt, 4))
        self.Q[1, 3] = (1.0 / 2) * (power(self.dt, 3))
        self.Q[2, 0] = (1.0 / 2) * (power(self.dt, 3))
        self.Q[2, 2] = power(self.dt, 2)
        self.Q[3, 1] = (1.0 / 2) * (power(self.dt, 3))
        self.Q[3, 3] = power(self.dt, 2)

        # vtVelocidade.prepend(QVector2D(x(2),x(3)));

        self.vtVelocidade = np.insert(self.vtVelocidade, 0, [self.x[2, 0], self.x[3, 0]], axis=0)

        # if(vtVelocidade.size() > 1)
        # {
        #     u(0) = (vtVelocidade.at(0).x() - vtVelocidade.at(1).x())*(dt);//-0.05;
        #     u(1) = (vtVelocidade.at(0).y() - vtVelocidade.at(1).y())*(dt);//-0.05;
        # }else {
        #     u(0) = 0.0;
        #     u(1) = 0.0;
        # }

        print(self.vtVelocidade)

        if self.vtVelocidade.shape[0] > 1:
            self.u[0, 0] = (self.vtVelocidade[0][0] - self.vtVelocidade[1][0]) * (self.dt)  # -0.05
            self.u[1, 0] = (self.vtVelocidade[0][1] - self.vtVelocidade[1][1]) * (self.dt)  # -0.05
        else:
            self.u[0, 0] = 0.0
            self.u[1, 0] = 0.0

        # if(vtVelocidade.size() > 2)
        #     vtVelocidade.pop_back();

        if self.vtVelocidade.shape[0] > 2:
            self.vtVelocidade = np.delete(self.vtVelocidade, self.vtVelocidade.shape[0] - 1, 0)

    def v_atualiza_variancia(self, _var_x, _var_y):
        """
        @brief Atualiza a variância em X e Y

        @param _var_x
        @param _var_y
        """

        # R(0,0) = _varX;
        # R(1,1) = _varY;

        self.R[0, 0] = _var_x
        self.R[1, 1] = _var_y

    def vt2d_prediz_futuro(self, _vt_kalman, _x_pred, _p_pred, _d_t, num):
        """
        @brief Realiza a predição de #num passos à frente

        @param _vt_kalman - Vetor com as posições filtradas do objeto
        @param _x_pred - Estado anterior
        @param _p_pred - Ganho no tempo anterior
        @param _d_t - Intervalo de tempo entre as amostras [s]
        @param num - Número de passos para a predição

        @return QVector2D - Posição no futuro
        """

        # Eigen::Matrix<double,4,1> x_k_1_ = xPred, x_k_1_aux;// x(k-1) Estado anterior
        # Eigen::Matrix<double,4,4> p_k_1_ = pPred, p_k_1_aux;// P(k-1) Ganho no tempo anterior
        # Eigen::Matrix<double,4,2> k_ = K;       // Kk Ganho de Kalman

        # double d_modulo;

        # Eigen::Matrix<double,2,2> sk;
        # Eigen::Matrix<double,2,1> zk,yk;

        # vAtualizaVariancia(99,99);

        x_k_1_ = self.xPred.copy()  # x(k-1) Estado anterior
        x_k_1_aux = np.zeros([4, 1])
        p_k_1_ = self.pPred.copy()  # P(k-1) Ganho no tempo anterior
        p_k_1_aux = np.zeros([4, 4])
        k_ = self.K.copy()  # Kk Ganho de Kalman

        d_modulo = 0.0

        sk = np.zeros([2, 2])
        zk = np.zeros([2, 1])
        yk = np.zeros([2, 1])

        self.v_atualiza_variancia(99, 99)

        # for(int i=1;i<=num;i++)
        # {
        #     d_modulo = sqrt(pow(x_k_1_(2),2) + pow(x_k_1_(3),2))/1e3;
        #     vAtualizaMatrizes(i*_d_t);

        #     if(d_modulo*10 > 0.05)
        #     {
        #         x_k_1_aux = A*x_k_1_ + B*u;
        #         p_k_1_aux = (A*p_k_1_)*A.transpose() + Q;

        #         zk << x_k_1_aux(0), x_k_1_aux(1);

        #         yk = zk - H*x_k_1_;
        #         sk = H*p_k_1_aux*(H.transpose()) + R;
        #         k_ = p_k_1_aux*(H.transpose())*(sk.inverse());
        #         x_k_1_  = x_k_1_aux + k_*yk;
        #         p_k_1_  = (ident - k_*H)*p_k_1_aux;
        #     }
        #     else
        #     {
        #         //            QApplication::beep();
        #         return QVector2D(x_k_1_(0),x_k_1_(1));
        #     }
        # }

        for i in range(1, num + 1):

            d_modulo = np.sqrt(power(x_k_1_[2, 0], 2) + power(x_k_1_[3, 0], 2)) / 1e3
            self.v_atualiza_matrizes(i * _d_t)

            if d_modulo * 10 > 0.05:

                x_k_1_aux = np.matmul(self.A, x_k_1_) + np.matmul(self.B, self.u)
                p_k_1_aux = np.matmul(np.matmul(self.A, p_k_1_), self.A.T) + self.Q

                zk[0, 0] = x_k_1_aux[0, 0]
                zk[1, 0] = x_k_1_aux[1, 0]

                yk = zk - np.matmul(self.H, x_k_1_)
                sk = np.matmul(np.matmul(self.H, p_k_1_aux), self.H.T) + self.R
                k_ = np.matmul(np.matmul(p_k_1_aux, self.H.T), np.linalg.inv(sk))
                x_k_1_ = x_k_1_aux + np.matmul(k_, yk)
                p_k_1_ = np.matmul(np.identity(4) - np.matmul(k_, self.H), p_k_1_aux)

            else:

                # beep()
                # return vector2d(x_k_1_[0, 0], x_k_1_[1, 0]) # <- usando namedtuple
                return np.array([x_k_1_[0, 0], x_k_1_[1, 0]])  # <- usando numpy.array

        # return vector2d(x_k_1_[0, 0], x_k_1_[1, 0]) # <- usando namedtuple
        return np.array([x_k_1_[0, 0], x_k_1_[1, 0]])  # <- usando numpy.array

    def v_inicializa_kalman(self, pos):

        i = pos.shape[0] - 1
        pos_x = pos[i, 0]
        pos_y = pos[i, 1]
        vel_x = pos[i, 0] - pos[i - 1, 0]
        vel_y = pos[i, 1] - pos[i - 1, 1]
        self.x = np.array([[pos_x],
                           [pos_y],
                           [vel_x],
                           [vel_y]])
