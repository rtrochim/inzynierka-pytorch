import args
from gnu.env import DIFFICULTIES


def parse_train(subparser):
    subparser.add_argument('--alpha', type=float, default=1e-4)
    subparser.add_argument('--lambda_param', type=float, default=0.7)
    subparser.add_argument('--episodes', type=int, default=200000)
    subparser.add_argument('--hidden_units', type=int, default=40)
    subparser.add_argument('--init_weights', action='store_true')
    subparser.add_argument('--model', type=str, default=None)
    subparser.add_argument('--name', type=str, default='exp1')
    subparser.add_argument('--seed', type=int, default=123)
    subparser.add_argument('--save_path', type=str, default=None)
    subparser.add_argument('--save_step', type=int, default=0)
    subparser.set_defaults(func=args.train)


def parse_web(subparser):
    subparser.add_argument('--host', default='localhost')
    subparser.add_argument('--port', default=8002, type=int)
    subparser.add_argument('--model', required=True, type=str)
    subparser.add_argument('--hidden_units', required=False, type=int, default=40)
    subparser.set_defaults(func=args.web)


def parse_evaluate(subparser):
    subparser.add_argument('--model0', required=True, type=str)
    subparser.add_argument('--model1', required=False, type=str)
    subparser.add_argument('--hidden_units0', required=False, type=int, default=40)
    subparser.add_argument('--hidden_units1', required=False, type=int, default=40)
    subparser.add_argument('--episodes', default=20, required=False, type=int)
    subparser.set_defaults(func=args.evaluate)
    return subparser.add_subparsers()


def parse_gnubg(subparser):
    subparser.add_argument('--host', type=str, required=True)
    subparser.add_argument('--port', type=int, required=True)
    subparser.add_argument('--difficulty', choices=DIFFICULTIES, type=str, required=False, default=DIFFICULTIES[0])
    subparser.set_defaults(func=args.gnubg)


def parse_random(subparser):
    subparser.set_defaults(func=args.random)


def parse_plot(subparser, parser):
    subparser.add_argument('--hidden_units', type=int, default=40)
    subparser.add_argument('--episodes', default=20, type=int)
    subparser.add_argument('--opponent', default='random', type=str)
    subparser.add_argument('--dst', type=str, default='myexp')
    subparser.add_argument('--checkpoint_path', type=str, required=True)
    subparser.set_defaults(func=lambda parsed_args: args.plot(parsed_args, parser))
