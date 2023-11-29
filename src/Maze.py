import numpy as np


class Maze:
    """Represents the maze."""

    def __init__(self, maze_str):
        self.maze = np.array(
            [list(map(int, x.strip().split(" "))) for x in maze_str.split("\n") if x]
        )
        self.height, self.width = self.shape = self.maze.shape

    def get_val(self, x, y):
        return self.maze[x, y]

    def set_value(self, x, y, val):
        self.maze[x, y] = val
