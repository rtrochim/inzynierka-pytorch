import numpy as np

from ..base_agent import BaseAgent
from gym_backgammon.envs.backgammon_game import WHITE, COLORS


class TDAgent(BaseAgent):
    def __init__(self, color, net):
        super().__init__(color)
        self.net = net
        self.name = f'TDAgent({COLORS[color]})'

    def best_move(self, valid_moves, env):
        if not valid_moves:
            return None

        saved_counter = env.move_counter
        env.move_counter = 0
        state = env.game.save_state()

        # Simulate performing every move
        values = []
        for i, move in enumerate(valid_moves):
            observation, reward, done, info = env.step(move)
            values += self.net(observation)

            # Undo the move and restore board state
            env.game.restore_state(state)

        # We look for the move that maximizes the value
        # for WHITE player and minimizes it for BLACK
        best_action = list(valid_moves)[int(np.argmax(values))
        if self.color == WHITE else int(np.argmin(values))]

        # Restore counter
        env.move_counter = saved_counter

        return best_action
