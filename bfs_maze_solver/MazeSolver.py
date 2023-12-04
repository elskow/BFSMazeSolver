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
    "path": (255, 255, 255),  # white
    "wall": (0, 0, 0),  # black
    "start": (255, 0, 0),  # red
    "end": (50, 50, 50),  # dark grey
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
        self.colors = np.full(
            (*self.maze.maze.shape, 3), COLOR_MAP["path"], dtype=np.uint8
        )
        self.print_maze()

    def print_maze(self, verbose=False):
        """Prints the maze to the console and updates the board."""
        if verbose:
            print(self.maze.maze)
        self.update_board()

    def update_board(self):
        """Updates the board with the current state of the maze."""
        colors = np.full((*self.maze.maze.shape, 3), COLOR_MAP["path"], dtype=np.uint8)
        for key, value in COLOR_MAP.items():
            if key == "path":
                colors[self.maze.maze == 0] = value
            elif key == "wall":
                colors[self.maze.maze == 1] = value
            elif key == "start":
                colors[self.maze.maze == 2] = value
            elif key == "end":
                colors[self.maze.maze == 3] = value

        self.colors = np.repeat(colors, 20, axis=0)
        self.colors = np.repeat(self.colors, 20, axis=1)
        qimg = QImage(
            self.colors.data,
            self.colors.shape[1],
            self.colors.shape[0],
            QImage.Format_RGB888,
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
            self.colors.data,
            self.colors.shape[1],
            self.colors.shape[0],
            QImage.Format_RGB888,
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
        self.colors[self.start] = COLOR_MAP["start"]
        self.update_board()  # Update the board after setting the start point
        QApplication.processEvents()

        while True:
            try:
                current_point = self.path[-1]
            except IndexError:
                self.end_solve("No solution found")
                break

            if current_point.pos == self.end:
                self.highlight_path()  # Highlight the path after the maze is solved
                self.end_solve("Maze solved successfully")
                break

            direction = current_point.get_dir(self.maze)
            if direction:
                current_point = Point(*current_point.get_coord(direction), direction)
                self.maze.set_value(*current_point.pos, 2)
                self.print_maze()
                self.update_board()  # Update the board after each step
                QApplication.processEvents()
                self.path.append(current_point)
            else:
                self.path.pop()
                self.maze.set_value(*current_point.pos, 3)
                self.print_maze()
                self.update_board()  # Update the board after backtracking
                QApplication.processEvents()

    def highlight_path(self):
        """Highlights the shortest path in red."""
        for point in self.path:
            self.handle_click(point.pos[1] * 20, point.pos[0] * 20, QColor(255, 0, 0))
        self.update_board()
        QApplication.processEvents()

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
