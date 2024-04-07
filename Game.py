
import random
from collections import deque


class GameLogic:
    def __init__(self, grid_layout, count_label):
        self.grid_layout = grid_layout
        self.count_label = count_label
        self.selected_buttons = []


    def randomly_fill_button(self, grid_layout, num_buttons):
        empty_buttons = []
        for i in range(5):
            for j in range(5):
                button = grid_layout.itemAtPosition(i, j).widget()
                if button.text() == "":
                    empty_buttons.append(button)
        if empty_buttons:
            buttons_to_fill = random.sample(empty_buttons, num_buttons)
            for button in buttons_to_fill:
                button.setText(str(random.randint(1, 3)))

    def clear_selection(self, selected_buttons):
        for btn in selected_buttons:
            btn.setStyleSheet("")
        selected_buttons.clear()

    def get_empty_neighbours(self, button, grid_layout):
        pos = grid_layout.getItemPosition(grid_layout.indexOf(button))
        rows, cols = grid_layout.rowCount(), grid_layout.columnCount()
        neighbours = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = pos[0] + dr, pos[1] + dc
                if (0 <= new_row < rows and 0 <= new_col < cols and
                    (dr, dc) != (0, 0) and
                    (dr == 0 or dc == 0)):
                    neighbour_button = grid_layout.itemAtPosition(new_row, new_col).widget()
                    if len(self.selected_buttons) == 2:
                        second_button = self.selected_buttons[1]
                        second_pos = grid_layout.getItemPosition(grid_layout.indexOf(second_button))
                        second_row, second_col = second_pos[0], second_pos[1]
                        if abs(pos[0] - second_row) <= 1 and abs(pos[1] - second_col) <= 1:
                            neighbours.append(second_button)
                    if neighbour_button.text() == "":
                        neighbours.append(neighbour_button)
                    elif not neighbour_button.text().isdigit():
                        neighbours.append(neighbour_button)

        return neighbours
    def checking_the_loss(self,grid_layout):
        rows, cols = grid_layout.rowCount(), grid_layout.columnCount()

        for i in range (grid_layout.rowCount()):
            for j in range(grid_layout.columnCount()):
                current_button = grid_layout.itemAtPosition(i, j).widget()
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        new_row, new_col = i + dr, j + dc
                        if (0 <= new_row < rows and 0 <= new_col < cols and
                                (dr, dc) != (0, 0) and
                                (dr == 0 or dc == 0)):
                            neighbour_button = grid_layout.itemAtPosition(new_row, new_col).widget()
                            if neighbour_button.text() == current_button.text() or neighbour_button.text() == "":
                                return True






    def has_path_between_buttons(self, button1, button2, grid_layout, selected_buttons):
        if button1 == button2:
            return False

        visited = set()
        queue = deque([button1])

        while queue:
            current_button = queue.popleft()

            if current_button == button2:
                return True

            if current_button in visited:
                continue

            visited.add(current_button)

            empty_neighbours = self.get_empty_neighbours(current_button, grid_layout)
            for neighbour in empty_neighbours:
                if neighbour not in visited and not self.is_diagonal(current_button, neighbour,grid_layout):
                    queue.append(neighbour)

        self.clear_selection(selected_buttons)
        return False

    def is_diagonal(self, button1, button2,grid_layout):
        pos1 = grid_layout.getItemPosition(grid_layout.indexOf(button1))
        pos2 = grid_layout.getItemPosition(grid_layout.indexOf(button2))
        row1, col1 = pos1[0], pos1[1]
        row2, col2 = pos2[0], pos2[1]
        return abs(row1 - row2) == 1 and abs(col1 - col2) == 1

    def fill_colors(self, grid_layout):
        for i in range(5):
            for j in range(5):
                button = grid_layout.itemAtPosition(i, j).widget()
                if button.text() == "1":
                    button.setStyleSheet("background-color: #FFFF00")
                if button.text() == "2":
                    button.setStyleSheet("background-color: #FFD700")
                if button.text() == "3":
                    button.setStyleSheet("background-color:#FFA500 ")
                if button.text() == "4":
                    button.setStyleSheet("background-color: #FF8C00")
                if button.text() == "5":
                    button.setStyleSheet("background-color: #FF4500")
                if button.text() == "6":
                    button.setStyleSheet("background-color: #FF0000")
                if button.text() == "7":
                    button.setStyleSheet("background-color: #87CEEB")
                if button.text() == "8":
                    button.setStyleSheet("background-color: #1E90FF")
                if button.text() == "9":
                    button.setStyleSheet("background-color: #7FFF00")
                if button.text() == "10":
                    button.setStyleSheet("background-color: #00FA9A")
                if button.text() == "11":
                    button.setStyleSheet("background-color: #228B22")
                if button.text() == "12":
                    button.setStyleSheet("background-color: #000000")