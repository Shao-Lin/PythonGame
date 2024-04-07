import sys
import random
from collections import deque

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont

from Game import GameLogic


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Сложение значений кнопок")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.count_label = QLabel("Score: 0", self)
        font = self.count_label.font()
        font.setPointSize(30)
        self.count_label.setFont(font)
        layout.addWidget(self.count_label)
        self.count = 0  # Счет игры
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        self.logic = GameLogic(self.grid_layout, self.count_label)  # Передача grid_layout при создании GameLogic

        for i in range(5):
            for j in range(5):
                button = QPushButton("", self)
                button.setFixedSize(100, 100)
                button.setFont(QFont("Vetka", 15))
                self.grid_layout.addWidget(button, i, j)
                button.clicked.connect(self.on_button_clicked)

        self.logic.randomly_fill_button(self.grid_layout, 3)
        self.logic.fill_colors(self.grid_layout)

    def update_count(self, result):
        self.count += result
        self.count_label.setText("Score: " + str(self.count))

    def on_button_clicked(self):
        if self.logic.checking_the_loss(self.grid_layout):
            button = self.sender()
            if len(self.logic.selected_buttons) < 2:
                self.logic.selected_buttons.append(button)
                button.setStyleSheet("border: 2px solid red;")

                if len(self.logic.selected_buttons) == 2:
                    button_1 = self.logic.selected_buttons[0]
                    button_2 = self.logic.selected_buttons[1]
                    if button_1.text() == "" or button_2.text() == "":
                        if self.logic.selected_buttons[0].text() == "":
                            self.logic.clear_selection(self.logic.selected_buttons)
                            self.logic.fill_colors(self.grid_layout)
                        elif self.logic.has_path_between_buttons(button_1, button_2, self.grid_layout,
                                                                 self.logic.selected_buttons):
                            value1 = int(self.logic.selected_buttons[0].text())
                            result = value1
                            self.logic.selected_buttons[1].setText(str(result))
                            self.logic.selected_buttons[0].setText("")
                            self.logic.clear_selection(self.logic.selected_buttons)
                            self.logic.randomly_fill_button(self.grid_layout, 2)
                            self.logic.fill_colors(self.grid_layout)
                        else:
                            self.logic.clear_selection(self.logic.selected_buttons)
                            self.logic.fill_colors(self.grid_layout)

                    elif self.logic.has_path_between_buttons(button_1, button_2, self.grid_layout,
                                                             self.logic.selected_buttons):
                        value1 = int(button_1.text())
                        value2 = int(button_2.text())
                        if value1 == value2:
                            result = value1 + 1
                            self.update_count(result)
                            self.logic.selected_buttons[1].setText(str(result))
                            self.logic.selected_buttons[0].setText("")
                            self.logic.clear_selection(self.logic.selected_buttons)
                            self.logic.randomly_fill_button(self.grid_layout, 1)
                            self.logic.fill_colors(self.grid_layout)
                            if result == 12:
                                self.show_win_box()
                        else:
                            self.logic.clear_selection(self.logic.selected_buttons)
                            self.logic.fill_colors(self.grid_layout)
                    else:
                        self.logic.fill_colors(self.grid_layout)
            else:
                self.logic.clear_selection(self.logic.selected_buttons)
        else:
            self.show_loser_box()


    def show_loser_box(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Поражение")
        msg_box.setText("Вы лузер хахаха!")
        msg_box.addButton(QMessageBox.Ok)
        msg_box.finished.connect(self.close)
        msg_box.exec_()
    def show_win_box(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Победа")
        msg_box.setText("Вы победили!")
        msg_box.addButton(QMessageBox.Ok)
        msg_box.finished.connect(self.close)
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.setGeometry(100, 100, 600, 600)
    window.show()
    sys.exit(app.exec_())


