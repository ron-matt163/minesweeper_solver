# Solving Minesweeper using a Probabilistic Approach

## How to run this stochastic minesweeper solver
Step 1: Enter the /src folder which contains all of the code files

Step 2: If you want to make the program solve a custom sized minesweeper board, you can run the following command:

`python main.py custom <num_rows> <num_cols> <num_of_mines>`

eg: `python main.py custom 12 12 10`

If you simply run `python main.py`, the program attempts to solve a 8X8 board with 10 mines.

If you want the program to solve an easier 8X8 board with 8 mines, run `python main.py easy`

If you want the program to solve a 16X16 board with 32 mines, run `python main.py medium`

If you want the program to solve a 32X16 board with 80 mines, run `python main.py hard`

You can how the state of the board change with each click/move on the terminal. Once the game complete, you
can see stats related to the game (like whether the game was won, no. of clicks,  % of board completion).

You can make the program the minesweeper game using the stochastic approach 500 times for a given board size if you run the command:

`python test_stochastic.py custom <num_rows> <num_cols> <num_of_mines>`

*Please give it a few minutes for the test to complete execution. It is bound to take time since the minesweeper game runs 500 times*

You can make the program the minesweeper game using the knowledge-based approach 500 times for a given board size if you run the command:

`python test_KB.py custom <num_rows> <num_cols> <num_of_mines>`

*Please give it a few minutes for the test to complete execution. It is bound to take time since the minesweeper game runs 500 times*

## How does the knowledge-based approach work?

## How does the stochastic approach work?
