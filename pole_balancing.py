import gym
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras.optimizers import Adam

env = gym.make('CartPole-v0')


class Agent:

    def __init__(self):
        # ako casto bude explorovat
        self.exploration_rate = 1
        # najmensi exploration_rate
        self.exploration_rate_min = 0.01
        # o kolko sa bude zmensovat exploration_rate
        self.exploration_rate_reduce = 0.999

        # definicia neuronky
        self.ann = Sequential()
        self.ann.add(Dense(units=24, activation="relu", input_dim=4))
        self.ann.add(Dense(units=24, activation="relu"))
        self.ann.add(Dense(units=24, activation="relu"))
        self.ann.add(Dense(units=2, activation="linear"))

        # mean squared error ako loss function
        # optimizer Adam s learning ratom 0.001
        self.ann.compile(loss='mse', optimizer=Adam(lr=0.001))

        # pouzivam ju v bellman vzorci
        # v podstate urcuje to ako moc ma zaujimaju akcie v nasledujucom "state"
        # do ktoreho sa dostanem ked vykonam akciu
        self.discount_rate = 0.95


    def select_action(self, state):
        """
        Vyberie akciu ktoru treba vykonat - doprava/dolava
        :param state:
        :return:
        """

        # vyberie random akciu
        if np.random.random() < self.exploration_rate:
            action = env.action_space.sample()
        else: # akciu vyberie ANN
            output = self.ann.predict(state)
            action = get_index_of_highest(output)

        # zredukujem exploration rate
        if self.exploration_rate > self.exploration_rate_min:
            self.exploration_rate *= self.exploration_rate_reduce

        return action

    def fit_network(self, last_state, new_state, action, reward, is_done):
        """
         tuto metodu pouzivam na "trenovanie" neuronovej siete
        :param last_state:  stav s1 v ktorom som bol v case t1
        :param new_state: stav s2 v ktorom som v case t2
        :param action: akcia a1 ktoru som vykonal v stave s1 v case t1
        :param reward: odmena za akciu ktoru som vykonal v stave s1, cize reward = (s1, a1)
        :param is_done: boolean
        """

        # predikovane hodnoty neuronovej siete => array s double cislami, pricom kazde reprezentuje
        # vyber nejakej akcie = doprava/dolava
        # predikovane hodnoty pre stav s1
        predicted = self.ann.predict(last_state)

        # predikovane hodnoty pre stav s2
        next_q_values = self.ann.predict(new_state)
        next_q_max_index = get_index_of_highest(next_q_values)

        # najlepsie ohodnotenie akcie v stave s2
        # ked som v stave s1 a vykonam akciu a1 => tak pomocou tohto si viem zistit
        # aku najlepsiu akciu budem moct vykonat v stave s2
        # vdaka tomu mozem lepsie "trenovat" neuronku
        next_q_max = next_q_values[0][next_q_max_index]

        if is_done:
            predicted[0][action] = -10
        else:
            # bellmanov vzorec
            predicted[0][action] = reward + self.discount_rate * next_q_max

        # trening neuronky
        # vstup je stav s1
        # labels su upravene predicted podla bellman vzorca
        self.ann.fit(last_state, predicted, verbose=0)


def pole_balancing():
    last_state = np.array([env.reset()])
    agent = Agent()

    steps = 0
    episode = 0
    while True:
        env.render()
        action = agent.select_action(last_state)
        curr_state, reward, done, _ = env.step(action)

        agent.fit_network(last_state, np.array([curr_state]), action, reward, done)

        last_state = np.array([curr_state])
        steps += 1
        if done:
            print("episode: ", episode, "score: ", steps)
            episode += 1
            steps = 0
            env.reset()
            last_state = np.array([env.reset()])

    env.close()


def get_index_of_highest(arr):
    """
        Najde index najvyssieho cisla v poli
    :param arr: napr. pole [1,2,3,4,2] => vrati index 3
    :return:
    """
    index = 0
    val = arr[0][index]
    for i in range(1, len(arr[0])):
        if arr[0][i] > val:
            index = i
            val = arr[0][i]
    return index


pole_balancing()
