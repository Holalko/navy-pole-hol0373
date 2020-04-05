import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D


class Graph2D:

    def __init__(self, interval):
        self.interval = interval
        plt.ion()
        self.fig = plt.figure()

    def animate(self, points, line, animate=False):
        b_x_v = []
        b_y_v = []
        r_x_v = []
        r_y_v = []
        g_x_v = []
        g_y_v = []
        for p in points:
            if p[2] == "b":
                b_x_v.append(p[0])
                b_y_v.append(p[1])
            elif p[2] == "r":
                r_x_v.append(p[0])
                r_y_v.append(p[1])
            else:
                g_x_v.append(p[0])
                g_y_v.append(p[1])

        plt.clf()
        plt.xlim(self.interval)
        plt.ylim(self.interval)

        line_x_v = [point[0] for point in line]
        line_y_v = [point[1] for point in line]
        plt.plot(line_x_v, line_y_v, "ro-")

        if len(b_x_v) > 0:
            plt.scatter(b_x_v, b_y_v, color="b")
        if len(r_x_v) > 0:
            plt.scatter(r_x_v, r_y_v, color="r")
        if len(g_x_v) > 0:
            plt.scatter(g_x_v, g_y_v, color="g")

        plt.show(block=False)
        if animate:
            plt.pause(0.4)


class Graph3D:

    def __init__(self, interval):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.interval = interval

    def show_plot(self, points):

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        xs = [x for x, y, z in points]
        ys = [y for x, y, z in points]
        zs = [z for x, y, z in points]

        self.ax.set_xlim3d(self.interval[0])
        self.ax.set_ylim3d(self.interval[1])
        self.ax.set_zlim3d(self.interval[2])

        self.ax.scatter(xs, ys, zs, c="black", s=0.5)
        plt.show()
