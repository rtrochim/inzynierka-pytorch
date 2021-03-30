import torch
import torch.nn as nn
import datetime
import random
import time
from itertools import count
from gym_backgammon.envs.backgammon_game import WHITE, BLACK, COLORS
from ..agents.td.td_agent import TDAgent
from ..agents.random_agent import RandomAgent
from ..evaluate import evaluate_agents


class BaseModel(nn.Module):
    def __init__(self, alpha, lambda_param, seed=5324533):
        super(BaseModel, self).__init__()
        self.alpha = alpha  # learning rate
        self.lambda_param = lambda_param  # trace-decay parameter
        self.start_episode = 0

        self.eligibility_traces = None
        torch.set_default_tensor_type('torch.DoubleTensor')
        torch.manual_seed(seed)
        random.seed(seed)

    def adjust_weights(self, p, p_next):
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError

    def initialize_weights(self):
        raise NotImplementedError

    def init_eligibility_traces(self):
        self.eligibility_traces = [torch.zeros(weights.shape, requires_grad=False) for weights in
                                   list(self.parameters())]

    def save_checkpoint(self, checkpoint_path, step, name_experiment):
        path = checkpoint_path + f"/{name_experiment}_{step + 1}.tar"
        torch.save({'step': step + 1,
                    'model_state_dict': self.state_dict(),
                    'eligibility': self.eligibility_traces if self.eligibility_traces else []
                    }, path)
        print(f"\nModel saved to: {path}")

    def load_checkpoint(self, path, eligibility_traces=None):
        checkpoint = torch.load(path)

        self.load_state_dict(checkpoint['model_state_dict'])

        self.start_episode = checkpoint['step']

        if eligibility_traces is not None:
            self.eligibility_traces = checkpoint['eligibility']

    def start_training(self, env, n_episodes, checkpoint_path=None, init_eligibility=False, save_step=0, name=''):
        n_episodes += self.start_episode

        scores = {WHITE: 0, BLACK: 0}

        agents = {WHITE: TDAgent(WHITE, net=self), BLACK: TDAgent(BLACK, net=self)}

        durations, steps = [], 0
        start_training = time.time()

        for episode in range(self.start_episode, n_episodes):
            self.init_eligibility_traces() if init_eligibility else None
            # Start the game
            agent_color, first_roll, observation = env.reset()
            agent = agents[agent_color]

            start_time = time.time()

            for i in count():
                roll, first_roll = (first_roll, None) if first_roll else (agent.roll_dice(), first_roll)

                # Evaluate the board before making a move
                p = self(observation)
                valid_actions = env.get_valid_actions(roll)
                observation_next, reward, done, winner = env.step(agent.best_move(valid_actions, env))
                # Evaluate the board after making a move
                p_next = self(observation_next)

                if not done:
                    # Game has not ended, update weights and keep playing
                    self.adjust_weights(p, p_next)
                else:
                    # There can be a draw if no one wins in 10000 plays
                    if winner is not None:
                        self.adjust_weights(p, reward)
                        scores[agent.color] += 1

                    total_wins = sum(scores.values()) if sum(scores.values()) > 0 else 1

                    print(
                        f"Episode={episode + 1:<6d} | Winner={COLORS[winner]} | after {i:<4} plays || Wins:"
                        f" {agents[WHITE].name}={scores[WHITE]:<6}({(scores[WHITE] / total_wins) * 100:<5.1f}%) |"
                        f" {agents[BLACK].name}={scores[BLACK]:<6}({(scores[BLACK] / total_wins) * 100:<5.1f}%) |"
                        f" Duration={time.time() - start_time:<.3f} sec")
                    durations.append(time.time() - start_time)
                    steps += i
                    break

                # Time for opponent
                agent = agents[env.get_opponent_agent()]

                observation = observation_next

            if checkpoint_path and save_step > 0 and episode > 0 and (episode + 1) % save_step == 0:
                self.save_checkpoint(checkpoint_path=checkpoint_path, step=episode, name_experiment=name)
                agents_to_evaluate = {WHITE: TDAgent(WHITE, net=self), BLACK: RandomAgent(BLACK)}
                evaluate_agents(agents_to_evaluate, env, n_episodes=20)
                print()

        total_duration = datetime.timedelta(seconds=int(time.time() - start_training))
        avg_duration = f"Avg game duration: {round(sum(durations) / n_episodes, 3)} seconds"
        avg_length = f"Avg game length: {round(steps / n_episodes, 2)} plays | Total Duration: {total_duration}"

        print(f"\n{avg_duration}")
        print(avg_length)

        if checkpoint_path:
            self.save_checkpoint(checkpoint_path=checkpoint_path, step=n_episodes - 1, name_experiment=name)

            with open(f'{checkpoint_path}/comments.txt', 'a') as file:
                file.write(avg_duration)
                file.write(f"\n{avg_length}")
        env.close()
