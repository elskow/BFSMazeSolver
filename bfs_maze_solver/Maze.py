import numpy as np


class Maze:
    """Represents the maze."""

    def __init__(self, maze_str, border: bool = True):
        self.maze = np.array(
            [list(map(int, x.strip().split(" "))) for x in maze_str.split("\n") if x]
        )
        if border:
            maze = np.array(
                [
                    list(map(int, x.strip().split(" ")))
                    for x in maze_str.split("\n")
                    if x
                ]
            )
            self.maze = self.add_border(maze)

        self.height, self.width = self.shape = self.maze.shape

    def get_val(self, x, y):
        return self.maze[x, y]

    def set_value(self, x, y, val):
        self.maze[x, y] = val

    def add_border(self, maze):
        x = 1
        y = len(maze)
        maze[0] = [1 for i in maze[0]]
        maze[-1] = [1 for i in maze[-1]]
        for i in maze:
            i[0] = 1
            i[-1] = 1

        return maze
