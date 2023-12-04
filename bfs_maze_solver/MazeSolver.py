from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QMessageBox,
    QMenuBar,
    QMenu,
    QAction,
    QVBoxLayout,
    QStatusBar,
    QFileDialog,
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import os

from Maze import Maze
from MazeFormatter import MazeFormatter
from MazePoint import Point


# Constants
IMG_PATH = os.path.join(os.path.dirname(__file__), "../example/maze0.jpg")
SLEEP_TIME = 10
GRID_SIZE = (33, 15)
COLOR_MAP = {
    "path": (255, 255, 255),  # white
    "wall": (0, 0, 0),  # black
    "start": (255, 0, 0),  # red
    "end": (50, 50, 50),  # dark grey
}
APP_TITLE = "Maze Solver"


class MazeSolver(QMainWindow):
    """Finds a solution to the maze."""

    def __init__(self, img_path, grid_size, sleep_time, title="Maze Solver"):
        super().__init__()
        self.setWindowTitle(title)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIconText("Maze Solver")
        self.setStyleSheet(
            "QMainWindow {background-color: #2b2b2b; border: 1px solid black;}"
            "QMenuBar {background-color: #2b2b2b; color: white;}"
            "QMenuBar::item {background-color: #2b2b2b; color: white;}"
            "QMenuBar::item::selected {background-color: #3b3b3b; color: white;}"
            "QMenu {background-color: #2b2b2b; color: white;}"
            "QMenu::item::selected {background-color: #3b3b3b; color: white;}"
            "QStatusBar {background-color: #2b2b2b; color: white;}"
            "QToolTip {background-color: #3b3b3b; color: white; border: 1px solid white;}"
        )

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        font = QFont("Inter", 10)
        self.setFont(font)

        # Create a menu bar
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)

        # Create a File menu
        self.fileMenu = QMenu("File", self)
        self.menuBar.addMenu(self.fileMenu)

        # Add actions to the File menu
        self.openImageAction = QAction("Open Image", self)
        self.fileMenu.addAction(self.openImageAction)
        self.openImageAction.triggered.connect(self.open_image)

        self.exitAction = QAction("Exit", self)
        self.fileMenu.addAction(self.exitAction)
        self.exitAction.triggered.connect(self.close)

        # Create an Actions menu
        self.actionsMenu = QMenu("Actions", self)
        self.menuBar.addMenu(self.actionsMenu)

        # Add actions to the Actions menu
        self.resetAction = QAction("Reset", self)
        self.actionsMenu.addAction(self.resetAction)
        self.resetAction.triggered.connect(self.reset_maze)

        # Add a Help menu
        self.helpMenu = QMenu("Help", self)
        self.menuBar.addMenu(self.helpMenu)
        self.aboutAction = QAction("About", self)
        self.helpMenu.addAction(self.aboutAction)
        self.aboutAction.triggered.connect(self.about)

        # Add tooltips to the menu items
        self.openImageAction.setToolTip("Open an image file of a maze")
        self.exitAction.setToolTip("Exit the application")
        self.resetAction.setToolTip("Reset the maze to its original state")
        self.aboutAction.setToolTip("Show information about the application")

        # Create a status bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

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
        label_size = self.label.size()
        label_pos = self.label.pos()
        cell_size_x = label_size.width() // self.maze.maze.shape[1]
        cell_size_y = label_size.height() // self.maze.maze.shape[0]
        maze_x, maze_y = (y - label_pos.y()) // cell_size_y, (
            x - label_pos.x()
        ) // cell_size_x
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
        qp.drawPoint(
            maze_y * cell_size_x + cell_size_x // 2,
            maze_x * cell_size_y + cell_size_y // 2,
        )
        qp.end()
        self.label.setPixmap(pixmap)
        return maze_x, maze_y

    def reset_maze(self):
        """Resets the maze to its original state."""
        self.maze_str = MazeFormatter(IMG_PATH, *GRID_SIZE).convert()
        self.maze = Maze(self.maze_str)
        self.board, self.start, self.end, self.path, self.clicks = (
            None,
            None,
            None,
            [],
            0,
        )
        self.colors = np.full(
            (*self.maze.maze.shape, 3), COLOR_MAP["path"], dtype=np.uint8
        )
        self.print_maze()

    def open_image(self):
        """Opens an image file."""
        img_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.xpm *.jpg)"
        )
        if img_path:
            self.maze_str = MazeFormatter(img_path, *self.grid_size).convert()
            self.maze = Maze(self.maze_str)
            self.board, self.start, self.end, self.path, self.clicks = (
                None,
                None,
                None,
                [],
                0,
            )
            self.colors = np.full(
                (*self.maze.maze.shape, 3), COLOR_MAP["path"], dtype=np.uint8
            )
            self.print_maze()
            QApplication.processEvents()

    def about(self):
        """Shows information about the application."""
        QMessageBox.about(
            self,
            "About Maze Solver",
            "Maze Solver is an application that finds a solution to a maze.\n\n"
            "To use the application, open an image file of a maze and click on the start "
            "and end points of the maze. The application will then find a solution to the "
            "maze and highlight the shortest path in red.\n\n"
            "The application was created by your friendly neighborhood programmer.",
        )

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

            try:
                direction = current_point.get_dir(self.maze)
            except IndexError:
                self.end_solve("Invalid maze configuration")
                break

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
        self.statusBar.showMessage(message)
        QApplication.processEvents()
        QApplication.beep()


def main():
    app = QApplication([])
    solver = MazeSolver(IMG_PATH, GRID_SIZE, SLEEP_TIME, APP_TITLE)
    solver.show()
    app.exec_()


if __name__ == "__main__":
    main()
