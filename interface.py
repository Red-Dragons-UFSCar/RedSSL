import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QCheckBox, QGroupBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea, QFrame, QButtonGroup
)
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Red Dragons - Interface")
        self.setMinimumSize(1000, 600)

        # Área central principal (widget) e layout horizontal
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # ---------- Barra lateral Esquerda ----------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Nome do time
        self.team_label = QLabel("<b>Red Dragons</b>")
        left_layout.addWidget(self.team_label)

        # Checkboxes de seleção de exibição (mutuamente exclusivos)
        self.cb_opponent = QCheckBox("Adversário")
        self.cb_red_dragons = QCheckBox("Red Dragons")
        group_left = QButtonGroup(self)
        group_left.setExclusive(True)
        group_left.addButton(self.cb_opponent)
        group_left.addButton(self.cb_red_dragons)
        left_layout.addWidget(self.cb_opponent)
        left_layout.addWidget(self.cb_red_dragons)

        # Grupo dos dados de posição e rotação (em formato de tabela)
        self.pos_group = QGroupBox("Posição e Rotação")
        pos_layout = QGridLayout()
        pos_layout.addWidget(QLabel("Robô"), 0, 0)
        pos_layout.addWidget(QLabel("Pos.X"), 0, 1)
        pos_layout.addWidget(QLabel("Pos.Y"), 0, 2)
        pos_layout.addWidget(QLabel("θ"), 0, 3)

        self.pos_labels = []
        for i in range(3):
            pos_layout.addWidget(QLabel(f"Robô {i}"), i + 1, 0)
            row_list = []
            for j in range(3):  # Colunas: Pos.X, Pos.Y, θ
                lbl = QLabel("?")
                row_list.append(lbl)
                pos_layout.addWidget(lbl, i + 1, j + 1)
            self.pos_labels.append(row_list)
        self.pos_group.setLayout(pos_layout)
        left_layout.addWidget(self.pos_group)

        left_layout.addStretch(1)

        # ---------- Área Central (campo) ----------
        center_area = QScrollArea()
        center_frame = QFrame()
        center_layout = QVBoxLayout(center_frame)

        # Exemplo de imagem do campo
        field_label = QLabel()
        pixmap = QPixmap(800, 600)
        pixmap.fill()
        field_label.setPixmap(pixmap)
        center_layout.addWidget(field_label)
        center_area.setWidget(center_frame)
        center_area.setWidgetResizable(True)

        # ---------- Barra lateral Direita ----------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Checkboxes para exibir dados (mutuamente exclusivos)
        self.cb_elec = QCheckBox("Eletrônica")
        self.cb_wheels = QCheckBox("Velo. Rodas")
        group_right = QButtonGroup(self)
        group_right.setExclusive(True)
        group_right.addButton(self.cb_elec)
        group_right.addButton(self.cb_wheels)
        right_layout.addWidget(self.cb_elec)
        right_layout.addWidget(self.cb_wheels)

        # Grupo da eletrônica (agora com dados para cada robô)
        self.elec_group = QGroupBox("Eletrônica")
        elec_layout = QGridLayout()
        elec_layout.addWidget(QLabel("Robô"), 0, 0)
        elec_layout.addWidget(QLabel("Tensão (V)"), 0, 1)
        elec_layout.addWidget(QLabel("Corrente (A)"), 0, 2)
        elec_layout.addWidget(QLabel("Loss (%)"), 0, 3)
        elec_layout.addWidget(QLabel("Ping (ms)"), 0, 4)

        self.elec_labels = []
        for i in range(3):
            # Primeira coluna: nome do robô
            elec_layout.addWidget(QLabel(f"Robô {i}"), i + 1, 0)
            # Demais colunas: tensao, corrente, loss, ping
            row_list = []
            for j in range(4):
                lbl = QLabel("?")
                row_list.append(lbl)
                elec_layout.addWidget(lbl, i + 1, j + 1)
            self.elec_labels.append(row_list)
        self.elec_group.setLayout(elec_layout)

        # Grupo das velocidades das rodas (em formato de tabela)
        self.wheels_group = QGroupBox("Velocidades")
        wheels_layout = QGridLayout()
        wheels_layout.addWidget(QLabel("Robô"), 0, 0)
        wheel_names = ["FR", "FL", "BR", "BL"]
        for col, w_name in enumerate(wheel_names, start=1):
            wheels_layout.addWidget(QLabel(w_name), 0, col)

        self.wheels_labels = []
        for i in range(3):
            wheels_layout.addWidget(QLabel(f"Robô {i}"), i + 1, 0)
            row_list = []
            for j in range(4):  # Colunas: FR, FL, BR, BL
                lbl = QLabel("?")
                row_list.append(lbl)
                wheels_layout.addWidget(lbl, i + 1, j + 1)
            self.wheels_labels.append(row_list)
        self.wheels_group.setLayout(wheels_layout)

        # Exibe "Velo. Rodas" por padrão
        right_layout.addWidget(self.elec_group)
        right_layout.addWidget(self.wheels_group)
        self.elec_group.hide()   # Oculto por padrão
        self.cb_wheels.setChecked(True)

        right_layout.addStretch(1)

        # ---------- Monta o layout geral ----------
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(center_area, 3)
        main_layout.addWidget(right_widget, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Conexões dos sinais
        self.cb_opponent.toggled.connect(self.on_left_checkbox_toggled)
        self.cb_red_dragons.toggled.connect(self.on_left_checkbox_toggled)
        self.cb_elec.toggled.connect(self.on_right_checkbox_toggled)
        self.cb_wheels.toggled.connect(self.on_right_checkbox_toggled)

    def on_left_checkbox_toggled(self):
        """
        Muda o título do pos_group e o texto dos robôs para "Adversários" ou "Red Dragons"
        dependendo de qual checkbox está selecionada.
        """
        if self.cb_opponent.isChecked():
            self.pos_group.setTitle("Adversários")
            self.team_label.setText("<b>Adversários</b>")
            for i, row_list in enumerate(self.pos_labels):
                for j, label in enumerate(row_list):
                    label.setText("?")
        elif self.cb_red_dragons.isChecked():
            self.pos_group.setTitle("Red Dragons")
            self.team_label.setText("<b>Red Dragons</b>")
            for i, row_list in enumerate(self.pos_labels):
                for j, label in enumerate(row_list):
                    label.setText("?")

    def on_right_checkbox_toggled(self):
        """
        Exibe informações de 'Eletrônica' ou 'Velo. Rodas' conforme a seleção.
        """
        if self.cb_elec.isChecked():
            self.elec_group.show()
            self.wheels_group.hide()
        elif self.cb_wheels.isChecked():
            self.elec_group.hide()
            self.wheels_group.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()