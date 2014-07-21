__author__ = 'daniel'

import numpy



class BoxTest:
    def __init__(self, data_x, data_y, i, j):
        self.data_x = data_x
        self.data_y = data_y
        self.i = i
        self.j = j


    def perform(self):
        # compute quantiles. Not using ranges since they are only overhead.
        self.x_q_i = self.data_x.quantile(self.i)
        self.x_q_j = self.data_x.quantile(self.j)
        self.y_q_i = self.data_y.quantile(self.i)
        self.y_q_j = self.data_y.quantile(self.j)
        print(self.x_q_i)
        print(self.x_q_j)
        print(self.y_q_i)
        print(self.y_q_j)

        overlap = self.overlap(self.x_q_i, self.x_q_j, self.y_q_i, self.y_q_j)

        return not overlap and self.x_q_j < self.y_q_i

    def x_box(self):
        return [self.x_q_i, self.x_q_j]

    def y_box(self):
        return [self.y_q_i, self.y_q_j]

    def overlap (self, a_lower, a_upper, b_lower, b_upper):
        return a_upper > b_lower and a_lower < b_upper














