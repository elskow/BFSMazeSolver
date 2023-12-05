import cv2
import os
import numpy as np

IMG_PATH = os.path.join(os.path.dirname(__file__), "../example/maze2.jpg")
N = 33
M = 15


class MazeFormatter:
    def __init__(self, img_path: str, N: int = 33, m: int = 15):
        self.img_path = img_path
        self.img = self.load_and_format_image(img_path)
        self.N = N
        self.m = m

    def load_and_format_image(self, img_path: str):
        img = cv2.imread(img_path, 0)
        img = cv2.resize(img, (495, 495))
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img

    def convert(self) -> str:
        (
            maze,
            white_cells,
            black_cells,
            thick_walls,
            thin_walls,
        ) = self.calculate_cells_and_walls()
        wall_thickness = "thick" if thick_walls > thin_walls else "thin"
        maze = self.adjust_maze_colors(maze, white_cells, black_cells, wall_thickness)
        return maze

    def calculate_cells_and_walls(self) -> (str, int, int, int, int):
        maze = ""
        white_cells = black_cells = thick_walls = thin_walls = 0
        for i in range(self.N):
            for j in range(self.N):
                val, cell = self.calculate_cell_value(i, j)
                maze += "{} ".format(cell)
                white_cells, black_cells = self.update_cell_counts(
                    cell, white_cells, black_cells
                )
                larger_area_val = self.calculate_larger_area_value(i, j)
                thick_walls, thin_walls = self.update_wall_counts(
                    larger_area_val, thick_walls, thin_walls
                )
            maze += "\n"
        return maze, white_cells, black_cells, thick_walls, thin_walls

    def calculate_cell_value(self, i: int, j: int) -> (int, int):
        val = int(
            self.img[
                i * self.m : (i + 1) * self.m, j * self.m : (j + 1) * self.m
            ].mean()
        )
        cell = 1 if val > 127 else 0
        return val, cell

    def update_cell_counts(
        self, cell: int, white_cells: int, black_cells: int
    ) -> (int, int):
        if cell == 1:
            white_cells += 1
        else:
            black_cells += 1
        return white_cells, black_cells

    def calculate_larger_area_value(self, i: int, j: int) -> int:
        return int(
            self.img[
                max(0, (i - 1) * self.m) : min((i + 2) * self.m, self.img.shape[0]),
                max(0, (j - 1) * self.m) : min((j + 2) * self.m, self.img.shape[1]),
            ].mean()
        )

    def update_wall_counts(
        self, larger_area_val: int, thick_walls: int, thin_walls: int
    ) -> (int, int):
        if larger_area_val < 127:
            thick_walls += 1
        else:
            thin_walls += 1
        return thick_walls, thin_walls

    def adjust_maze_colors(
        self, maze: str, white_cells: int, black_cells: int, wall_thickness: int
    ) -> str:
        if white_cells > black_cells:
            maze = self.swap_colors(maze)
        if wall_thickness == "thick":
            maze = self.swap_colors(maze)
        return maze

    def swap_colors(self, maze: str) -> str:
        return maze.replace("0", "2").replace("1", "0").replace("2", "1")

    def show(self, border: bool = True):
        maze = self.create_maze_array(border)
        maze_resized = self.resize_maze(maze)
        self.display_maze(maze_resized)

    def create_maze_array(self, border: bool) -> np.uint8:
        if border:
            maze = np.array(
                [
                    list(map(int, x.strip().split(" ")))
                    for x in self.convert().split("\n")
                    if x
                ]
            )
            return self.add_border(maze)

        return np.array(
            [
                list(map(int, x.strip().split(" ")))
                for x in self.convert().split("\n")
                if x
            ]
        )

    def resize_maze(self, maze: np.uint8):
        maze_resized = np.repeat(maze, 15, axis=0)
        maze_resized = np.repeat(maze_resized, 15, axis=1)
        maze_resized = maze_resized.astype(np.uint8) * 255  # 0 is black, 255 is white
        return 255 - maze_resized

    def display_maze(self, maze_resized):
        cv2.imshow("Maze Preview", maze_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def add_border(self, maze: np.uint8) -> np.uint8:
        x = 1
        y = self.N - 1
        maze[0] = [1 for i in maze[0]]
        maze[-1] = [1 for i in maze[-1]]
        for i in maze:
            i[0] = 1
            i[-1] = 1

        return maze


if __name__ == "__main__":
    rm = MazeFormatter(IMG_PATH, N, M)
    print(rm.convert())
    rm.show(border=True)
