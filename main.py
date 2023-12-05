from bfs_maze_solver import MazeSolverGUI
from PyQt5.QtWidgets import QApplication
import os

# Constants
IMG_PATH = os.path.join(os.path.dirname(__file__), "example/maze0.jpg")
SLEEP_TIME = 10
GRID_SIZE = (33, 15)
APP_TITLE = "Maze Solver"

if __name__ == "__main__":
    app = QApplication([])
    solver = MazeSolverGUI(IMG_PATH, GRID_SIZE, SLEEP_TIME, APP_TITLE)
    solver.show()
    app.exec_()
