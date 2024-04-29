import numpy as np
import random
from helper import *
from scipy.signal import convolve2d
from functools import reduce

def get_surrounding_mine_count(board, row, col):
    # Define the neighborhood indices around the target element (row, col)
    neighborhood = board[max(0, row - 1):min(board.shape[0], row + 2),
                         max(0, col - 1):min(board.shape[1], col + 2)]
    mine_count = 0
    for val in neighborhood.flatten():
        if val == -1:
            mine_count += 1        
    return mine_count

def initialize_board(num_rows, num_cols, mine_count):
    flat_board = np.full((num_rows * num_cols), 0, dtype=int)
    mine_positions = np.random.choice(len(flat_board), mine_count, replace=False)
    flat_board[mine_positions] = -1
    board = flat_board.reshape((num_rows, num_cols))
    return board

# Populates non-mine cells that are adjacent to mines with the count of mines
# surrounding them
def populate_mine_neighborhood(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != -1:
                board[i][j] = get_surrounding_mine_count(board, i, j)
    return board

def create_minesweeper_board(num_rows, num_cols, mine_count):
    board = populate_mine_neighborhood(initialize_board(num_rows, num_cols, mine_count))
    return board

def reveal_board(board, revealed_board, x, y):
    num_rows, num_cols = board.shape
    # Base cases for recursion:
    # 1. Out of board bounds or already revealed
    if x < 0 or x >= num_rows or y < 0 or y >= num_cols or ~np.isnan(revealed_board[x][y]):
        return revealed_board
    # 2. Hit a mine (-1)
    if board[x][y] == -1:
        revealed_board[x][y] = -1
        print("Hit a mine! Game Over")
        return revealed_board
    # 3. Reveal the current cell
    revealed_board[x][y] = board[x][y]    
    # Recursive reveal of neighboring cells (8 directions: up, down, left, right, and diagonals)
    if board[x][y] == 0:  # If current cell is blank, reveal neighbors recursively
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                revealed_board = reveal_board(board, revealed_board, x + dx, y + dy)
    return revealed_board

def click(board, state, known, x, y):
    hit_mine = False
    print("Click coordinates: ", x, y)
    state = reveal_board(board, state, x, y)
    print("Shape of state: ", state.shape)
    print("\nState after the most recent click:\n", state)
    # print_colored_array(state)
    # Updating known
    for i in range(len(state)):
        for j in range(len(state[i])):
            if ~np.isnan(state[i][j]):
                if state[i][j] >= 0:
                    known[i][j] = 0
                if state[i][j] == -1:
                    known[i][j] = 1
    print("\nKnown: \n", known)

    if -1 in state:
        hit_mine = True
    return state, known, hit_mine

def is_game_over(board, state, hit_mine):
    if hit_mine:
        return True
    
    game_over = True
    for i in range(len(state)):
        for j in range(len(state[i])):
            if board[i][j] != -1 and np.isnan(state[i][j]):
                game_over = False
    return game_over

# Simpify the game by subtracting the values in each cell by the number of mines we have found
def simplify_state(state, known):
    neighbor_counts = get_true_neighbor_count(known)
    state_copy = state.copy()
    state_copy[~np.isnan(state_copy)] -= neighbor_counts[~np.isnan(state_copy)]
    return state_copy


def infer_obvious_moves(state, known, probabilities):
    new_inference = True
    state = simplify_state(state, known == 1)
    print("Simplified state: \n", state)
    unknown_cells = np.isnan(state) & np.isnan(known)
    print("Unknown cells: \n", unknown_cells)

    while new_inference:
        # stores count of unopened and unknown neighbors
        unknown_neighbor_counts = get_true_neighbor_count(unknown_cells)
        # Finding cells for which the number assigned = number of unopened cells 
        solutions = (state == unknown_neighbor_counts) & (unknown_neighbor_counts > 0)
        print("Solutions mines: \n", solutions)
        known_mines = unknown_cells & reduce(np.logical_or,
            [neighbors(x, y, state.shape) for y, x in zip(*solutions.nonzero())], np.zeros(state.shape, dtype=bool))
        print("Known mines: ", known_mines)
        known[known_mines] = 1
        state = simplify_state(state, known_mines)
        unknown_cells = unknown_cells & ~known_mines
        unknown_neighbor_counts = get_true_neighbor_count(unknown_cells)
        # Squares with a 0 value that are unopened or are still unknown are marked here
        solutions = (state == 0) & (unknown_neighbor_counts > 0)
        print("Solutions safe: \n", solutions)
        known_safe = unknown_cells & reduce(np.logical_or,
            [neighbors(x, y, state.shape) for y, x in zip(*solutions.nonzero())], np.zeros(state.shape, dtype=bool))
        print("Known safe: ", known_safe)
        known[known_safe] = 0
        unknown_cells = unknown_cells & ~known_safe

        # Updating the probabilities: Safe tiles are given a probability of 0, mines are given a probability of 1
        probabilities[known_safe], probabilities[known_mines] = 0, 1
        new_inference = (known_safe | known_mines).any()
    return known, probabilities


def update_state_and_probabilities(state, known, probabilities):
    known, probabilities = infer_obvious_moves(state, known, probabilities)
    # checking if "certain" probabilities have been assigned to any of the tiles
    print("State after update: \n", state)
    print("Known after update: \n", known)
    print("Probabilities after update: \n", probabilities)    
    if ~np.isnan(probabilities).all() and 0 in probabilities:
        return state, known, probabilities




def play_minesweeper(board, num_rows, num_cols, mine_count):
    state = np.full((num_rows, num_cols), np.nan, dtype=float)
    # In 'known', a cells are given the value 1 if it is a mine for sure, 0 if it is not a mine for sure
    # 'np.nan' otherwise 
    known = np.full((num_rows, num_cols), np.nan, dtype=float)
    probabilities = np.full((num_rows, num_cols), np.nan, dtype=float)
    # The first click has to be a random click
    x, y = random.randint(0, num_rows-1), random.randint(0, num_cols-1)
    # We're 'clicking' on the minesweeper board at x,y here
    state, known, hit_mine = click(board, state, known, x, y)
    while not is_game_over(board, state, hit_mine):
        # x, y = next_click(board, state, known, probabilities)
        state, known, probabilities = update_state_and_probabilities(state, known, probabilities)
        print("State after update: \n", state)
        print("Known after update: \n", known)
        print("Probabilities after update: \n", probabilities)

        least_probability = np.nanmin(probabilities)
        print("Least probability: ", least_probability)
        safest_xs, safest_ys = (probabilities == least_probability).nonzero()
        print(f"Safest Xs: {safest_xs}, safest Ys: {safest_ys}")
        for x, y in zip(safest_xs, safest_ys):
            state, known, hit_mine = click(board, state, known, x, y)

    if hit_mine == False:
        print("You Win!")
        # break

        # for x, y in zip(*(probabilities == 1).nonzero()):
            # GUI STUFF LATER


        
