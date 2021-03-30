import gym
import re
import matplotlib.pyplot as plt
import numpy as np
from helpers import *
from training import *
from gnu import *
from gnu.env import DIFFICULTIES
from gym_backgammon.envs.backgammon_game import WHITE, BLACK, COLORS
from web.server import start
from web.gui import GUI
from scipy.interpolate import interp1d

def train(args):
    net = TDGammon(hidden_units=args.hidden_units,
                   alpha=args.alpha,
                   lambda_param=args.lambda_param,
                   init_weights=args.init_weights,
                   seed=args.seed)
    env = gym.make('gym_backgammon:backgammon-v0')

    if args.model and path_exists(args.model):
        net.load_checkpoint(path=args.model, eligibility_traces=True)

    save_path = None
    if args.save_path and path_exists(args.save_path):
        save_path = args.save_path
        write_params_to_file(save_path,
                             save_path=args.save_path,
                             command_line_args=args,
                             hidden_units=args.hidden_units,
                             init_weights=args.init_weights,
                             alpha=net.alpha,
                             lambda_param=net.lambda_param,
                             n_episodes=args.episodes,
                             save_step=args.save_step,
                             start_episode=net.start_episode,
                             name_experiment=args.name,
                             env=env.spec.id,
                             restored_model=args.model,
                             seed=args.seed,
                             eligibility=True,
                             modules=[module for module in net.modules()])

    net.start_training(env=env,
                       n_episodes=args.episodes,
                       checkpoint_path=save_path,
                       save_step=args.save_step,
                       init_eligibility=True,
                       name=args.name)


def web(args):
    if not path_exists(args.model):
        return
    net = TDGammon(hidden_units=args.hidden_units, alpha=0.1, lambda_param=None, init_weights=False)
    env = gym.make('gym_backgammon:backgammon-v0')
    net.load_checkpoint(path=args.model, eligibility_traces=False)
    agents = {BLACK: TDAgent(BLACK, net=net), WHITE: HumanAgent(WHITE)}
    start(host=args.host, port=args.port, gui=GUI(env=env, agents=agents))


def evaluate(args):
    if not path_exists(args.model0) or not path_exists(args.model1):
        return
    net0 = TDGammon(hidden_units=args.hidden_units0, alpha=0.1, lambda_param=None, init_weights=False)
    net1 = TDGammon(hidden_units=args.hidden_units1, alpha=0.1, lambda_param=None, init_weights=False)
    env = gym.make('gym_backgammon:backgammon-v0')

    net0.load_checkpoint(path=args.model0, eligibility_traces=False)
    net1.load_checkpoint(path=args.model1, eligibility_traces=False)

    agents = {WHITE: TDAgent(WHITE, net=net1), BLACK: TDAgent(BLACK, net=net0)}
    evaluate_agents(agents, env, args.episodes)


def gnubg(args):
    if not path_exists(args.model0):
        return
    net0 = TDGammon(hidden_units=args.hidden_units0, alpha=0.1, lambda_param=None, init_weights=False)

    net0.load_checkpoint(path=args.model0, eligibility_traces=False)

    gnubg_interface = GnubgInterface(host=args.host, port=args.port)
    gnubg_env = GnuEnv(gnubg_interface, difficulty=args.difficulty)
    scores = evaluate_gnubg(agent=TDAgentGNU(WHITE, net=net0, interface=gnubg_interface),
                            env=gnubg_env,
                            n_episodes=args.episodes)
    save_scores_for_model(args.model0, scores[WHITE], args.difficulty, args.episodes)


def random(args):
    if not path_exists(args.model0):
        return
    net0 = TDGammon(hidden_units=args.hidden_units0, alpha=0.1, lambda_param=None, init_weights=False)

    net0.load_checkpoint(path=args.model0, eligibility_traces=False)
    env = gym.make('gym_backgammon:backgammon-v0')
    agents = {WHITE: TDAgent(WHITE, net=net0), BLACK: RandomAgent(BLACK)}
    scores = evaluate_agents(agents, env, n_episodes=args.episodes)

    save_scores_for_model(args.model0, scores[WHITE], 'Random', args.episodes)


def plot(args, parser):
    # model_path = args.checkpoint_path
    # hidden_units = args.hidden_units
    # n_episodes = args.episodes
    # opponents = args.opponent.split(',')

    models_paths = [
        './checkpoints/best1',
        './checkpoints/best2',
        './checkpoints/best3',
    ]
    wins = []
    for model in models_paths:
        with open(f'{model}/evaluation.json', 'r') as eval_file:
            data = json.load(eval_file).popitem()[1]
            labels = list(data.keys())
            wins.append(list(data.values()))
    x = np.arange(len(labels))
    width = 0.25
    fig, ax = plt.subplots()
    rects = []
    rects.extend(list(ax.bar(x-width, wins[0], width, label='A')))
    rects.extend(list(ax.bar(x      , wins[1], width, label='B')))
    rects.extend(list(ax.bar(x+width, wins[2], width, label='C')))
    plt.xticks(rotation=30)
    ax.set_xlabel('Poziomy trudności')
    ax.set_ylabel('Wygrane (%)')
    ax.set_ylim([0, 90])
    ax.set_title('Skuteczność najlepszych sieci')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f'{height}',
            xy=(rect.get_x()+(rect.get_width()/2), height),
            xytext=(0, 3),
            textcoords='offset points',
            ha='center',
            va='bottom',
            fontsize=8)
    fig.tight_layout()
    plt.show()
    
    # difficulty = 'Beginner'
    # dirs = [
    #     './checkpoints/hu/hu5/',
    #     # './checkpoints/hu/hu10/',;
    #     # './checkpoints/hu/hu20/',
    #     './checkpoints/hu/hu40/',
    #     # './checkpoints/hu/hu60/',
    #     './checkpoints/hu/hu90/',
    #     # './checkpoints/hu/hu120/',
    #     './checkpoints/hu/hu150/',
    # ]
    # fig, ax = plt.subplots()
    # for dir in dirs:
    #     with open(f'{dir}/evaluation.json', 'r') as eval_file:
    #         data = sorted(json.load(eval_file).items(),
    #                       key=lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', str(s))])
    #         labels = [entry[0].split('_')[1].split('.')[0] for entry in data]
    #         wins = [entry[1][difficulty] for entry in data]
    #         ax.plot(labels, wins)
    # ax.set_ylim([0, 100])
    # ax.set_xlim([0, 100])
    # plt.xticks(np.arange(10, 100, 10), range(1000, 10000, 1000))
    # ax.set(xlabel='Liczba partii treningowych', ylabel='Wygrane (%)')
    # # plt.legend(['\u03B1=0.3', '\u03B1=0.5', '\u03B1=0.7', '\u03B1=0.9'])
    # plt.legend(['n=5', 'n=40','n=90', 'n=150'])
    # plt.title(f'Sieć vs GNUbg - {difficulty}')
    # ax.grid()
    # plt.show()
