from collections import deque
from .MazePoint import MazePoint
import time


class MazeSolverLogic:
    """Finds a solution to the maze using a breadth-first search algorithm."""

    def __init__(self, maze, start, end, update_gui, sleep_time=None):
        self.maze = maze
        self.start = start
        self.end = end
        self.path = deque()  # Use deque for O(1) append and popleft
        self.is_solved = False
        self.update_gui = update_gui
        self.sleep_time = sleep_time
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        self.visited = set()  # Use set for O(1) lookup

    def solve(self):
        """Solves the maze."""
        start_point = MazePoint(*self.start)
        self.path.append(start_point)
        self.visited.add(start_point.pos)  # Mark as visited
        predecessor = {}

        while self.path:
            current_point = self.path.popleft()
            self.maze.set_value(*current_point.pos, 3)  # Mark as visited

            if current_point.pos == self.end:
                self.is_solved = True
                break

            for i in range(4):
                next_pos = (
                    current_point.pos[0] + self.directions[i][0],
                    current_point.pos[1] + self.directions[i][1],
                )
                next_point = MazePoint(*next_pos, i + 1)
                if (
                    self.maze.get_val(*next_point.pos) == 0
                    and next_point.pos not in self.visited
                ):
                    self.visited.add(next_point.pos)  # Mark as visited
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
