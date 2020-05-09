import matplotlib.pyplot as plt
import random
from copy import deepcopy
import time
import matplotlib.animation as animation

# RGB
EMPTY = (0, 0, 0)
TREE = (0, 255, 0)
FIRE = (200, 0, 0)


class ForestFireModel:

    def __init__(self):

        self.p = 0.010  # An empty space fills with a tree with probability p
        self.f = 0.0005  # A tree ignites with probability f even if no neighbor is burning

        self.size = 100
        self.board = []
        self.around = [  # na vypocet susedov danej bunky
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1], [0, 1],
            [1, -1], [1, 0], [1, 1]]

    def init(self):
        for y in range(self.size):
            row = []
            for x in range(self.size):
                # 3:1 pomer stromov k prazdnym bunkam na zaciatku
                if random.uniform(0, 1) < 0.25:
                    row.append(EMPTY)
                else:
                    row.append(TREE)
            self.board.append(row)

    # ziska vsetky susedne bunky
    def get_neighbors(self, cords):
        ret = []
        for neighbor in self.around:
            neigh = [x + y for x, y in zip(cords, neighbor)]
            y, x = neigh
            if 0 <= y < self.size and 0 <= x < self.size:
                ret.append(self.board[y][x])
        return ret

    # zisti ci nejaky sused hori
    def is_neighbor_on_fire(self, cells):
        for cell in cells:
            if cell == FIRE:
                return True
        return False

    def iterate(self, i):
        new_board = deepcopy(self.board)
        for y in range(self.size):
            for x in range(self.size):
                curr_cell = self.board[y][x]
                neighbors = self.get_neighbors([y, x])
                # pravidla som nasiel na wiki
                if curr_cell == FIRE:  # A burning cell turns into an empty cell
                    new_board[y][x] = EMPTY
                elif self.board[y][x] == TREE and self.is_neighbor_on_fire(
                        neighbors):  # A tree will burn if at least one neighbor is burning
                    new_board[y][x] = FIRE
                elif self.board[y][x] == TREE and random.uniform(0,
                                                                 1) < self.f:  # A tree ignites with probability f even if no neighbor is burning
                    new_board[y][x] = FIRE
                elif self.board[y][x] == EMPTY and random.uniform(0,
                                                                  1) < self.p:  # An empty space fills with a tree with probability p
                    new_board[y][x] = TREE

        self.board = deepcopy(new_board)
        return [plt.imshow(self.board)]  # animacia

    def forest_fire(self):
        self.init()

        fig = plt.figure()
        anim = animation.FuncAnimation(
            fig,
            self.iterate,
            interval=30, blit=True
        )
        plt.show()


ff_model = ForestFireModel()
ff_model.forest_fire()
