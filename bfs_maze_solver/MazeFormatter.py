import cv2
import os
import numpy as np

IMG_PATH = os.path.join(os.path.dirname(__file__), "../example/maze5.jpg")
N = 33
M = 15


class MazeFormatter:
    def __init__(self, img_path, N=33, m=15):
        self.img_path = img_path
        self.img = cv2.imread(img_path, 0)
        self.img = cv2.resize(self.img, (495, 495))
        _, self.img = cv2.threshold(
            self.img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        self.N = N
        self.m = m

    def convert(self):
        maze = ""
        white_cells = 0
        black_cells = 0
        thick_walls = 0
        thin_walls = 0
        for i in range(self.N):
            for j in range(self.N):
                val = int(
                    self.img[
                        i * self.m : (i + 1) * self.m, j * self.m : (j + 1) * self.m
                    ].mean()
                )
                cell = 1 if val > 127 else 0
                maze += "{} ".format(cell)
                if cell == 1:
                    white_cells += 1
                else:
                    black_cells += 1

                larger_area_val = int(
                    self.img[
                        max(0, (i - 1) * self.m) : min(
                            (i + 2) * self.m, self.img.shape[0]
                        ),
                        max(0, (j - 1) * self.m) : min(
                            (j + 2) * self.m, self.img.shape[1]
                        ),
                    ].mean()
                )
                if larger_area_val < 127:
                    thick_walls += 1
                else:
                    thin_walls += 1

            maze += "\n"

        wall_thickness = "thick" if thick_walls > thin_walls else "thin"

        if white_cells > black_cells:
            maze = maze.replace("0", "2")
            maze = maze.replace("1", "0")
            maze = maze.replace("2", "1")

        if wall_thickness == "thick":
            maze = maze.replace("0", "2")
            maze = maze.replace("1", "0")
            maze = maze.replace("2", "1")

        return maze

    def show(self):
        maze = np.array(
            [
                list(map(int, x.strip().split(" ")))
                for x in self.convert().split("\n")
                if x
            ]
        )
        maze_resized = np.repeat(maze, 15, axis=0)
        maze_resized = np.repeat(maze_resized, 15, axis=1)
        maze_resized = maze_resized.astype(np.uint8) * 255  # 0 is black, 255 is white
        maze_resized = 255 - maze_resized
        cv2.imshow("Maze Preview", maze_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rm = MazeFormatter(IMG_PATH, N, M)
    print(rm.convert())
    rm.show()
