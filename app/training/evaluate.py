import time
from itertools import count
from gym_backgammon.envs.backgammon_game import WHITE, BLACK, COLORS


def evaluate_agents(agents, env, n_episodes):
    scores = {WHITE: 0, BLACK: 0}

    for episode in range(n_episodes):

        agent_color, first_roll, observation = env.reset()
        agent = agents[agent_color]

        start_time = time.time()

        for i in count():
            roll, first_roll = (first_roll, None) if first_roll else (agent.roll_dice(), first_roll)

            valid_actions = env.get_valid_actions(roll)
            observation_next, reward, done, winner = env.step(agent.best_move(valid_actions, env))

            if not done:
                agent = agents[env.get_opponent_agent()]
                continue

            if winner is not None:
                # The game ended in less than 10000 plays so there was no draw
                scores[agent.color] += 1

            total_wins = sum(scores.values()) if sum(scores.values()) > 0 else 1

            print(
                f"Evaluation=> Episode={episode + 1:<6d} | Winner= {COLORS[winner]} | after {i:<4} plays || Wins:"
                f" {agents[WHITE].name}={scores[WHITE]:<6}({(scores[WHITE] / total_wins) * 100:<5.1f}%) |"
                f" {agents[BLACK].name}={scores[BLACK]:<6}({(scores[BLACK] / total_wins) * 100:<5.1f}%) |"
                f" Duration={time.time() - start_time:<.3f} sec")
            break

    return scores


def evaluate_gnubg(agent, env, n_episodes):
    scores = {WHITE: 0, BLACK: 0}

    for episode in range(n_episodes):
        observation, first_roll = env.reset()
        start_time = time.time()
        for i in count():
            if first_roll:
                roll, first_roll = first_roll, None
            else:
                env.game = agent.roll_dice()
                env.update_board(env.game.board)
                roll = env.game.roll

            valid_actions = env.get_valid_actions(roll)

            observation_next, reward, done, info = env.step(agent.best_move(valid_actions, env))

            if not done:
                continue
            winner = {'O': WHITE, 'X': BLACK}[env.game.winner]
            scores[winner] += 1
            total_wins = sum(scores.values()) if sum(scores.values()) > 0 else 1

            print(
                f"EVAL => Game={episode + 1:<6} {'('+env.difficulty+')':>15} | Winner={COLORS[winner]}"
                f" | after {env.game.n_moves:<4} plays ||"
                f" Wins: {agent.name}={scores[WHITE]:<6}({((scores[WHITE] / total_wins) * 100):<5.1f}%)"
                f" | gnubg={scores[BLACK]:<6}({((scores[BLACK] / total_wins) * 100):<5.1f}%)"
                f" | Duration={time.time() - start_time:<.3f} sec")
            break

    env.interface.execute("new session")
    return scores
