import cv2
import os
import numpy as np

img_path = os.path.join(os.path.dirname(__file__), "../example/maze0.jpg")
output_path = os.path.join(os.path.dirname(__file__), "../example/maze.txt")


class MazeFormatter:
    def __init__(self, img_path, N=33, m=15, threshold=90):
        self.img_path = img_path
        self.img = cv2.imread(img_path, 0)
        self.img = cv2.resize(self.img, (495, 495))
        self.N = N
        self.m = m
        self.threshold = threshold

    def convert(self):
        maze = ''
        for i in range(self.N):
            for j in range(self.N):
                val = int(
                    self.img[
                        i * self.m : (i + 1) * self.m, j * self.m : (j + 1) * self.m
                    ].mean()
                )
                maze += "{} ".format(1 if val > self.threshold else 0)
            maze += "\n"

        return maze

    def show(self):
        maze = np.array([list(map(int, x.strip().split(" "))) for x in self.convert().split("\n") if x])
        maze_resized = np.repeat(maze, 15, axis=0)
        maze_resized = np.repeat(maze_resized, 15, axis=1)
        maze_resized = maze_resized.astype(np.uint8) * 255  # 0 is black, 255 is white
        maze_resized = 255 - maze_resized
        cv2.imshow("Maze Preview", maze_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rm = MazeFormatter(img_path)
    print(rm.convert())
    rm.show()
