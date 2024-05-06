import matplotlib.pyplot as plt
import multiprocessing
from functools import partial

import run
from strategy import GameStrategy, PlayerStrategy

def run_game_wrapper(max_player_strategy, min_player_strategy, debug_print=False):
    result = run.run_game('initial_state.txt', max_player_strategy, min_player_strategy, 3, debug_print)
    return result

def run_games():
    max_player_strategy = GameStrategy(True, PlayerStrategy.EARLY_GAME_CONQUER_CENTER, PlayerStrategy.MIDDLE_GAME_MOVE_DIAGONAL, PlayerStrategy.END_GAME_FILL_FROM_END)
    min_player_strategy = GameStrategy(False, PlayerStrategy.EARLY_GAME_CONQUER_CENTER, PlayerStrategy.MIDDLE_GAME_MOVE_DIAGONAL, PlayerStrategy.END_GAME_FILL_FROM_END)
    
    # Create a pool of processes
    pool = multiprocessing.Pool(processes=5)
    run_game_partial = partial(run_game_wrapper, max_player_strategy, min_player_strategy)
    results = pool.map(run_game_partial, [False]*5)

    final_results = []
    for result in results:
        final_results.append(result)

    pool.close()
    pool.join()

    return final_results

def plot_results():
    fig, ax = plt.subplots(figsize=(10,5))

    results = run_games()

    for game_results in results:
        ax.plot(game_results[0].min_player_visited_nodes.keys(), game_results[0].min_player_visited_nodes.values(), label='MIN')
        ax.plot(game_results[0].max_player_visited_nodes.keys(), game_results[0].max_player_visited_nodes.values(), label='MAX')
    ax.set_title('Put option values for different time to maturity')
    ax.legend(loc='upper left')

    plt.show()

if __name__=='__main__':
    plot_results()