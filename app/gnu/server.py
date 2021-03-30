# Python 2.7 required for this to be read by gnubg

import json
import gnubg
# Importing 2.7 versions of these modules
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs


class Handler(BaseHTTPRequestHandler):

    # Handler for GET request
    def do_GET(self):
        # Respond with basic hello if path exists
        if self.urlparse(self.path).path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("It works! GNU Backgammon GUI is at your service!"))

    # Handler for POST request
    def do_POST(self):
        data = parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        old_state = gnubg.match(0)['games'][-1]['game'] if gnubg.match(0) else []
        command = data['command'][0]
        print(command)
        gnubg.command(command)
        response = {'board': [], 'last_move': [], 'info': []}
        if gnubg.match(0):
            previous_games = gnubg.match(0)['games'][-1]
            current_state = previous_games['game'][-1]
            response['last_move'] = [old_state, current_state]
            response['board'] = gnubg.board()
            for index, game in enumerate(gnubg.match(0)['games']):
                response['info'].append(
                    {
                        'n_moves': len(game['game']),
                        'winner': game['info']['winner'],
                        'resigned': game['info']['resigned'] if 'resigned' in game['info'] else None,
                    }
                )
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(response))


def start(host, port):
    address = (host, port)
    server = HTTPServer(address, Handler)
    print('Server started at ({}:{})...'.format(host, port))
    server.serve_forever()


if __name__ == "__main__":
    start(host='0.0.0.0', port=8001)
