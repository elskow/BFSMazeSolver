class MazePoint:
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
