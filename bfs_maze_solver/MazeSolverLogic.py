from .MazePoint import MazePoint
from collections import deque
import time


class MazeSolverLogic:
    """Finds a solution to the maze. Uses a breadth-first search algorithm."""

    def __init__(self, maze, start, end, update_gui, sleep_time=None):
        self.maze = maze
        self.start = start
        self.end = end
        self.path = deque()
        self.is_solved = False
        self.update_gui = update_gui
        self.the_shortest_path = []
        self.sleep_time = sleep_time

    def solve(self):
        """Solves the maze."""
        self.path.append(MazePoint(*self.start))
        self.maze.set_value(*self.start, 3)

        predecessor = {}

        while self.path:
            current_point = self.path.popleft()

            if current_point.pos == self.end:
                self.is_solved = True
                break

            for direction in range(1, 5):
                next_point = MazePoint(*current_point.get_coord(direction), direction)
                if self.maze.get_val(*next_point.pos) == 0:
                    self.maze.set_value(*next_point.pos, 3)
                    self.path.append(next_point)
                    predecessor[next_point.pos] = current_point
            if self.sleep_time:
                time.sleep(self.sleep_time)
            self.update_gui()

        # Backtrack to find the shortest path
        if self.is_solved:
            current_point = MazePoint(*self.end)
            while current_point.pos != self.start:
                self.maze.set_value(*current_point.pos, 2)
                current_point = predecessor[current_point.pos]
            self.maze.set_value(*self.start, 2)
