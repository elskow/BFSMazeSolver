# from MazePoint import MazePoint as Point
from collections import deque

class Point:
    """Represents a point in the maze."""

    def __init__(self, x, y, d=None, directions=None):
        if directions is None:
            directions = [1, 2, 3, 4]
        self.x = x
        self.y = y
        self.directions = directions.copy()
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


class MazeSolverLogic:
    """Finds a solution to the maze. Uses a breadth-first search algorithm."""

    def __init__(self, maze, start, end, update_gui):
        self.maze = maze
        self.start = start
        self.end = end
        self.path = deque()
        self.is_solved = False
        self.update_gui = update_gui

    def solve(self):
        """Solves the maze."""
        self.path.append(Point(*self.start))
        self.maze.set_value(*self.start, 2)

        while self.path:
            current_point = self.path.popleft()

            if current_point.pos == self.end:
                self.is_solved = True
                break

            for direction in range(1, 5):
                next_point = Point(*current_point.get_coord(direction), direction)
                if self.maze.get_val(*next_point.pos) == 0:
                    self.maze.set_value(*next_point.pos, 2)
                    self.path.append(next_point)

            self.update_gui()