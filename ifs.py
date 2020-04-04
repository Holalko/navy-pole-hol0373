import numpy as np

from graphs import Graph3D

# definovane modely
model1_transformation1 = np.array([[0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05], [0.00, 0.00, 0.00]])
model1_transformation1_chance = 0.25
model1_transformation2 = np.array([[0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24], [0.00, 0.80, 0.00]])
model1_transformation2_chance = 0.25
model1_transformation3 = np.array([[-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24], [0.00, 0.22, 0.00]])
model1_transformation3_chance = 0.25
model1_transformation4 = np.array([[0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84], [0.00, 0.80, 0.00]])
model1_transformation4_chance = 1 - model1_transformation1_chance - model1_transformation2_chance - model1_transformation3_chance

model1 = [model1_transformation1, model1_transformation2, model1_transformation3, model1_transformation4]

model2_transformation1 = np.array([[0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05], [0.00, 0.00, 0.00]])
model2_transformation1_chance = 0.25
model2_transformation2 = np.array([[0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.22, -0.45], [0.00, 1.00, 0.00]])
model2_transformation2_chance = 0.25
model2_transformation3 = np.array([[-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45], [0.00, 1.25, 0.00]])
model2_transformation3_chance = 0.25
model2_transformation4 = np.array([[0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49], [0.00, 2.00, 0.00]])
model2_transformation4_chance = 1 - model2_transformation1_chance - model2_transformation2_chance - model2_transformation3_chance

model2 = [model2_transformation1, model2_transformation2, model2_transformation3, model2_transformation4]

# nahodne vyberie transformaciu
def pick_transformation(model):
    rand = np.random.random()
    if rand < 0.25:
        return model[0]
    elif rand < 0.50:
        return model[1]
    elif rand < 0.75:
        return model[2]
    else:
        return model[3]

# vykona
#  |x'|   | a b c |   |x|   |j|
# w|y'| = | d e f | * |y| + |k|
#  |z'|   | g h i |   |z|   |l|
def transform(transformation, position):
    x, y, z = position

    matrix = np.array(transformation[0]).reshape(3, 3)

    pos = np.array([x, y, z]).reshape(3, 1)
    third_part = np.array(transformation[1]).reshape(3, 1)
    return matrix.dot(pos) + third_part


def ifs(model, interval):
    iterations = 50000

    all_positions = []
    # nahodne zvolim zaciatocnu pozicii
    x, y, z = (np.random.random(), np.random.random(), np.random.random())
    # k vizualizacii ukladam vsetky body do pola
    all_positions.append((x, y, z))
    for i in range(iterations):
        transformation = pick_transformation(model)
        [x, y, z] = transform(transformation, (x, y, z))
        # toto je trosku skaredy sposob ale funguje :D
        x = x[0]
        y = y[0]
        z = z[0]
        all_positions.append((x, y, z))

    # zobrazim
    graph = Graph3D(interval)
    graph.show_plot(all_positions)


ifs(model1, [
    (-1, 1),
    (0, 7),
    (0, 1)
])
ifs(model2, [
    (-1, 1),
    (0, 5),
    (0, 10)
])
