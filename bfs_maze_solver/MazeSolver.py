import cv2
import numpy as np
import os
import time
from tkinter import messagebox

from Maze import Maze
from MazeFormatter import MazeFormatter
from MazePoint import Point

IMG_PATH = os.path.join(os.path.dirname(__file__), "../example/maze0.jpg")
SLEEP_TIME = 0.01
GRID_SIZE = (33, 15)
COLOR_MAP = {
    "path": 255,  # white
    "wall": 0,  # black
    "start": 180,  # grey
    "end": 50,  # dark grey
}
VERBOSE = False


class MazeSolver:
    """Finds a solution to the maze."""

    def __init__(self, img_path, grid_size, sleep_time):
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

        self.board = cv2.cvtColor(self.board, cv2.COLOR_GRAY2BGR)
        self.board[self.maze.maze == 2] = [0, 0, 255]

        self.board = self.board.repeat(20, axis=0).repeat(20, axis=1)
        cv2.imshow("Maze", self.board)
        cv2.waitKey(1)

    def draw_circle(self, center, color):
        """Draws a circle at the given center with the given color."""
        cv2.circle(self.board, center, 10, color, -1)
        cv2.imshow("Maze", self.board)
        cv2.waitKey(1)

    def handle_click(self, x, y, color):
        """Handles a click event at the given coordinates with the given color."""
        maze_x, maze_y = y // 20, x // 20
        self.clicks += 1
        center_x, center_y = maze_y * 20 + 10, maze_x * 20 + 10
        self.draw_circle((center_x, center_y), color)
        return maze_x, maze_y

    def set_start_end(self, event, x, y, flags, param):
        """Sets the start and end points of the maze."""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.clicks == 0:
                self.start = self.handle_click(x, y, (0, 255, 0))
            elif self.clicks == 1:
                self.end = self.handle_click(x, y, (0, 0, 255))
                self.solve()

    def solve(self):
        """Solves the maze."""
        self.path.append(Point(*self.start))
        self.maze.set_value(*self.start, 2)
        self.print_maze()

        while True:
            time.sleep(self.sleep_time)
            try:
                current_point = self.path[-1]
            except IndexError:
                self.end_solve("No solution found")
                break

            if current_point.pos == self.end:
                self.end_solve("Maze solved successfully")
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

    def end_solve(self, message):
        """Ends the solving process and displays a message."""
        messagebox.showinfo("Maze Solver", message)
        cv2.destroyAllWindows()


def main():
    solver = MazeSolver(IMG_PATH, GRID_SIZE, SLEEP_TIME)
    solver.print_maze(VERBOSE)
    cv2.setMouseCallback("Maze", solver.set_start_end)
    messagebox.showinfo("Maze Solver", "Please click start and end points")
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
