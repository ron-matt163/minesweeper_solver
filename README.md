# Solving Minesweeper using a Knowledge-Based and Probabilistic Approaches

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

You can also see how the state of the board changes in the GUI that pops up after executing `main.py`

## Running a performance test on the Knowledge-Based Minesweeper Solver
You can make the program the minesweeper game using the knowledge-based approach 500 times for a given board size if you run the command:

`python test_KB.py custom <num_rows> <num_cols> <num_of_mines>`

*Please give it a few minutes for the test to complete execution. It is bound to take time since the minesweeper game runs 500 times. You will not see a GUI for these test programs since they are meant solely for performance testing.*

## Running a performance test on the stochastic minesweeper solver
You can make the program solve the minesweeper game using the stochastic approach 500 times for a given board size if you run the command:

`python test_stochastic.py custom <num_rows> <num_cols> <num_of_mines>`

*Please give it a few minutes for the test to complete execution. It is bound to take time since the minesweeper game runs 500 times. You will not see a GUI for these test programs since they are meant solely for performance testing.*

## How does the knowledge-based approach work?
The knowledge-based inference logic has a matrix called `known` which keeps track of all the tiles that are certain 
mines and certain safe tiles. A matrix called `state` contains track of all the tiles that have been opened so far, 
the unopened tiles are represented by a special number. 

The following logic is used to find out tiles that safe and tiles that are mines for certain:

1. If an opened tile has a number 'x' (indicating the presence of x neighbors that are mines) and it has only 'x'
neighbors that not opened yet, then we can infer that all of these unopened neighbors surrounding this opened tile 
are mines. These tiles are flagged in the `known` matrix.

2. If an opened tile has a number 'x' (indicating the presence of x neighbors that are mines) and we observe from 
the `known` matrix that 'x' of its unopened neighbors have been flagged for mines, then we can infer that all of its unflagged and unopened neighbors are safe tiles.

3. In order to simplify the inference process we, we subtract the numbers at each opened tiles of `state` by the number of known unopened neighbors. After this simplification, the numbers in the `state` matrix represents the number of neighboring tiles that have not been flagged as mines instead of the total number of neighboring mines.

4. If the agent cannot find a certain safe tile using these rules at any given step of playing the game, it picks a 
tile at random.


## How does the stochastic approach work?
In our project, the stochastic approach only takes effect when the knowledge-based system cannot find a safe tile to pick next using its rules. In such a scenario, the agent selects a tile that has the least `likelihood` (or probability) of being a mine. The likelihoods are calculated in the following manner:

1. If an opened tile has a number 'x' and it has 'k' unopened neighbors, then each of the unopened neighbors has 
probability of 'x/k' of being a mine (this is assuming that none of the neighbors is adjacent to any other open tile). Let us call this probability 'p'. The opened tiles assigns a likelihood score of 'p' to each of its unopened neighbors

![Example 1 for likelihood score assignment](/assets/likelihood_assignment.png)

2. If an unopened tile has multiple opened neighbors, then each of its opened neighbors assigns a likelihood score of 'p' to it. The effective likelihood score at such a node is the sum of these individual likelihood scores assigned by the opened neighbors.

![Example for likelihood score aggregation](/assets/likelihood_assignment_aggregation.png)

If the knowledge-based system does not find a safe tile, we select the tile with the least likelihood score for our 
next move. The tile with the least likelihood score is the least likely to be a mine. Please note that the likelihood score does not give the exact probability. It could have any value between 0 and 8 since it is the sum 
of the probabilities assigned to it by each of its neighbors.
