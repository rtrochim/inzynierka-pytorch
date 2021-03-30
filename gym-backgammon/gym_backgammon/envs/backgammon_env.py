import gym
from gym_backgammon.envs.backgammon_game import BackgammonGame as Game, WHITE, BLACK, COLORS
from random import randint
import numpy as np

class BackgammonEnv(gym.Env):

    def __init__(self):
        self.game = Game()
        self.current_agent = None
        self.move_counter = 0
        self.max_moves = 10000

    def step(self, action):
        self.game.make_move(self.current_agent, action)

        observation = self.game.get_observation(self.game.get_opponent(self.current_agent))
        reward, done, winner = 0, False, self.game.get_winner()

        if winner is not None or self.move_counter > self.max_moves:
            if winner == WHITE:
                reward = 1
            done = True
        self.move_counter += 1

        return observation, reward, done, winner

    def reset(self):
        # Roll dice in order to determine whos to start
        roll = randint(1, 6), randint(1, 6)

        # If rolls are equal, roll again
        while roll[0] == roll[1]:
            roll = randint(1, 6), randint(1, 6)

        # Set beginning player
        if roll[0] > roll[1]:
            self.current_agent = WHITE
            roll = (-roll[0], -roll[1])
        else:
            self.current_agent = BLACK

        self.game = Game()
        self.move_counter = 0

        return self.current_agent, roll, self.game.get_observation(self.current_agent)

    def render(self):
        self.game.render()
        return True

    def get_valid_actions(self, roll):
        return self.game.get_valid_actions(self.current_agent, roll)

    def get_opponent_agent(self):
        self.current_agent = self.game.get_opponent(self.current_agent)
        return self.current_agent
