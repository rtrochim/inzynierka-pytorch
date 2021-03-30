from .base_agent import BaseAgent
from gym_backgammon.envs.backgammon_game import COLORS
from random import choice


class RandomAgent(BaseAgent):
    def __init__(self, color):
        super().__init__(color)
        self.name = f'RandomAgent({COLORS[color]})'

    def best_move(self, actions, env):
        return choice(list(actions)) if actions else None
