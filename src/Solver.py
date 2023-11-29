import numpy as np
import os
import time
import cv2

from MazeFormatter import MazeFormatter
from MazePoint import Point
from Maze import Maze


IMG_PATH = os.path.join(os.path.dirname(__file__), "../example/maze0.jpg")
SLEEP_TIME = 0.01
N = 33
M = 15
THRESHOLD = 100


class Solution:
    """Finds a solution to the maze."""

    def __init__(self, img_path, n=33, m=15, threshold=100, sleep_time=None):
        self.board = None
        self.start = None
        self.end = None
        self.path = []
        self.clicks = 0
        self.n = n
        self.m = m
        self.threshold = threshold
        self.sleep_time = sleep_time
        maze_str = MazeFormatter(img_path, n, m, threshold).convert()
        self.maze = Maze(maze_str)

    def set_start_end(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            maze_x, maze_y = y // 20, x // 20
            self.clicks += 1
            if self.clicks == 1:
                self.start = (maze_x, maze_y)
            elif self.clicks == 2:
                self.end = (maze_x, maze_y)
                self.solve()

    def print_maze(self):
        os.system("cls")
        print(self.maze.maze)

        self.board = self.maze.maze.astype(np.uint8)
        self.board[self.board == 0] = 255
        self.board[self.board == 1] = 0
        self.board[self.board == 2] = 180
        self.board[self.board == 3] = 50

        self.n = 20
        self.board = self.board.repeat(self.n, axis=0).repeat(self.n, axis=1)
        cv2.imshow("maze", self.board)
        cv2.waitKey(1)

    def solve(self):
        self.path.append(Point(*self.start))
        self.maze.set_value(*self.start, 2)
        self.print_maze()
        while True:
            time.sleep(SLEEP_TIME)
            try:
                current_point = self.path[-1]
            except IndexError:
                print("No solution found")
                break

            if current_point.pos == self.end:
                print("done")
                break
            d = current_point.get_dir(self.maze)
            if d:
                current_point = Point(*current_point.get_coord(d), d)
                self.maze.set_value(*current_point.pos, 2)
                self.print_maze()
                self.path.append(current_point)
            else:
                current_point = self.path.pop()
                self.maze.set_value(*current_point.pos, 3)
                self.print_maze()


if __name__ == "__main__":
    solution = Solution(IMG_PATH, N, M, THRESHOLD, SLEEP_TIME)
    solution.print_maze()
    cv2.setMouseCallback("maze", solution.set_start_end)

    message = np.zeros((200, 600), dtype="uint8")
    cv2.putText(
        message,
        "Please click start and end points",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
    )
    cv2.imshow("Message", message)
    cv2.waitKey(0)

    cv2.waitKey(0)
