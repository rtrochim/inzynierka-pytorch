from gym_backgammon.envs.backgammon_game import WHITE, BLACK, COLORS


class GUI:
    def __init__(self, env, agents=None):
        self.agents = agents
        self.env = env
        self.agent = None
        self.first_roll = None
        self.wins = {WHITE: 0, BLACK: 0}
        self.roll = None
        self.game_started = False
        self.game_finished = False
        self.last_commands = []

    def reset(self):
        self.agent = None
        self.first_roll = None
        self.wins = {WHITE: 0, BLACK: 0}
        self.roll = None
        self.game_started = False
        self.game_finished = False
        self.last_commands = []

    def start(self):
        self.reset()
        message = '\nNew game started\n'
        log = []

        if not self.game_started:
            self.game_finished, self.game_started = False, True
            agent_color, self.first_roll, observation = self.env.reset()
            self.agent = self.agents[agent_color]

            if agent_color == BLACK:
                opponent = self.agents[agent_color]
                message += f"{COLORS[opponent.color]} Starts first | Roll={(abs(self.first_roll[0]), abs(self.first_roll[1]))}\n"

                roll, self.first_roll = (self.first_roll, None) if self.first_roll else (
                opponent.roll_dice(), self.first_roll)

                valid_actions = self.env.get_valid_actions(roll)
                best_action = opponent.best_move(valid_actions, self.env)
                message += f"{COLORS[opponent.color]} | Roll={roll} | Action={best_action} | Run 'roll'\n"
                log.extend(['roll', 'new game'])
                self.env.step(best_action)

                self.agent = self.agents[self.env.get_opponent_agent()]
            else:
                message += f"{COLORS[self.agent.color]} Starts first | Roll={(abs(self.first_roll[0]), abs(self.first_roll[1]))} | Run 'move (src/target)'\n"
                log.extend(self.env.get_valid_actions(self.first_roll))
                self.roll = self.first_roll
        else:
            message = "The game is already started. To start a new game, type 'new game'\n"
            log.append('new game')

        return {'message': message, 'state': self.env.game.state, 'actions': list(log)}

    def roll_dice(self):
        message = ''
        log = []

        if self.roll is not None:
            message += f"You have already rolled the dice {(abs(self.roll[0]), abs(self.roll[1]))}. Run 'move (src/target)'\n"
            valid_actions = self.env.get_valid_actions(self.roll)
            log.append('start') if len(valid_actions) == 0 else log.extend(list(valid_actions))

        elif self.game_finished:
            message += "The game is finished. Type 'Start' to start a new game\n"
            log.append('start')

        elif not self.game_started:
            message += "The game is not started. Type 'start' to start a new game\n"
            log.append('start')

        else:
            self.roll = self.agent.roll_dice()
            message += f"{COLORS[self.agent.color]} | Roll={(abs(self.roll[0]), abs(self.roll[1]))} | Run 'move (src/target)'\n"
            valid_actions = self.env.get_valid_actions(self.roll)
            log.extend(list(valid_actions))

            if len(valid_actions) == 0:
                message += "You cannot move\n"

                opponent = self.agents[self.env.get_opponent_agent()]

                roll = opponent.roll_dice()

                valid_actions = self.env.get_valid_actions(roll)
                best_action = opponent.best_move(valid_actions, self.env)
                message += f"{COLORS[opponent.color]} | Roll={roll} | Action={best_action}\n"
                observation_next, reward, done, info = self.env.step(best_action)

                if not done:
                    self.agent, self.roll = self.agents[self.env.get_opponent_agent()], None
                    log.extend(['roll', 'new game'])
                else:
                    winner = self.env.game.get_winner()
                    message += f"Game Finished!!! {COLORS[winner]} wins \n"
                    log.append('new game')
                    self.game_finished = True

        return {'message': message, 'state': self.env.game.state, 'actions': list(log)}

    def move(self, command):
        message = ''
        log = []

        if self.roll is None:
            message += "You must roll the dice first\n"
            log = self.last_commands

        elif self.game_finished:
            message += "The game is finished. Type 'new game' to start a new game\n"
            log.append('new game')

        else:
            try:
                action = parse_move(command)
            except Exception as e:
                message += "Error during parsing move\n"
                log = self.last_commands

            else:
                valid_actions = self.env.get_valid_actions(self.roll)

                if action in valid_actions:
                    message += f"{COLORS[self.agent.color]} | Roll={(abs(self.roll[0]), abs(self.roll[1]))} | Action={action}\n"
                    observation_next, reward, done, info = self.env.step(action)

                    if not done:
                        agent_color = self.env.get_opponent_agent()
                        opponent = self.agents[agent_color]

                        roll = opponent.roll_dice()
                        valid_actions = self.env.get_valid_actions(roll)
                        action = opponent.best_move(valid_actions, self.env)

                        message += f"{COLORS[opponent.color]} | Roll={roll} | Action={action}\n"
                        observation_next, reward, done, info = self.env.step(action)

                        if not done:
                            log.extend(['roll', 'new game'])
                            agent_color = self.env.get_opponent_agent()
                            self.agent = self.agents[agent_color]
                            self.roll = None

                        else:
                            winner = self.env.game.get_winner()
                            message += f"Game Finished!!! {COLORS[winner]} wins\n"
                            log.append('new game')
                            self.game_finished = True

                    else:
                        winner = self.env.game.get_winner()
                        message += f"Game Finished!!! {COLORS[winner]} wins\n"
                        log.append('new game')
                        self.game_finished = True
                else:
                    message += f"Illegal move | Roll={(abs(self.roll[0]), abs(self.roll[1]))}\n"

        return {'message': message, 'state': self.env.game.state, 'actions': list(log)}


def parse_move(command):
    action = command.split()[1]
    action = action.split(',')
    play = []
    bar_play = False

    for move in action:
        move = move.replace(')', '')
        move = move.replace('(', '')
        source, target = move.split('/')

        if source != 'BAR' and source != 'bar':
            play.append((int(source), int(target)))
        else:
            play.append(('bar', int(target)))
            bar_play = True

    if bar_play:
        action = tuple(play)
    else:
        action = tuple(sorted(play, reverse=True))

    return action
