import sys # Módulo para interagir com o interpretador Python, usado para sair da aplicação (sys.exit)
import os  # Módulo para interagir com o sistema operacional, usado para construir caminhos de arquivos (os.path)
import math # Módulo para funções matemáticas, como pi e conversão de graus/radianos
import socket
import json

# Importações de classes e módulos específicos do PyQt5 para construir a interface gráfica
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QCheckBox, QGroupBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QFrame, QButtonGroup, QSplitter
)
from PyQt5.QtGui import (
    QPixmap, QPainter, QPen, QBrush, QColor, QFont, QPalette, QPolygonF, QFontMetrics # QFontMetrics ADICIONADO AQUI
)
from PyQt5.QtCore import (
    Qt, QRectF, QLineF, QPointF, QSize, QThread, pyqtSignal
)

# Host e porta para abrir o socket
HOST = ''
PORT = 12000

# Thread: socket que recebe informações do código
class UDPListenerThread(QThread):
    message_received = pyqtSignal(str) 

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((HOST, PORT))

        while True:
            msg_bytes, ip_client = server_socket.recvfrom(2048)
            msg_decod = msg_bytes.decode()
            self.message_received.emit(msg_decod)

class SoccerFieldWidget(QWidget): # Define uma classe personalizada que herda de QWidget
    """
    Widget responsável por desenhar o campo de futebol com as dimensões SSL-EL, robôs e bola.
    """
    # --- Constantes de Dimensões do Campo (SSL-EL) em metros ---
    FIELD_TOTAL_LENGTH_M = 5.5      # Comprimento total do campo com áreas de segurança
    FIELD_TOTAL_WIDTH_M = 4.0       # Largura total do campo com áreas de segurança
    FIELD_PLAYING_LENGTH_M = 4.5    # Comprimento da área de jogo (onde os robôs atuam)
    FIELD_PLAYING_WIDTH_M = 3.0     # Largura da área de jogo
    DEFENSE_AREA_WIDTH_M = 1.35     # Largura da área de defesa (ao longo da linha de gol)
    DEFENSE_AREA_DEPTH_M = 0.5      # Profundidade da área de defesa (a partir da linha de gol)
    CENTER_CIRCLE_DIAMETER_M = 1.0  # Diâmetro do círculo central
    GOAL_OPENING_M = 0.8            # Abertura do gol
    GOAL_DEPTH_M = 0.18             # Profundidade do gol
    PENALTY_MARK_X_POS_1_M = 3.0    # Posição X da marca de pênalti (lado esquerdo, a 3m da linha de gol)
    PENALTY_MARK_X_POS_2_M = FIELD_PLAYING_LENGTH_M - 3.0 # Posição X da marca de pênalti (lado direito)
    LINE_THICKNESS_M = 0.01         # Espessura das linhas do campo

    # --- Constantes de Dimensões do Robô (baseado nas regras SSL) ---
    ROBOT_DIAMETER_M = 0.18                         # Diâmetro do robô
    ROBOT_VISION_CENTER_DOT_DIAMETER_M = 0.05       # Diâmetro do círculo central do padrão de visão (50mm)

    # --- Constantes de Dimensões da Bola (baseado nas regras SSL) ---
    BALL_DIAMETER_M = 0.043                         # Diâmetro da bola
    BALL_COLOR = QColor(255, 165, 0)                # Cor laranja para a bola


    def __init__(self, parent=None): # Construtor da classe
        super().__init__(parent) # Chama o construtor da classe pai (QWidget)
        
        # Calcula a proporção (aspect ratio) da área de jogo para redimensionamento
        self.aspect_ratio = self.FIELD_PLAYING_LENGTH_M / self.FIELD_PLAYING_WIDTH_M
        min_width_playing_area = 150 # Define uma largura mínima em pixels para a área de jogo
        # Define o tamanho mínimo do widget, mantendo a proporção calculada
        self.setMinimumSize(int(min_width_playing_area), int(min_width_playing_area / self.aspect_ratio))
        
        self.setAutoFillBackground(True) # Permite que o widget preencha seu fundo automaticamente
        palette = self.palette() # Obtém a paleta de cores atual do widget
        # Define a cor de fundo do widget (representa a área de segurança ao redor do campo)
        palette.setColor(self.backgroundRole(), QColor("#4a1e1e")) # Vermelho escuro para a área de segurança
        self.setPalette(palette) # Aplica a nova paleta ao widget

        self.robots_data = [
            # Time Azul: id, posição x (m), posição y (m), orientação (radianos), cor
            {"id": 0, "x": self.FIELD_PLAYING_LENGTH_M * 0.25, "y": self.FIELD_PLAYING_WIDTH_M * 0.3, "orientation": math.pi / 4, "team_color": QColor("blue")},
            {"id": 1, "x": self.FIELD_PLAYING_LENGTH_M * 0.15, "y": self.FIELD_PLAYING_WIDTH_M * 0.5, "orientation": 0, "team_color": QColor("blue")}, # Exemplo de goleiro
            {"id": 2, "x": self.FIELD_PLAYING_LENGTH_M * 0.25, "y": self.FIELD_PLAYING_WIDTH_M * 0.7, "orientation": -math.pi / 4, "team_color": QColor("blue")},
            # Time Amarelo
            {"id": 3, "x": self.FIELD_PLAYING_LENGTH_M * 0.75, "y": self.FIELD_PLAYING_WIDTH_M * 0.3, "orientation": math.pi * 3/4, "team_color": QColor("yellow")},
            {"id": 4, "x": self.FIELD_PLAYING_LENGTH_M * 0.85, "y": self.FIELD_PLAYING_WIDTH_M * 0.5, "orientation": math.pi, "team_color": QColor("yellow")}, # Exemplo de goleiro
            {"id": 5, "x": self.FIELD_PLAYING_LENGTH_M * 0.75, "y": self.FIELD_PLAYING_WIDTH_M * 0.7, "orientation": -math.pi * 3/4, "team_color": QColor("yellow")},
        ]
        self.ball_data = { # Posição da bola em metros
            "x": self.FIELD_PLAYING_LENGTH_M / 2, # Centro do campo em X
            "y": self.FIELD_PLAYING_WIDTH_M / 2,  # Centro do campo em Y
        }

    # --- Métodos de Desenho ---
    def draw_robot(self, painter, robot_info, pixels_per_meter):
        """Desenha um robô no campo."""
        # Extrai informações do robô do dicionário 'robot_info'
        x_m, y_m = robot_info["x"] / 100, robot_info["y"] / 100     # dados vêm em cm
        orientation_rad, team_color = robot_info["orientation"], robot_info["team_color"]

        # Converte dimensões e posições de metros para pixels
        robot_radius_px = (self.ROBOT_DIAMETER_M / 2.0) * pixels_per_meter
        center_x_px = x_m * pixels_per_meter
        center_y_px = (self.FIELD_PLAYING_WIDTH_M - y_m) * pixels_per_meter     # precisa inverter o referencial y
        
        # DEBUG: verifique se está desenhando corretamente
        # print(f"[Desenho] Robô {robot_info['id']} em ({x_m}, {y_m}) -> px ({center_x_px}, {center_y_px})")
        # print(f"  Raio em px: {robot_radius_px}, Cor válida: {team_color.isValid()}")

        painter.save() # Salva o estado atual do QPainter (transformações, caneta, pincel)
        painter.translate(center_x_px, center_y_px) # Move a origem do sistema de coordenadas para o centro do robô
        painter.rotate(math.degrees(orientation_rad)) # Rotaciona o sistema de coordenadas de acordo com a orientação do robô

        # Desenha o corpo do robô (círculo base)
        painter.setBrush(QColor(50, 50, 50)) # Define a cor de preenchimento (cinza escuro)
        painter.setPen(QPen(Qt.black, 1))    # Define a caneta para a borda (preta, 1 pixel)
        painter.drawEllipse(QPointF(0, 0), robot_radius_px, robot_radius_px) # Desenha a elipse (círculo)

        # Desenha o círculo central do padrão de visão na cor do time
        vision_center_dot_radius_px = (self.ROBOT_VISION_CENTER_DOT_DIAMETER_M / 2.0) * pixels_per_meter
        painter.setBrush(team_color) # Define a cor de preenchimento para a cor do time
        painter.setPen(Qt.NoPen)     # Remove a borda para o ponto de visão
        painter.drawEllipse(QPointF(0, 0), vision_center_dot_radius_px, vision_center_dot_radius_px)
        
        # Desenha um indicador de orientação (linha na "frente" do robô)
        front_indicator_length = robot_radius_px * 0.8 # Comprimento do indicador
        # Define a caneta para o indicador (branca, espessura escalonada)
        painter.setPen(QPen(Qt.white, max(1.0, 2.0 * pixels_per_meter / 100))) 
        painter.drawLine(QPointF(vision_center_dot_radius_px, 0), QPointF(front_indicator_length, 0)) # Desenha a linha

        painter.restore() # Restaura o estado anterior do QPainter

    def draw_ball(self, painter, ball_info, pixels_per_meter):
        """Desenha a bola no campo."""
        x_m, y_m = ball_info["x"] / 100, ball_info["y"] / 100   # dados vêm em cm 
        # Converte dimensões e posições para pixels
        ball_radius_px = (self.BALL_DIAMETER_M / 2.0) * pixels_per_meter
        center_x_px = x_m * pixels_per_meter
        center_y_px = (self.FIELD_PLAYING_WIDTH_M - y_m) * pixels_per_meter     # precisa inverter o referencial y

        painter.save() # Salva estado do painter
        painter.translate(center_x_px, center_y_px) # Move origem para o centro da bola
        
        painter.setBrush(self.BALL_COLOR) # Define cor de preenchimento da bola (laranja)
        # Define caneta para borda sutil da bola (marrom escuro, espessura escalonada)
        painter.setPen(QPen(QColor(100,60,0), max(0.5, 1.0 * pixels_per_meter / 150))) 
        painter.drawEllipse(QPointF(0,0), ball_radius_px, ball_radius_px) # Desenha a bola
        
        painter.restore() # Restaura estado do painter

    def paintEvent(self, event): # Método chamado automaticamente quando o widget precisa ser redesenhado
        super().paintEvent(event) # Chama o paintEvent da classe pai
        painter = QPainter(self) # Cria um objeto QPainter para desenhar neste widget
        painter.setRenderHint(QPainter.Antialiasing) # Habilita antialiasing para desenhos mais suaves

        # Obtém as dimensões atuais do widget
        widget_w, widget_h = float(self.width()), float(self.height())

        if widget_w <= 0 or widget_h <= 0: return # Não desenha se as dimensões forem inválidas

        # --- Cálculo das Dimensões e Escala do Campo ---
        # Calcula as dimensões da área de jogo em pixels, mantendo a proporção
        playing_area_px_w = widget_w
        playing_area_px_h = playing_area_px_w / self.aspect_ratio
        if playing_area_px_h > widget_h: # Se altura calculada exceder a altura do widget
            playing_area_px_h = widget_h # Ajusta altura para caber
            playing_area_px_w = playing_area_px_h * self.aspect_ratio # Recalcula largura com base na nova altura
        
        # Calcula o fator de escala (pixels por metro)
        pixels_per_meter = 1.0 # Valor padrão para evitar divisão por zero
        if self.FIELD_PLAYING_LENGTH_M > 0:
            pixels_per_meter = playing_area_px_w / self.FIELD_PLAYING_LENGTH_M
        
        # Calcula os deslocamentos (offsets) para centralizar a área de jogo no widget
        offset_x = (widget_w - playing_area_px_w) / 2.0
        offset_y = (widget_h - playing_area_px_h) / 2.0
        
        painter.save() # Salva o estado do painter antes de aplicar a translação do campo
        painter.translate(offset_x, offset_y) # Aplica o deslocamento para desenhar o campo centralizado

        # --- Desenho dos Elementos do Campo ---
        # Converte dimensões do campo de metros para pixels usando a escala
        line_thickness_px = max(1.5, self.LINE_THICKNESS_M * pixels_per_meter) 
        defense_area_w_px = self.DEFENSE_AREA_WIDTH_M * pixels_per_meter
        defense_area_d_px = self.DEFENSE_AREA_DEPTH_M * pixels_per_meter
        center_circle_radius_px = (self.CENTER_CIRCLE_DIAMETER_M / 2.0) * pixels_per_meter
        goal_opening_px = self.GOAL_OPENING_M * pixels_per_meter
        goal_depth_px = self.GOAL_DEPTH_M * pixels_per_meter
        penalty_mark_x1_px = self.PENALTY_MARK_X_POS_1_M * pixels_per_meter
        penalty_mark_x2_px = self.PENALTY_MARK_X_POS_2_M * pixels_per_meter
        penalty_mark_radius_px = max(2.0, 0.03 * pixels_per_meter) 

        # Desenha o fundo da área de jogo (gramado)
        painter.fillRect(QRectF(0.0, 0.0, playing_area_px_w, playing_area_px_h), QColor(0, 120, 0)) 

        # Configura a caneta para as linhas do campo
        pen = QPen(QColor(255,255,255, 200), line_thickness_px) # Linhas brancas semi-transparentes
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush) # Sem preenchimento para as formas desenhadas com a caneta

        # Desenha as linhas do campo
        painter.drawRect(QRectF(0.0, 0.0, playing_area_px_w, playing_area_px_h)) # Linha de contorno
        painter.drawLine(QLineF(playing_area_px_w / 2.0, 0.0, playing_area_px_w / 2.0, playing_area_px_h)) # Linha do meio
        painter.drawEllipse(QPointF(playing_area_px_w / 2.0, playing_area_px_h / 2.0), # Círculo central
                            center_circle_radius_px, center_circle_radius_px)
        # Áreas de defesa
        left_da_y = (playing_area_px_h - defense_area_w_px) / 2.0
        painter.drawRect(QRectF(0.0, left_da_y, defense_area_d_px, defense_area_w_px)) # Esquerda
        right_da_x = playing_area_px_w - defense_area_d_px
        painter.drawRect(QRectF(right_da_x, left_da_y, defense_area_d_px, defense_area_w_px)) # Direita
        # Gols
        goal_y_px = (playing_area_px_h - goal_opening_px) / 2.0
        goal_pen = QPen(QColor(220,220,220, 180), line_thickness_px * 1.2) # Caneta diferente para os gols
        painter.setPen(goal_pen)
        painter.drawRect(QRectF(-goal_depth_px, goal_y_px, goal_depth_px, goal_opening_px)) # Gol esquerdo
        painter.drawRect(QRectF(playing_area_px_w, goal_y_px, goal_depth_px, goal_opening_px)) # Gol direito
        # Marcas de pênalti
        painter.setPen(pen) # Volta para a caneta padrão das linhas
        painter.setBrush(QColor(255,255,255,150)) # Preenchimento semi-transparente para as marcas
        painter.drawEllipse(QPointF(penalty_mark_x1_px, playing_area_px_h / 2.0), 
                              penalty_mark_radius_px, penalty_mark_radius_px)
        painter.drawEllipse(QPointF(penalty_mark_x2_px, playing_area_px_h / 2.0),
                              penalty_mark_radius_px, penalty_mark_radius_px)
        
        # --- Desenhar Robôs e Bola ---
        for robot_data in self.robots_data: # Itera sobre a lista de robôs
            self.draw_robot(painter, robot_data, pixels_per_meter) # Chama o método para desenhar cada robô
        self.draw_ball(painter, self.ball_data, pixels_per_meter) # Chama o método para desenhar a bola
        
        painter.restore() # Restaura o estado do painter (remove a translação do campo)
        painter.end()     # Finaliza o uso do QPainter para este evento

    def resizeEvent(self, event): # Método chamado quando o widget é redimensionado
        self.update() # Agenda um redesenho do widget para refletir o novo tamanho
        super().resizeEvent(event) # Chama o método da classe pai
        
    # Função que atuzaliza o campo, convertendo os dados recebidos no formato de robot_data e ball_data
    def load_from_json(self, game_state_json):
        self.robots_data = self.json_to_robot_data(game_state_json)
        self.ball_data = {
            "x": game_state_json["ball"]["x"],
            "y": game_state_json["ball"]["y"]
        }
        self.update()
        
    def json_to_robot_data(self, json_data):
        robots = []
        for i in range(3):
            robots.append({
                "id": i,
                "x": json_data[f"robot{i}"]["x"],
                "y": json_data[f"robot{i}"]["y"],
                "orientation": json_data[f"robot{i}"]["theta"],
                "team_color": QColor("blue"),
            })
        for i in range(3):
            robots.append({
                "id": i + 3,
                "x": json_data[f"enemy_robot{i}"]["x"],
                "y": json_data[f"enemy_robot{i}"]["y"],
                "orientation": json_data[f"enemy_robot{i}"]["theta"],
                "team_color": QColor("yellow"),
            })
        return robots


class MainWindow(QMainWindow): # Define a classe da janela principal, herda de QMainWindow
    SIDEBAR_FIXED_WIDTH = 300 # Largura fixa para as barras laterais em pixels
    LOGO_HEIGHT = 100         # Altura desejada para a logo em pixels

    def __init__(self): # Construtor da janela principal
        super().__init__() # Chama o construtor da classe pai
        self.setWindowTitle("Red Eye - Interface SSL-EL") # Define o título da janela
        self.setMinimumSize(1024, 768) # Define o tamanho mínimo da janela
        self.setFont(QFont("Segoe UI", 9)) # Define uma fonte padrão para a janela

        # Define a folha de estilos (QSS) para customizar a aparência da interface
        self.setStyleSheet("""
            QMainWindow { background-color: #3B0000; } /* Fundo da janela principal */
            QWidget { color: #F5F5F5; font-family: "Segoe UI", Arial, sans-serif; } /* Estilo padrão para widgets */
            QLabel { qproperty-alignment: 'AlignCenter'; padding: 2px; } /* Alinhamento e padding para Labels */
            QLabel#LogoLabel { margin-bottom: 0px; } /* Removida margem para cálculo do espaçador */
            QLabel#TeamTitleLabel, QLabel#RightSidebarTitleLabel { 
                font-size: 14pt; 
                font-weight: bold; 
                color: #fd0000; /* COR ALTERADA PARA VERMELHO PURO */
                padding: 5px 0px; 
            }
            QGroupBox { background-color: #4A0000; border: 1px solid #2C0000; border-radius: 8px; margin-top: 12px; padding: 10px; } /* Estilo para QGroupBox */
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 3px 12px; background-color: #D32F2F; color: #FFFFFF; border-radius: 4px; font-weight: bold; } /* Estilo para o título do QGroupBox */
            QCheckBox { spacing: 5px; padding: 5px; } /* Estilo para QCheckBox */
            QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #8B0000; border-radius: 4px; } /* Indicador do QCheckBox */
            QCheckBox::indicator:unchecked { background-color: #5A2A2A; } /* Indicador não marcado */
            QCheckBox::indicator:checked { background-color: #D32F2F; } /* Indicador marcado */
            QCheckBox::indicator:hover { border: 1px solid #FF6666; } /* Indicador ao passar o mouse */
            QSplitter::handle { background-color: #4A0000; border: 1px solid #2C0000; border-radius: 3px; } /* Manipulador do QSplitter */
            QSplitter::handle:horizontal { width: 5px; margin: 2px 0; } /* Manipulador horizontal */
            QSplitter::handle:vertical { height: 5px; margin: 0 2px; } /* Manipulador vertical */
            QSplitter::handle:hover { background-color: #D32F2F; } /* Manipulador ao passar o mouse */
            QGroupBox QGridLayout QLabel { border: 1px solid #5A2A2A; border-radius: 3px; padding: 4px; background-color: #501010; } /* Labels dentro de tabelas (GridLayout em QGroupBox) */
            QGroupBox QGridLayout QLabel[isHeader="true"] { font-weight: bold; color: #FFCDD2; background-color: #6A0000; } /* Labels de cabeçalho em tabelas */
        """)

        # --- Configuração do Layout Principal ---
        main_widget = QWidget() # Widget container principal
        main_layout = QHBoxLayout(main_widget) # Layout horizontal para o widget principal
        main_layout.setContentsMargins(10,10,10,10) # Define margens para o layout principal

        # Configura as barras laterais e o campo de futebol
        self.setupLeftSidebar()
        self.setupRightSidebar() # Chamado após setupLeftSidebar para usar self.left_layout.spacing()
        self.soccer_field_widget = SoccerFieldWidget() # Cria a instância do widget do campo

        # Cria o QSplitter para dividir a janela em seções redimensionáveis
        splitter = QSplitter(Qt.Horizontal) # Splitter horizontal
        splitter.addWidget(self.left_sidebar_widget) # Adiciona a barra esquerda ao splitter
        splitter.addWidget(self.soccer_field_widget) # Adiciona o campo ao centro do splitter
        splitter.addWidget(self.right_sidebar_widget) # Adiciona a barra direita ao splitter

        # Define como as seções do splitter se comportam ao redimensionar
        splitter.setStretchFactor(0, 0) # Barra esquerda não expande
        splitter.setStretchFactor(1, 1) # Campo central expande para preencher o espaço
        splitter.setStretchFactor(2, 0) # Barra direita não expande
        
        # A linha splitter.setSizes é mantida conforme o código original fornecido pelo usuário.
        # Se o campo não aparecer, esta linha pode ser a causa e pode precisar ser comentada/removida.
        splitter.setSizes([self.SIDEBAR_FIXED_WIDTH, self.width() - (2 * self.SIDEBAR_FIXED_WIDTH) - 20, self.SIDEBAR_FIXED_WIDTH])

        main_layout.addWidget(splitter) # Adiciona o splitter ao layout principal
        self.setCentralWidget(main_widget) # Define o widget principal da QMainWindow

        # --- Conexões de Sinais e Slots ---
        self.cb_opponent.toggled.connect(self.update_left_panel_display)
        self.cb_red_dragons.toggled.connect(self.update_left_panel_display)
        self.cb_elec.toggled.connect(self.update_right_panel_display)
        self.cb_wheels.toggled.connect(self.update_right_panel_display)

        # Atualiza a UI inicial
        self.update_left_panel_display()
        self.update_right_panel_display()
        
        # Comunicação com o código principal
        self.last_udp_message = None
        self.listener_thread = UDPListenerThread()      # Thread de comunicação
        self.listener_thread.message_received.connect(self.receive_message)
        self.listener_thread.start()
        
    def receive_message(self, msg):
        try:
            data = json.loads(msg)
            self.last_udp_message = data  # salva último dado recebido
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON")
            return

        self.display_left_sidebar(data)     # dados para a left bar
        self.update_wheel_speeds(data)      # dados para a right bar
        self.soccer_field_widget.load_from_json(data)       # dados para o campo

    # Função que atuzaliza a left sidebar
    def display_left_sidebar(self, data):
        team = "robot" if self.cb_red_dragons.isChecked() else "enemy_robot"

        for i in range(3):
            key = f"{team}{i}"
            if key in data:
                rob = data[key]
                self.pos_labels[i][0].setText(f"{(rob['x']/100):.2f}")
                self.pos_labels[i][1].setText(f"{(rob['y']/100):.2f}")
                self.pos_labels[i][2].setText(f"{rob['theta']:.2f}")
            else:
                self.pos_labels[i][0].setText("?")
                self.pos_labels[i][1].setText("?")
                self.pos_labels[i][2].setText("?")

        if "ball" in data:
            self.ball_pos_x_label_value.setText(f"{(data['ball']['x']/100):.2f}")
            self.ball_pos_y_label_value.setText(f"{(data['ball']['y']/100):.2f}")

    # Função que atuzaliza a right sidebar (por enquanto não recebemos nada da eletrônica)
    def update_wheel_speeds(self, data):
        wheel_keys = ["FR", "FL", "BR", "BL"]

        for i in range(3):
            robot_key = f"robot{i}"
            if robot_key in data and "wheels" in data[robot_key]:
                wheels = data[robot_key]["wheels"]
                for j, wheel in enumerate(wheel_keys):
                    value = wheels.get(wheel, None)
                    if value is not None:
                        self.wheels_labels[i][j].setText(f"{value:.2f}")
                    else:
                        self.wheels_labels[i][j].setText("?")
            else:
                for j in range(4):
                    self.wheels_labels[i][j].setText("?")

    def create_styled_label(self, text, is_header=False): 
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter) 
        label.setProperty("isHeader", is_header) 
        return label

    def setupLeftSidebar(self): 
        self.left_sidebar_widget = QWidget()
        self.left_sidebar_widget.setFixedWidth(self.SIDEBAR_FIXED_WIDTH) 
        self.left_layout = QVBoxLayout(self.left_sidebar_widget) 
        self.left_layout.setAlignment(Qt.AlignTop) 
        self.left_layout.setSpacing(10) 

        self.logo_label = QLabel() 
        self.logo_label.setObjectName("LogoLabel") 
        script_dir = os.path.dirname(os.path.realpath(__file__)) 
        logo_path = os.path.join(script_dir, "assets", "logoRedEye.png") 

        if os.path.exists(logo_path): 
            pixmap = QPixmap(logo_path) 
            scaled_pixmap = pixmap.scaledToHeight(self.LOGO_HEIGHT, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap) 
            self.logo_label.setAlignment(Qt.AlignCenter) 
            self.left_layout.addWidget(self.logo_label) 
        else:
            print(f"AVISO: Logo não encontrada em {logo_path}") 
            error_logo_spacer = QWidget()
            error_logo_spacer.setFixedHeight(self.LOGO_HEIGHT)
            self.left_layout.addWidget(error_logo_spacer)
        
        self.team_label = QLabel("Red Dragons") 
        self.team_label.setObjectName("TeamTitleLabel") 
        self.left_layout.addWidget(self.team_label)

        self.cb_opponent = QCheckBox("Adversário")
        self.cb_red_dragons = QCheckBox("Red Dragons")
        self.cb_red_dragons.setChecked(True) 
        
        self.left_display_group = QButtonGroup(self) 
        self.left_display_group.setExclusive(True)
        self.left_display_group.addButton(self.cb_opponent)
        self.left_display_group.addButton(self.cb_red_dragons)
        
        self.checkbox_layout_left = QHBoxLayout() 
        self.checkbox_layout_left.addWidget(self.cb_opponent)
        self.checkbox_layout_left.addWidget(self.cb_red_dragons)
        self.checkbox_layout_left.addStretch() 
        self.left_layout.addLayout(self.checkbox_layout_left) 

        self.pos_group = QGroupBox("Posição e Rotação") 
        pos_layout = QGridLayout(self.pos_group) 
        pos_layout.setSpacing(5) 

        pos_layout.addWidget(self.create_styled_label("Robô", True), 0, 0)
        pos_layout.addWidget(self.create_styled_label("Pos.X (m)", True), 0, 1)
        pos_layout.addWidget(self.create_styled_label("Pos.Y (m)", True), 0, 2)
        pos_layout.addWidget(self.create_styled_label("θ (rad)", True), 0, 3)

        self.pos_labels = [] 
        for i in range(3): 
            self.pos_labels.append([])
            robot_label_text = f"Robô {i+1}" 
            pos_layout.addWidget(self.create_styled_label(robot_label_text), i + 1, 0) 
            for j in range(3): 
                lbl = self.create_styled_label("?") 
                self.pos_labels[i].append(lbl) 
                pos_layout.addWidget(lbl, i + 1, j + 1) 
        self.left_layout.addWidget(self.pos_group)

        self.ball_pos_group = QGroupBox("Posição da Bola")
        ball_pos_layout = QGridLayout(self.ball_pos_group)
        ball_pos_layout.setSpacing(5)

        ball_pos_layout.addWidget(self.create_styled_label("Coordenada", True), 0, 0)
        ball_pos_layout.addWidget(self.create_styled_label("Valor (m)", True), 0, 1)
        
        self.ball_pos_x_label_title = self.create_styled_label("Pos.X")
        self.ball_pos_x_label_value = self.create_styled_label("?")
        self.ball_pos_y_label_title = self.create_styled_label("Pos.Y")
        self.ball_pos_y_label_value = self.create_styled_label("?")

        ball_pos_layout.addWidget(self.ball_pos_x_label_title, 1, 0)
        ball_pos_layout.addWidget(self.ball_pos_x_label_value, 1, 1)
        ball_pos_layout.addWidget(self.ball_pos_y_label_title, 2, 0)
        ball_pos_layout.addWidget(self.ball_pos_y_label_value, 2, 1)
        
        self.left_layout.addWidget(self.ball_pos_group)
        
        self.left_layout.addStretch(1) 

    def setupRightSidebar(self): 
        self.right_sidebar_widget = QWidget()
        self.right_sidebar_widget.setFixedWidth(self.SIDEBAR_FIXED_WIDTH)
        self.right_layout = QVBoxLayout(self.right_sidebar_widget) 
        self.right_layout.setAlignment(Qt.AlignTop)
        self.right_layout.setSpacing(10) 

        # --- Espaçador para alinhar títulos ---
        # Adiciona um espaçador no topo da barra direita com a altura da logo da barra esquerda.
        # Como o espaçamento dos layouts é o mesmo (10px), isso deve alinhar os títulos.
        logo_alignment_spacer = QWidget()
        logo_alignment_spacer.setFixedHeight(self.LOGO_HEIGHT) # Usa a altura da logo
        self.right_layout.addWidget(logo_alignment_spacer)
        # --- Fim Espaçador ---

        self.right_sidebar_title_label = QLabel("Informações Eletrônica")
        self.right_sidebar_title_label.setObjectName("RightSidebarTitleLabel") 
        self.right_layout.addWidget(self.right_sidebar_title_label)
        
        self.cb_elec = QCheckBox("Eletrônica")
        self.cb_wheels = QCheckBox("Velo. Rodas")
        self.cb_wheels.setChecked(True) 

        self.right_display_group = QButtonGroup(self) 
        self.right_display_group.setExclusive(True)
        self.right_display_group.addButton(self.cb_elec)
        self.right_display_group.addButton(self.cb_wheels)

        checkbox_layout_right = QHBoxLayout() 
        checkbox_layout_right.addWidget(self.cb_elec)
        checkbox_layout_right.addWidget(self.cb_wheels)
        checkbox_layout_right.addStretch()
        self.right_layout.addLayout(checkbox_layout_right) 

        self.elec_group = QGroupBox("Eletrônica")
        elec_layout = QGridLayout(self.elec_group)
        elec_layout.setSpacing(5)
        elec_layout.setColumnStretch(0, 1); elec_layout.setColumnStretch(1, 2); elec_layout.setColumnStretch(2, 2); elec_layout.setColumnStretch(3, 1); elec_layout.setColumnStretch(4, 2)

        elec_layout.addWidget(self.create_styled_label("Robô", True), 0, 0)
        elec_layout.addWidget(self.create_styled_label("Tensão (V)", True), 0, 1)
        elec_layout.addWidget(self.create_styled_label("Corrente (A)", True), 0, 2)
        elec_layout.addWidget(self.create_styled_label("Loss (%)", True), 0, 3)
        elec_layout.addWidget(self.create_styled_label("Ping (ms)", True), 0, 4)

        self.elec_labels = [] 
        for i in range(3):
            self.elec_labels.append([])
            elec_layout.addWidget(self.create_styled_label(f"Robô {i+1}"), i + 1, 0)
            for j in range(4):
                lbl = self.create_styled_label("?")
                self.elec_labels[i].append(lbl)
                elec_layout.addWidget(lbl, i + 1, j + 1)
        self.right_layout.addWidget(self.elec_group)

        self.wheels_group = QGroupBox("Velocidades")
        wheels_layout = QGridLayout(self.wheels_group)
        wheels_layout.setSpacing(5)
        wheels_layout.addWidget(self.create_styled_label("Robô", True), 0, 0)
        wheel_names = ["FR", "FL", "BR", "BL"] 
        for col_idx, name in enumerate(wheel_names):
            wheels_layout.addWidget(self.create_styled_label(name, True), 0, col_idx + 1)

        self.wheels_labels = [] 
        for i in range(3):
            self.wheels_labels.append([])
            wheels_layout.addWidget(self.create_styled_label(f"Robô {i+1}"), i + 1, 0)
            for j in range(len(wheel_names)):
                lbl = self.create_styled_label("?")
                self.wheels_labels[i].append(lbl)
                wheels_layout.addWidget(lbl, i + 1, j + 1)
        self.right_layout.addWidget(self.wheels_group)
        
        self.right_layout.addStretch(1) 
        self.elec_group.hide() 
        
    def update_left_panel_display(self): 
        is_opponent = self.cb_opponent.isChecked()
        team_name = "Adversários" if is_opponent else "Red Dragons"
        data_prefix = "Op" if is_opponent else "RD"
        
        self.team_label.setText(team_name) 
        self.pos_group.setTitle(f"Posição e Rotação ({data_prefix})")
        
        num_robots_to_display = 3 
        for i in range(num_robots_to_display):
            if i < len(self.pos_labels): 
                 self.pos_labels[i][0].setText("---") 
                 self.pos_labels[i][1].setText("---") 
                 self.pos_labels[i][2].setText("---") 
        
        self.ball_pos_x_label_value.setText("?.??") 
        self.ball_pos_y_label_value.setText("?.??") 

    def update_right_panel_display(self): 
        self.elec_group.setVisible(self.cb_elec.isChecked()) 
        self.wheels_group.setVisible(self.cb_wheels.isChecked()) 
        
        if self.cb_elec.isChecked(): self.right_sidebar_title_label.setText("Info Eletrônica")
        elif self.cb_wheels.isChecked(): self.right_sidebar_title_label.setText("Info Velocidades")
        else: self.right_sidebar_title_label.setText("Informações")

        num_robots_to_display = 3
        if self.cb_elec.isChecked():
            for i in range(num_robots_to_display):
                 if i < len(self.elec_labels):
                    for j in range(4): self.elec_labels[i][j].setText("-/-")
        elif self.cb_wheels.isChecked():
            for i in range(num_robots_to_display):
                if i < len(self.wheels_labels):
                    for j in range(4): self.wheels_labels[i][j].setText("0.0")

def main(): 
    app = QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    sys.exit(app.exec_()) 

if __name__ == "__main__": 
    main()
