import sys
from minesweeper import create_minesweeper_board, play_minesweeper_stochastic

if __name__ == "__main__":
    num_rows, num_cols, mine_count = 0, 0, 0

    if len(sys.argv) < 2:
        num_rows, num_cols, mine_count = 8, 8, 10
    elif len(sys.argv) == 2:
        if sys.argv[1] == "easy":
            num_rows, num_cols, mine_count = 8, 8, 8
        elif sys.argv[1] == "medium":
            num_rows, num_cols, mine_count = 16, 16, 32
        elif sys.argv[1] == "hard":
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

    minesweeper_board = create_minesweeper_board(num_rows, num_cols, mine_count)
    print("\n\nGenerated Minesweeper Board:\n", minesweeper_board)
    win, board_completion, clicks = play_minesweeper_stochastic(minesweeper_board, num_rows, num_cols, mine_count)
    print(f"\nWin = {win==1}, Board completion % = {board_completion*100},  Clicks = {clicks}")