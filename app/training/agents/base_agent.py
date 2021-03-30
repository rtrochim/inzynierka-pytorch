from gym_backgammon.envs.backgammon_game import WHITE, COLORS
from random import seed, randint


class BaseAgent:
    def __init__(self, color):
        self.name = f'Agent({COLORS[color]})'
        self.color = color
        seed(0)

    def best_move(self, actions, env):
        raise NotImplementedError

    def roll_dice(self):
        return (randint(1, 6), randint(1, 6)) if self.color != WHITE else (-randint(1, 6), -randint(1, 6))
