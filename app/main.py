import argparse
from parsers import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parse_train(subparsers.add_parser('train'))
    parse_web(subparsers.add_parser('web'))

    opponent_subparser = parse_evaluate(subparsers.add_parser('evaluate'))
    parse_gnubg(opponent_subparser.add_parser('vs_gnubg'))
    parse_random(opponent_subparser.add_parser('vs_random'))

    parse_plot(subparsers.add_parser('plot'), parser)
    parsed_args = parser.parse_args()
    parsed_args.func(parsed_args)
