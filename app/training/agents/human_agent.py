from .base_agent import BaseAgent
from gym_backgammon.envs.backgammon_game import COLORS


class HumanAgent(BaseAgent):
    def __init__(self, color):
        super().__init__(color)
        self.name = f'HumanAgent({COLORS[color]})'

    def best_move(self, actions=None, env=None):
        return None
