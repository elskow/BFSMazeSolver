from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import os
import time

from Maze import Maze
from MazeFormatter import MazeFormatter
from MazePoint import Point

IMG_PATH = os.path.join(os.path.dirname(__file__), "../example/maze0.jpg")
SLEEP_TIME = 10
GRID_SIZE = (33, 15)
COLOR_MAP = {
    "path": 255,  # white
    "wall": 0,  # black
    "start": 180,  # grey
    "end": 50,  # dark grey
}
VERBOSE = False


class MazeSolver(QMainWindow):
    """Finds a solution to the maze."""

    def __init__(self, img_path, grid_size, sleep_time):
        super().__init__()
        self.grid_size = grid_size
        self.sleep_time = sleep_time

        self.maze_str = MazeFormatter(img_path, *grid_size).convert()
        self.maze = Maze(self.maze_str)

        self.board, self.start, self.end, self.path, self.clicks = (
            None,
            None,
            None,
            [],
            0,
        )

        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_board)
        self.timer.start(1000 * self.sleep_time)

        self.print_maze()

    def print_maze(self, verbose=False):
        """Prints the maze to the console and updates the board."""
        if verbose:
            print(self.maze.maze)
        self.update_board()

    def update_board(self):
        """Updates the board with the current state of the maze."""
        self.board = self.maze.maze.astype(np.uint8)
        for key, value in COLOR_MAP.items():
            if key == "path":
                self.board[self.board == 0] = value
            elif key == "wall":
                self.board[self.board == 1] = value
            elif key == "start":
                self.board[self.board == 2] = value
            elif key == "end":
                self.board[self.board == 3] = value

        self.board = self.board.repeat(20, axis=0).repeat(20, axis=1)
        qimg = QImage(
            self.board.data,
            self.board.shape[1],
            self.board.shape[0],
            QImage.Format_Indexed8,
        )
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def mousePressEvent(self, event):
        """Sets the start and end points of the maze."""
        if event.button() == Qt.LeftButton:
            if self.clicks == 0:
                self.start = self.handle_click(event.x(), event.y(), QColor(0, 255, 0))
            elif self.clicks == 1:
                self.end = self.handle_click(event.x(), event.y(), QColor(0, 0, 255))
                self.solve()

    def handle_click(self, x, y, color):
        """Handles a click event at the given coordinates with the given color."""
        maze_x, maze_y = y // 20, x // 20
        self.clicks += 1
        qimg = QImage(
            self.board.data,
            self.board.shape[1],
            self.board.shape[0],
            QImage.Format_Indexed8,
        )
        pixmap = QPixmap.fromImage(qimg)
        qp = QPainter(pixmap)
        qp.setPen(QPen(color, 10, Qt.SolidLine))
        qp.drawPoint(maze_y * 20 + 10, maze_x * 20 + 10)
        qp.end()
        self.label.setPixmap(pixmap)
        return maze_x, maze_y

    def solve(self):
        """Solves the maze."""
        self.path.append(Point(*self.start))
        self.maze.set_value(*self.start, 2)
        self.print_maze()

        while True:
            try:
                current_point = self.path[-1]
            except IndexError:
                self.end_solve("No solution found")
                break

            if current_point.pos == self.end:
                self.end_solve("Maze solved successfully")
                self.highlight_path()
                break

            direction = current_point.get_dir(self.maze)
            if direction:
                current_point = Point(*current_point.get_coord(direction), direction)
                self.maze.set_value(*current_point.pos, 2)
                self.print_maze()
                self.path.append(current_point)
            else:
                self.path.pop()
                self.maze.set_value(*current_point.pos, 3)
                self.print_maze()

    def highlight_path(self):
        """Highlights the shortest path in red."""
        for point in self.path:
            self.handle_click(point.pos[1] * 20, point.pos[0] * 20, QColor(255, 0, 0))
        self.update_board()

    def end_solve(self, message):
        """Ends the solving process and displays a message."""
        QMessageBox.information(self, "Maze Solver", message)
        self.close()


def main():
    app = QApplication([])
    solver = MazeSolver(IMG_PATH, GRID_SIZE, SLEEP_TIME)
    solver.show()
    app.exec_()


if __name__ == "__main__":
    main()
