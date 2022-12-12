from copy import deepcopy

import numpy as np
import random
from nimply import cook_status_t1


class Agent(object):
    def __init__(self, states, alpha=0.15, random_factor=0.2):  # 80% explore, 20% exploit
        state = tuple(states.rows)
        self.state_history = []  # state, reward
        self.alpha = alpha
        self.random_factor = random_factor
        self.G = {}
        self.init_reward(states)

    def init_reward(self, states):
        '''
        Initialize rewards for each possible move, referring to
        (i,j) = (state index, n. objects to be taken)
        '''
        for i, row in enumerate(states.rows):
            for j in range(1, row+1):
                self.G[(i,j)] = np.random.uniform(low=1.0, high=0.1)

    def choose_action(self, state):
        allowedMoves = cook_status_t1(state)["possible_moves"]
        maxG = -10e15
        next_move = None
        randomN = np.random.random()
        if randomN < self.random_factor:
            # if random number below random factor, choose random action
            next_move = random.choice(allowedMoves)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for action in allowedMoves:
                tmp = deepcopy(state)
                tmp.nimming(action)
                new_state = tuple(tmp.rows)
                if self.G[action] >= maxG:
                    next_move = action
                    maxG = self.G[action]

        return next_move

    def update_state_history(self, action, reward):
        self.state_history.append((action, reward))

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            # print('(prev, reward): ', (prev, reward))
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []

        self.random_factor -= 10e-5  # decrease random factor each episode of play
