import sys
from minesweeper import create_minesweeper_board, play_minesweeper

if __name__ == "__main__":
    num_rows, num_cols, mine_count = 0, 0, 0

    if len(sys.argv) < 2:
        num_rows, num_cols, mine_count = 8, 8, 10
    elif len(sys.argv) == 2:
        if sys.argv[1] == "beginner":
            num_rows, num_cols, mine_count = 8, 8, 10
        elif sys.argv[1] == "intermediate":
            num_rows, num_cols, mine_count = 16, 16, 40
        elif sys.argv[1] == "expert":
            num_rows, num_cols, mine_count = 30, 16, 99
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
    print("Generated Minesweeper Board:\n", minesweeper_board)
    play_minesweeper(minesweeper_board, num_rows, num_cols, mine_count)