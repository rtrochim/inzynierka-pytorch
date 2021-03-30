import requests
from collections import namedtuple
from gym_backgammon.envs.backgammon_game import WHITE, BLACK, NUM_POINTS


class GnubgInterface:
    def __init__(self, host, port):
        self.url = f"http://{host}:{port}"
        # Change board representation from gnu to the one used by our env
        self.board_map = {23 - k: k for k in range(NUM_POINTS)}
        # Position 25 in GNU is for the bar, here it's 24 because we count from 0
        self.board_map[24] = 'bar'
        self.board_map[-1] = -1

    # Tuple ((23,21),(5,4) to string '24/22,6/5'
    def action_to_str(self, action):
        arr = []
        for move in action:
            source, target = move
            # Getting of the bar
            if source == 'bar':
                arr += [f"bar/{target + 1}"]
            # Bearing off
            elif target == -1:
                arr += [f"{source + 1}/off"]
            # Standard move
            else:
                arr += [f"{source + 1}/{target + 1}"]
        return ','.join(arr)

    def parse_response(self, response):
        board = response["board"]
        last_move = response["last_move"][-1] if response["last_move"] else None
        res_info = response["info"][-1] if response["info"] else None
        double, move, roll, agent = False, (), (), None

        if last_move:
            agent = WHITE if last_move['player'] == 'O' else BLACK

            if last_move['action'] == 'move':
                move = tuple(tuple([self.board_map[a - 1], self.board_map[b - 1]]) for (a, b) in last_move['move'])
            if last_move['action'] == "double":
                double = True
            elif 'dice' in last_move:
                roll = tuple(last_move['dice'])
                roll = (-roll[0], -roll[1]) if agent == WHITE else (roll[0], roll[1])

        state = namedtuple('GNUState', ['agent', 'roll', 'move', 'board', 'double', 'winner',
                                        'n_moves', 'action', 'resigned', 'history'])

        return state(agent=agent,
                     roll=roll,
                     move=move,
                     board=board[:],
                     double=double,
                     winner=res_info['winner'] if res_info else None,
                     n_moves=res_info['n_moves'] if res_info else 0,
                     action=last_move,
                     resigned=res_info['resigned'] if res_info else False,
                     history=response["info"])

    # Send the given command to gnubg
    def execute(self, command):
        try:
            return self.parse_response(requests.post(url=self.url, data={"command": command}).json())
        except Exception as e:
            print(f"Connection to {self.url} failed: {e} Check if gnubg is running.")
