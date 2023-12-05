from MazePoint import Point


class MazeSolverLogic:
    """Finds a solution to the maze."""

    def __init__(self, maze, start, end, update_gui):
        self.maze = maze
        self.start = start
        self.end = end
        self.path = []
        self.is_solved = False
        self.update_gui = update_gui

    def solve(self):
        """Solves the maze."""
        self.path.append(Point(*self.start))
        self.maze.set_value(*self.start, 2)

        while True:
            try:
                current_point = self.path[-1]
            except IndexError:
                break

            if current_point.pos == self.end:
                self.is_solved = True
                break

            try:
                direction = current_point.get_dir(self.maze)
            except IndexError:
                break

            if direction:
                current_point = Point(*current_point.get_coord(direction), direction)
                self.maze.set_value(*current_point.pos, 2)
                self.path.append(current_point)
            else:
                self.path.pop()
                self.maze.set_value(*current_point.pos, 3)

            self.update_gui()