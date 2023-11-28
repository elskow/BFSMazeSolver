import numpy as np
import os
import time
import cv2


MAZE_PATH = os.path.join(os.path.dirname(__file__), "../example/maze.txt")
DIRECTIONS = [1, 2, 3, 4]
# START_POINT = (1, 1)
# END_POINT = (15, 15)
SLEEP_TIME = 0.01


class Point:
    """Represents a point in the maze."""

    def __init__(self, x, y, d=None):
        self.x = x
        self.y = y
        self.directions = DIRECTIONS.copy()
        if d:
            self.directions.remove((d + 1) % 4 + 1)
        self.d = self.directions[0]

    @property
    def pos(self):
        return self.x, self.y

    def get_coord(self, d):
        x = self.x + (3 - d) if d % 2 == 0 else self.x
        y = self.y + (2 - d) if d % 2 else self.y
        return x, y

    def get_dir(self, maze):
        while self.directions:
            d = self.directions.pop(0)
            x, y = self.get_coord(d)
            if maze.get_val(x, y):
                continue
            else:
                break
        else:
            d = 0
        self.d = d
        return d

    def __repr__(self):
        return "x={},y={},dirs={}".format(self.x, self.y, self.directions)


class Maze:
    """Represents the maze."""

    def __init__(self, maze_str):
        maze_list = [[int(i) for i in x.strip().split(" ")] for x in maze_str]
        self.maze = np.array(maze_list)
        self.height, self.width = self.shape = self.maze.shape

    def get_val(self, x, y):
        return self.maze[x, y]

    def set_value(self, x, y, val):
        self.maze[x, y] = val


class Solution:
    """Finds a solution to the maze."""

    def __init__(self, maze_str, start=None, end=None):
        self.maze = Maze(maze_str)
        self.start = start
        self.end = end or (self.maze.height - 2, self.maze.width - 2)
        self.path = []
        self.clicks = 0

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

        N = 20
        self.board = self.maze.maze.astype(np.uint8)
        self.board[self.board == 0] = 255
        self.board[self.board == 1] = 0
        self.board[self.board == 2] = 180
        self.board[self.board == 3] = 50

        self.board = self.board.repeat(N, 0).repeat(N, 1)
        cv2.imshow("maze", self.board)
        cv2.waitKey(1)

    def solve(self):
        self.path.append(Point(*self.start))
        self.maze.set_value(*self.start, 2)
        self.print_maze()
        while True:
            time.sleep(SLEEP_TIME)
            current_point = self.path[-1]
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
    with open(MAZE_PATH, "r") as file:
        maze = file.readlines()
    solution = Solution(maze)
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
