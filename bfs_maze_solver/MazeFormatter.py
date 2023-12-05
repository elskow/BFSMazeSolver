import os
import cv2
import numpy as np

IMG_PATH = os.path.join(os.path.dirname(__file__), "../example/maze0.jpg")
N = 33
M = 15


class MazeFormatter:
    def __init__(self, img_path, n=33, m=15):
        self.img_path = img_path
        self.img = self.load_and_format_image(img_path)
        self.N = n
        self.m = m

    @staticmethod
    def load_and_format_image(img_path):
        img = cv2.imread(img_path, 0)
        img = cv2.resize(img, (495, 495))
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img

    def convert(self):
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

    def calculate_cells_and_walls(self):
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

    def calculate_cell_value(self, i, j):
        val = int(
            self.img[
                i * self.m: (i + 1) * self.m, j * self.m: (j + 1) * self.m
            ].mean()
        )
        cell = 1 if val > 127 else 0
        return val, cell

    @staticmethod
    def update_cell_counts(cell, white_cells, black_cells):
        if cell == 1:
            white_cells += 1
        else:
            black_cells += 1
        return white_cells, black_cells

    def calculate_larger_area_value(self, i, j):
        return int(
            self.img[
                max(0, (i - 1) * self.m): min((i + 2) * self.m, self.img.shape[0]),
                max(0, (j - 1) * self.m): min((j + 2) * self.m, self.img.shape[1]),
            ].mean()
        )

    @staticmethod
    def update_wall_counts(larger_area_val, thick_walls, thin_walls):
        if larger_area_val < 127:
            thick_walls += 1
        else:
            thin_walls += 1
        return thick_walls, thin_walls

    def adjust_maze_colors(self, maze, white_cells, black_cells, wall_thickness):
        if white_cells > black_cells:
            maze = self.swap_colors(maze)
        if wall_thickness == "thick":
            maze = self.swap_colors(maze)
        return maze

    @staticmethod
    def swap_colors(maze):
        return maze.replace("0", "2").replace("1", "0").replace("2", "1")

    def show(self):
        maze = self.create_maze_array()
        maze_resized = self.resize_maze(maze)
        self.display_maze(maze_resized)

    def create_maze_array(self):
        return np.array(
            [
                list(map(int, x.strip().split(" ")))
                for x in self.convert().split("\n")
                if x
            ]
        )

    @staticmethod
    def resize_maze(maze):
        maze_resized = np.repeat(maze, 15, axis=0)
        maze_resized = np.repeat(maze_resized, 15, axis=1)
        maze_resized = maze_resized.astype(np.uint8) * 255  # 0 is black, 255 is white
        return 255 - maze_resized

    @staticmethod
    def display_maze(maze_resized):
        cv2.imshow("Maze Preview", maze_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rm = MazeFormatter(IMG_PATH, N, M)
    print(rm.convert())
    rm.show()
