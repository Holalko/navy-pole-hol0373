import matplotlib.pyplot as plt
import numpy as np


class MandelBrot:

    def __init__(self):
        self.zoom = 1
        self.move_x = 0
        self.move_y = 0

    def compute_mandelbrot(self, n_max, nx, ny):
        # toto pouzivam kvoli zoomovaniu
        move_x = self.move_x
        move_y = self.move_y
        zoom = 1 / self.zoom

        # pre vypocet sequencie c-cisel, pripocitavam tam move_x/_y a zoom kvoli zoomovaniu
        x_zoom1, x_zoom2 = (-2 + move_x) * zoom, (2 + move_x) * zoom
        y_zoom1, y_zoom2 = (-1.5 + move_y) * zoom, (1.5 + move_y) * zoom
        x = np.linspace(x_zoom1, x_zoom2, nx)
        y = np.linspace(y_zoom1, y_zoom2, ny)

        c = x.reshape(len(x), 1) + 1j * y.reshape(1, len(y))

        z = c
        # z_0  = 0, z_{n+1} = z_n^2 + c
        for j in range(n_max):
            z = z ** 2 + c

        # |z_n| <= m
        mandelbrot_set = (abs(z) < 2)

        return mandelbrot_set

    def onclick(self, event):
        # tu pocitam zoom a zmenu pozicie v grafe po kliknuti na graf
        if event.xdata > 400:
            move_x = 1
        elif event.xdata < 200:
            move_x = -1
        else:
            move_x = 0
        if event.ydata > 400:
            move_y = 1
            zoom = self.zoom + 1
        elif event.ydata < 200:
            move_y = -1
            zoom = self.zoom + 1
        else:
            zoom = self.zoom * 1.5
            move_y = self.move_x * 0.5
            move_x = self.move_y * 0.5

        self.move_x += move_x
        self.move_y += move_y
        self.zoom = zoom

        mandelbrot_set = self.compute_mandelbrot(50, 600, 600)
        plt.imshow(mandelbrot_set.T)
        plt.show()

    def compute(self):
        mandelbrot_set = self.compute_mandelbrot(200, 600, 600)
        plt.imshow(mandelbrot_set.T)
        plt.connect('button_press_event', self.onclick)
        plt.show()


mandelbrot = MandelBrot()
mandelbrot.compute()
