import sys
import numpy as np
from minesweeper import *

# Plays minesweeper using a KB approach. 
# The this function calls another function named `update_state_and_probabilities` in the minesweeper.py file 
# which calls a function named infer_obvious_moves(). The infer_obvious_moves() method acts as the knowledge-based agent
def play_minesweeper_KB(board, num_rows, num_cols, mine_count): 
    clicks = 0
    state = np.full((num_rows, num_cols), np.nan, dtype=float)
    # In 'known', a cells are given the value 1 if it is a mine for sure, 0 if it is not a mine for sure
    # 'np.nan' otherwise 
    known = np.full((num_rows, num_cols), np.nan, dtype=float)
    probabilities = np.full((num_rows, num_cols), np.nan, dtype=float)
    # The first click has to be a random click
    x, y = random.randint(0, num_rows-1), random.randint(0, num_cols-1)
    # We're 'clicking' on the minesweeper board at x,y here
    state, known, hit_mine = click(board, state, known, x, y)
    clicks += 1
    while not is_game_over(board, state, hit_mine):
        # Reinitializing probabilities to avoid clicking on the same tile over and over again
        probabilities = np.full((num_rows, num_cols), np.nan, dtype=float)
        # This function calls another function named infer_obvious_moves(). The infer_obvious_moves() method acts as the knowledge-based agent
        state, known, probabilities = update_state_and_probabilities(state, known, probabilities)
        least_probability = np.nanmin(probabilities)
        print("Least likelihood: ", least_probability)
        safest_xs, safest_ys = (probabilities == least_probability).nonzero()
        print(f"Safest Xs: {safest_xs}, safest Ys: {safest_ys}")
        
        # If least probability != 0, it means that the KB approach has not found a certain safe tile
        # In such a scenario, it selects a random tile
        if least_probability != 0:
            x, y = random_select_unknown_cell(known)
            state, known, hit_mine = click(board, state, known, x, y)
            clicks += 1
        else:       
            for x, y in zip(safest_xs, safest_ys):
                state, known, hit_mine = click(board, state, known, x, y)
                clicks += 1
        print("State after click:\n", state)

    print("\nState when game is over: \n",state)
    print("\nInitial board for reference: \n", board)
    board_completion = np.sum(~np.isnan(state))/(state.size-mine_count)

    if hit_mine:
        print("\n\nYOU HIT A MINE! GAME OVER!")
        win = 0
    else:
        print("\n\nYOU WIN!")
        win = 1
    return win, board_completion, clicks


if __name__ == "__main__":
    num_rows, num_cols, mine_count = 0, 0, 0
    total_wins, total_board_completion, total_clicks = 0, 0.0, 0
    num_repeats = 500

    if len(sys.argv) < 2:
        num_rows, num_cols, mine_count = 8, 8, 10
    elif len(sys.argv) == 2:
        if sys.argv[1] == "beginner":
            num_rows, num_cols, mine_count = 8, 8, 8
        elif sys.argv[1] == "intermediate":
            num_rows, num_cols, mine_count = 16, 16, 32
        elif sys.argv[1] == "expert":
            num_rows, num_cols, mine_count = 32, 16, 80
    elif sys.argv[1] == "custom":
        if len(sys.argv) == 5:
            num_rows, num_cols, mine_count = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
            if mine_count > num_rows * num_cols:
                print("Invalid configuration: You cannot have more mines than the number of cells")
                exit(1)
        else:
            print(f"Error! Expected difficulty level (custom), num_rows, num_cols and mine_count as in-line parameters")
            exit(1)
    else:
        print("Error! The command for executing this program should be in following format")
        print("python main.py <difficulty> <num_rows (only for custom)> <num_cols (only for custom)> <mine_count (only for custom)>")
        exit(1)        

    for i in range(num_repeats):
        minesweeper_board = create_minesweeper_board(num_rows, num_cols, mine_count)
        print("\n\nGenerated Minesweeper Board:\n", minesweeper_board)
        win, board_completion, clicks = play_minesweeper_KB(minesweeper_board, num_rows, num_cols, mine_count)
        total_wins += win
        total_board_completion += board_completion
        total_clicks += clicks

    print("\n\nWin % = ", total_wins*100/num_repeats)
    print("Average board completion % = ", total_board_completion*100/num_repeats)
    print("Average no. of clicks per game = ", total_clicks/num_repeats)

