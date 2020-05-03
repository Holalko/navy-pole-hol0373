import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense


def logistic_equation(a, x):
    return a * x * (1 - x)


def logistic_map(a):
    x = np.linspace(0, 50)
    plt.plot(x, logistic_equation(a, x), 'k')


def bifurcation_diagram():
    a_values = np.linspace(0, 4, 200)

    x_vals = []
    a_vals = []
    for a in a_values:
        x = 0.2
        for i in range(110):
            x = logistic_equation(a, x)
            if i >= 100: # vizualizujem iba poslednych 10 bodov, ked uz je to zconvergovane k nejakemu cislu
                x_vals.append(x)
                a_vals.append(a)
    plt.plot(a_vals, x_vals, ls='', marker=',', color='black')
    plt.show()


def nn():
    # neuronka
    ann = Sequential()
    ann.add(Dense(units=10, activation="relu", input_dim=2))
    ann.add(Dense(units=1, activation="relu"))

    ann.compile(loss='mse', optimizer='sgd')

    a_values = np.linspace(0, 4, 5000)
    np.random.shuffle(a_values) # shuffle aby som nemal overfitting pri trenovani tej neuronky

    inputs = []
    target_outs = []
    for a in a_values:
        x = 0.2
        for _ in range(150):
            # vytvorim si trenovaciu mnozinu
            x = logistic_equation(a, x)
            inputs.append([a, x])
            target_outs.append(x)
    for epoch in range(0, 50):
        print(epoch, "epoch")
        ann.train_on_batch(np.array(inputs), np.array(target_outs)) # train on batch pretoze tych dat je extremne vela a trvalo to roky

    x_vals_nn = [] # sem si ukladam data kvoli vizualizacii
    x_vals_orig = []

    a_vals = []

    a_values = np.linspace(0, 4, 500)
    # vizualizacia
    for a in a_values:
        x = 0.2
        x_orig = 0.2
        for i in range(0, 110):
            # predikovane z NN
            x = ann.predict(np.array([[a, x]]))[0][0]
            # original
            x_orig = logistic_equation(a, x_orig)
            if i >= 100:
                x_vals_nn.append(x)
                x_vals_orig.append(x_orig)
                a_vals.append(a)
    plt.subplot(1, 2, 1)
    plt.plot(a_vals, x_vals_nn, ls='', marker=',', color='black')
    plt.ylabel('NN predictions')
    plt.ylim(-0.05, 1)
    plt.subplot(1, 2, 2)
    plt.plot(a_vals, x_vals_orig, ls='', marker=',', color='black')
    plt.ylabel('Original')
    plt.ylim(-0.05, 1)
    plt.show()


# bifurcation_diagram()
nn()
