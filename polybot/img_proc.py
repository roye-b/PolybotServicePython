from pathlib import Path
from matplotlib.image import imread, imsave
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):
        # TODO remove the `raise` below, and write your implementation
        n = []
        for i in range(len(self.data)):
            n.append([])
            for j in range(0, len(self.data[i])):
                r = len(self.data)
                n[i].append(self.data[r-j-1][i])
        self.data = n





    def salt_n_pepper(self):
        # TODO remove the `raise` below, and write your implementation
        for i in range (len(self.data)):
            for j in range(0, len(self.data[i])):
                x = random.uniform(0, 1)
                if x < 0.2:
                    self.data[i][j] = 255
                if x > 0.8:
                    self.data[i][j] = 0






    def concat(self, other_img, direction='horizontal'):
        # TODO remove the `raise` below, and write your implementation
        if len(self.data) == len(other_img.data):
             for i in range (len(self.data)):
                 self.data[i]=self.data[i]+other_img.data[i]
        else:
            raise RuntimeError("the")


    def segment(self):
        # TODO remove the `raise` below, and write your implementation
        for i in range(len(self.data)):
            for j in range(0, len(self.data[i])):
                if  self.data[i][j] <= 100:
                    self.data[i][j] = 0
                if  self.data[i][j] > 100:
                    self.data[i][j] = 255



if __name__ == '__main__':
    my_img = Img('/home/roye/PolybotServicePython/polybot/test/beatles.jpeg')
    my_img.segment()
    my_img.save_img()

