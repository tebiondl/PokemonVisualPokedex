import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tres en Raya')
        self.setGeometry(100, 100, 300, 350)

        # Layout principal
        layout = QVBoxLayout()

        # Label para el turno del jugador
        self.turn_label = QLabel('Turno del jugador: X', self)
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.turn_label)

        # Grid layout para los botones
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)
        
        # Crear botones y añadirlos al grid
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton('', self)
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda _, x=i, y=j: self.button_clicked(x, y))
                self.grid_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        self.setLayout(layout)

        # Matriz para almacenar los movimientos
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 1  # 1 para X, 2 para O
        self.winner = 1
        
    def button_clicked(self, x, y):
        if self.board[x][y] == 0:
            if self.current_player == 1:
                self.buttons[x][y].setText('X')
                self.board[x][y] = 1
                self.turn_label.setText('Turno del jugador: O')
                self.check_victory()
                self.current_player = 2
            else:
                self.buttons[x][y].setText('O')
                self.board[x][y] = 2
                self.turn_label.setText('Turno del jugador: X')
                self.check_victory()
                self.current_player = 1
                
    def check_victory(self):
        # Check if any player has won, and in case of draw, restart
        # check colums, rows or diagonals for wins
        for i in range(len(self.board)):
            # Check row
            if self.board[i][0] == 1 and self.board[i][1] == 1 and self.board[i][2] == 1:
                # Player 1 wins
                self.winner = 1
                self.show_dialog()
            elif self.board[i][0] == 2 and self.board[i][1] == 2 and self.board[i][2] == 2:
                # Player 1 wins
                self.winner = 2
                self.show_dialog()
            
        for j in range(len(self.board[0])):
            if self.board[0][j] == 1 and self.board[1][j] == 1 and self.board[2][j] == 1:
                # Player 1 wins
                self.winner = 1
                self.show_dialog()
            elif self.board[0][j] == 2 and self.board[1][j] == 2 and self.board[2][j] == 2:
                # Player 1 wins
                self.winner = 2
                self.show_dialog()
                
        # If there are no spaces left, it is a draw
        space_left = False
        for i in self.board:
            for j in i:
                if j == 0:
                    space_left = True
                    break
        
        if not space_left:
            #Draw
            self.winner = 0
            self.show_dialog()
        
        # Check diagonals (there are only 2, so just check those specific squares)
        
        if (self.board[0][0] == 1 and self.board[1][1] == 1 and self.board[2][2] == 1) or (self.board[0][2] == 1 and self.board[1][1] == 1 and self.board[2][0] == 1):
            # Player 1 wins
            self.winner = 1
            self.show_dialog()
        elif (self.board[0][0] == 2 and self.board[1][1] == 2 and self.board[2][2] == 2) or (self.board[0][2] == 2 and self.board[1][1] == 2 and self.board[2][0] == 2):
            # Player 1 wins
            self.winner = 2
            self.show_dialog()
                
    def show_dialog(self):
        msg_box = QMessageBox()
        msg_box.setText(f"El jugador { self.winner } ha ganado.")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.buttonClicked.connect(self.reset_board)
        msg_box.exec()
        
    def reset_board(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        for i in self.buttons:
            for j in i:
                j.setText('')
        
                


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicTacToe()
    ex.show()
    sys.exit(app.exec())