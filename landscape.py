import matplotlib.pyplot as plt
import numpy as np


class LandScapeGenerator:

    # nastavim zakladne hodnoty
    def __init__(self, size, iterations=4, colors=True, lines=True):
        self.all_perturbations = {}
        self.size = size
        # vzladom na to ze chcem aby ten stvorec vyzeral ako kosodlzik,
        # tak ho akokeby "rotujem", aby som vytvoril "3D effekt"
        self.rotation = self.size * 0.5
        # ci mam zobrazovat farby a lines
        self.colors = colors
        self.lines = lines
        self.total_iterations = iterations
        self.current_iteration = 0

    def generate(self):
        self.current_iteration = 0

        # vygenerujem si prvy kosostvorec
        # jednotlive body oznacuju vrcholy
        #         d_____ c
        #        /      /
        #       /      /
        #      a______b
        #
        # z toho dovodu tam mam tu rotation, aby som akokeby bod 'd' a 'c' posunul doprava

        a = (0, 0)
        b = (self.size, 0)
        c = (self.size + self.rotation, self.size)
        d = (self.rotation, self.size)

        # kosostvorec
        init_square = [a, b, c, d]

        squares = []
        squares.append(init_square)

        # pre kazdu iteraciu musim vsetky stvorce rozdelit na 4 mensie
        for i in range(self.total_iterations):
            # toto vyuzivam aby som mohol pre kazdu dalsiu iteraciu zmensit "perturbaciu"
            self.current_iteration = i

            # temp variable
            new_squares = []

            for square in squares:
                divided_square = self.divide_square(square)
                # priradim nove stvroce co sa mi vytvorili
                new_squares += divided_square
            squares = new_squares[:]

        # vizualizacia
        for square in squares:
            square_points = self.square_to_points(square)
            xs = [x[0] for x in square_points]
            ys = [y[1] for y in square_points]
            if self.colors:
                plt.fill(xs, ys, color=self.pick_color(xs, ys))
            if self.lines:
                plt.plot(xs, ys, color="black", linewidth=0.3)

        # plt.axis((75, self.size+75, -25, self.size+100))
        plt.show()

    def pick_color(self, xs, ys):
        x = xs[0]
        y = ys[0]
        if y < self.size * 0.33:
            return "#2b62cf"
        elif y < self.size * 0.66:
            return "#57d46e"
        else:
            return "grey"

    def square_to_points(self, points):
        new_points = points
        new_points.append(points[0])
        return new_points

    # rozdelim stvorec na 4 mensie
    # a pre nove body
    # vertically perturb each of the 5 new vertices by a random amount
    def divide_square(self, square):
        a, b, c, d = square[0], square[1], square[2], square[3]

        # vypocitam si stred
        center = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)

        # perturbacia stredu
        center = self.perturb_point(center)

        # tu pocitam stred medzi bodmi
        # napr stred medzi a-b:
        #
        #         d_____ c
        #        /      /
        #       /      /
        #      a______b
        #         ^
        #     center_a_b
        center_a_b = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        # ten nasledne perturbujem
        center_a_b = self.perturb_point(center_a_b)

        center_a_d = ((a[0] + d[0]) / 2, (a[1] + d[1]) / 2)
        center_a_d = self.perturb_point(center_a_d)

        center_b_c = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)
        center_b_c = self.perturb_point(center_b_c)

        center_d_c = ((d[0] + c[0]) / 2, (d[1] + c[1]) / 2)
        center_d_c = self.perturb_point(center_d_c)

        # dam dokopy nove stvorce
        first_square = [a, center_a_b, center, center_a_d]
        second_square = [center_a_b, b, center_b_c, center]
        third_square = [center, center_b_c, c, center_d_c]
        fourth_square = [center_a_d, center, center_d_c, d]

        return [first_square, second_square, third_square, fourth_square]

    # perturbacia bodu
    def perturb_point(self, point):
        # kvoli tomu, ze ked mam rozdeleny ten prvy stvorec na 4 mensie, tak mam akokeby 4x hodnotu stredu
        # vysvetlenie
        #         d_____ c_______x
        #        /      /        /
        #       /      /        /
        #      a______center___y
        #      /      /        /
        #     /      /        /
        #    k______l________m
        # tak vidim ze vsetky maju akokeby rovnaku suradnicu "center"
        # ale ked to sperturbujem pre stvorec (a,center,c,d) tak potom by som to musel zmenit aj pre ostatne
        # tak aby sedeli tie body
        # tak preto to ukladam do slovnika perturbacii, a ak uz bol dany bod zperturbovany, tak si vytiahnem zo
        # slovnika jeho novu polohu
        if repr(point) in self.all_perturbations:
            return self.all_perturbations.get(repr(point))
        old_x = point[0]
        old_y = point[1]

        # pocitam ako moc sperturbujem
        # kazdou dalsou iteraciou sa to cislo znizuje
        perturbation = self.size * (self.total_iterations / (self.total_iterations + self.current_iteration)) * 0.1
        new_y = old_y + np.random.randint(-perturbation, perturbation)

        new_point = (old_x, new_y)
        self.all_perturbations[repr(point)] = new_point
        return new_point


landscape = LandScapeGenerator(400, iterations=4, colors=True, lines=True)
landscape.generate()
