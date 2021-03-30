import numpy as np
from .td_agent import TDAgent
from gym_backgammon.envs.backgammon_game import WHITE


class TDAgentGNU(TDAgent):

    def __init__(self, color, net, interface):
        super().__init__(color, net)
        self.interface = interface

    def roll_dice(self):
        game = self.interface.execute("roll")
        # Rolling the dice can end in two ways
        # - I can perform a move
        # - I cannot move, so the enemy rolls the dice, moves and may finally ask for a double

        # We need to check who made the last play
        previous_agent = game.agent
        if previous_agent == self.color:
            # I can send the move command
            return game
        else:
            # The opponent is to play
            while previous_agent != self.color and game.winner is None:
                if game.double:
                    # Always take the double
                    game = self.interface.execute("take")
                else:
                    # Else make the next roll
                    game = self.interface.execute("roll")
                previous_agent = game.agent
            return game

    def best_move(self, valid_moves, gnu_env):
        if not valid_moves:
            return None

        game = gnu_env.env
        state = game.save_state()

        # Simulate performing every move
        values = []
        for i, move in enumerate(valid_moves):
            game.make_move(self.color, move)
            observation = game.get_observation(game.get_opponent(self.color))
            values += self.net(observation)
            # Undo the move and restore board state
            game.restore_state(state)

        # We look for the move that maximizes the value for WHITE player and minimizes it for BLACK
        best_move = list(valid_moves)[int(np.argmax(values)) if self.color == WHITE else int(np.argmin(values))]

        return best_move

