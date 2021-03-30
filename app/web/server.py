import os
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from functools import partial


# noinspection PyPep8Naming
class Handler(BaseHTTPRequestHandler):

    def __init__(self, gui, *args, **kwargs):
        self.gui = gui
        super().__init__(*args, **kwargs)

    def parse_data(self, data):
        command = 'move' if 'move' in data['command'].lower() else data['command'].lower()

        routes = {
            'start': lambda: self.gui.start(),
            'new game': lambda: self.gui.start(),
            'roll': lambda: self.gui.roll_dice(),
            'move': lambda: self.gui.move(data['command'].lower())
        }

        response = routes.get(command, lambda: {'message': 'Invalid command\n',
                                                'state': self.gui.env.game.state,
                                                'actions': self.gui.last_commands})()

        self.gui.last_commands = response['actions']
        response['message'] = response['message'].rstrip()

        return response

    def do_GET(self):
        path = urlparse(self.path).path

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            f = open(os.path.dirname(__file__) + '/index.html').read()
            self.gui.reset()

            self.wfile.write(bytes(f, encoding='utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            f = open(os.path.dirname(__file__) + f"{path}").read()
            self.wfile.write(bytes(f, encoding='utf-8'))

    def do_POST(self):
        response = self.parse_data(json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), encoding='utf-8'))


def start(host, port, gui):
    handler = partial(Handler, gui)
    server = HTTPServer((host, port), handler)
    print(f'Starting httpd (http://{host}:{port})...')
    server.serve_forever()
