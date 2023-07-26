# Qlearning_mazesolver
solves a given 4x4 and 10x10 mazes by training agent and draws the Qtable. (in progress)
# Introduction
    The purpose of this assignment is to first define the problem of an agent stock in a maze and 
    trying to scape, which includes defining states actions rewards and goal states. 
    and then to train the agent by applying q learning. this is done by creating a qtable and 
    updating it after each action using the qlearning equation.
    q table is basically a map for to see what's the best action in a given state.
    agent then can start to play the maze by using the stimulated annealing algorithm to decide 
    the best move and the qtable as the heuristic. stimulated annealing is used to keep the 
    agent from getting stock in a loop.

# what are the files in this zip file 
    no_gui_bothmazes.py : this is a non_gui version of the code.
        Inputs : none
        Out puts : 4x4 maze and its q table , 10x10 maze and its qtable after running episodes
    gui_4x4_maze.py : this is the GUI version of the code for a 4x4 maze.
    gui_10x10_maze.py : this is the GUI version for the 10x10 example in the assignment.
    mazes.py : contains given mazes

# How the code runs 
    GUI is coded by pygame. the screen contains the qtable and the current state of the maze. 
    number of episode and d factor and learning rate are also shown on the screen.

# QLearning numbers, states and actions 
    states : position of the agent in the maze(between and maze size) 
    actions : moving up, down, left, right.
    goal state : no flags are left on the maze and position of agent is the target position. 
    rewards (gui ) : hit wall - out of board - taking flag / n(flags) win ????
    Rewards (none gui) : hit wall - out of board - taking flag / n(flags) win ????

# Results 
    effect of changing gamma : as gamma increases the effect of rewards increases. this causes 
    agent to prefer bigger results(reaching goal state) over smaller rewards. as its increased the 
    values in the q table are increased but i didn't see much change in the ratio of the values to 
    each other. and the preferred actions didn't change.

    changing alpha : as it increases agent learns faster. with alpha = there were still weird 
    values after episodes.(best action was hitting a wall!) agent with higher alpha values 
    learned faster. increasing alpha also increased the values in qtable. 

# Problems ------------------------------------------------------------------------------------------
    ??? what to do with impossible mazes ???
    ??? find the best route to reach goal form Qtable ???
    ??? best numbers to use ???
