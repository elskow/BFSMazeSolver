import cv2
import os
import numpy as np

img_path = os.path.join(os.path.dirname(__file__), "../example/maze0.jpg")
output_path = os.path.join(os.path.dirname(__file__), "../example/maze.txt")


class MazeFormatter:
    def __init__(self, img_path, output_path, N=33, m=15, threshold=100):
        self.img_path = img_path
        self.output_path = output_path
        self.img = cv2.imread(img_path, 0)
        self.img = cv2.resize(self.img, (495, 495))
        self.N = N
        self.m = m
        self.threshold = threshold

    def convert(self):
        foo = open(self.output_path, "w")
        for i in range(self.N):
            for j in range(self.N):
                val = int(
                    self.img[
                        i * self.m : (i + 1) * self.m, j * self.m : (j + 1) * self.m
                    ].mean()
                )
                foo.write("{} ".format(1 if val > self.threshold else 0))
            foo.write("\n")
        foo.close()

    def show(self):
        maze = np.loadtxt(self.output_path)
        maze = np.repeat(maze, 15, axis=0)
        maze = np.repeat(maze, 15, axis=1)
        maze = maze.astype(np.uint8) * 255
        maze = 255 - maze
        cv2.imshow("Maze Preview", maze)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rm = MazeFormatter(img_path, output_path)
    rm.convert()
    rm.show()
