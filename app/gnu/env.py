from gym_backgammon.envs.backgammon_game import BackgammonGame, WHITE, BLACK, NUM_POINTS

DIFFICULTIES = [
    'Beginner',
    'Casual',
    'Intermediate',
    'Advanced',
    'Expert',
    'WorldClass',
    'Supremo',
    'Grandmaster',
    '4ply'
]


class GnuEnv:
    def __init__(self, interface, difficulty=DIFFICULTIES[0]):
        self.env = BackgammonGame()
        self.agent = WHITE
        self.interface = interface
        self.difficulty = difficulty
        self.game = None
        self.viewer = None

    def step(self, action):
        if self.game.winner is None and action:
            self.game = self.interface.execute(self.interface.action_to_str(action))
        # If gnubg wants to double, always take
        if self.game.double and self.game.winner is None:
            self.game = self.interface.execute("take")
        # If gnubg resigns always accept
        if self.game.agent == WHITE and self.game.action[
            'action'] == 'move' and self.game.winner is None and self.game.winner != 'O':
            self.game = self.interface.execute("accept")

        self.update_board(self.game.board)

        observation = self.env.get_observation(self.agent)

        winner = self.game.winner

        done, reward = False, 0

        if winner is not None:
            winner = WHITE if winner == 'O' else BLACK
            reward = 1 if winner == WHITE else 0
            done = True

        return observation, reward, done, winner

    def reset(self):
        # Begin new game
        self.game = self.interface.execute("new session")
        self.set_difficulty()

        roll = None if self.game.agent == BLACK else self.game.roll

        self.agent = WHITE
        self.env = BackgammonGame()
        self.update_board(self.game.board)

        observation = self.env.get_observation(self.agent)
        return observation, roll

    def update_board(self, gnu_board):
        # Set our board to be the same as the gnu board
        # Each player in gnu has a list of 25 elements
        gnu_white, gnu_black = gnu_board[0], gnu_board[1]
        board = [(0, None)] * NUM_POINTS

        for src, checkers in enumerate(reversed(gnu_white[:-1])):
            if checkers > 0:
                board[src] = (checkers, BLACK)

        for src, checkers in enumerate(gnu_black[:-1]):
            if checkers > 0:
                board[src] = (checkers, WHITE)

        self.env.board = board
        # Checkers on the bar
        self.env.bar = [gnu_black[-1], gnu_white[-1]]
        # Checkers which bore off
        self.env.off = [15 - sum(gnu_black), 15 - sum(gnu_white)]
        # Set both players position
        self.env.players_positions = self.env.get_players_positions()

    def get_valid_actions(self, roll):
        return self.env.get_valid_actions(self.agent, roll)

    def render(self):
        self.env.render()
        return True

    def set_difficulty(self):
        self.interface.execute('set automatic roll off')
        self.interface.execute('set automatic game off')

        commands = {
            DIFFICULTIES[0]: ['chequerplay evaluation plies 0',
                              'chequerplay evaluation prune off',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.080',
                              'cubedecision evaluation plies 0',
                              'cubedecision evaluation prune off',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.080'],

            DIFFICULTIES[1]: ['chequerplay evaluation plies 0',
                              'chequerplay evaluation prune off',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.060',
                              'cubedecision evaluation plies 0',
                              'cubedecision evaluation prune off',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.060'],

            DIFFICULTIES[2]: ['chequerplay evaluation plies 0',
                              'chequerplay evaluation prune off',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.040',
                              'cubedecision evaluation plies 0',
                              'cubedecision evaluation prune off',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.040'],

            DIFFICULTIES[3]: ['chequerplay evaluation plies 0',
                              'chequerplay evaluation prune off',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.020',
                              'cubedecision evaluation plies 0',
                              'cubedecision evaluation prune off',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.020'],

            DIFFICULTIES[4]: ['chequerplay evaluation plies 0',
                              'chequerplay evaluation prune off',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.000',
                              'cubedecision evaluation plies 0',
                              'cubedecision evaluation prune off',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.000'],

            DIFFICULTIES[5]: ['chequerplay evaluation plies 2',
                              'chequerplay evaluation prune on',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.000',
                              'cubedecision evaluation plies 2',
                              'cubedecision evaluation prune on',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.000',
                              'movefilter 1 0 0 8 0.160',
                              'movefilter 2 0 0 8 0.160',
                              'movefilter 3 0 0 8 0.160',
                              'movefilter 3 2 0 2 0.040',
                              'movefilter 4 0 0 8 0.160',
                              'movefilter 4 2 0 2 0.040'],

            DIFFICULTIES[6]: ['chequerplay evaluation plies 2',
                              'chequerplay evaluation prune on',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.000',
                              'cubedecision evaluation plies 2',
                              'cubedecision evaluation prune on',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.000',
                              'movefilter 1 0 0 16 0.320',
                              'movefilter 2 0 0 16 0.320',
                              'movefilter 3 0 0 16 0.320',
                              'movefilter 3 2 0 4 0.080',
                              'movefilter 4 0 0 16 0.320',
                              'movefilter 4 2 0 4 0.080'],

            DIFFICULTIES[7]: ['chequerplay evaluation plies 3',
                              'chequerplay evaluation prune on',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.000',
                              'cubedecision evaluation plies 3',
                              'cubedecision evaluation prune on',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.000',
                              'movefilter 1 0 0 16 0.320',
                              'movefilter 2 0 0 16 0.320',
                              'movefilter 3 0 0 16 0.320',
                              'movefilter 3 2 0 4 0.080',
                              'movefilter 4 0 0 16 0.320',
                              'movefilter 4 2 0 4 0.080'],

            DIFFICULTIES[8]: ['chequerplay evaluation plies 4',
                              'chequerplay evaluation prune on',
                              'chequerplay evaluation cubeful on',
                              'chequerplay evaluation noise 0.000',
                              'cubedecision evaluation plies 4',
                              'cubedecision evaluation prune on',
                              'cubedecision evaluation cubeful on',
                              'cubedecision evaluation noise 0.000',
                              'movefilter 1 0 0 16 0.320',
                              'movefilter 2 0 0 16 0.320',
                              'movefilter 3 0 0 16 0.320',
                              'movefilter 3 2 0 4 0.080',
                              'movefilter 4 0 0 16 0.320',
                              'movefilter 4 2 0 4 0.080']
        }[self.difficulty]

        for cmd in commands:
            self.interface.execute(f'set player gnubg {cmd}')

        self.interface.execute('save setting')
