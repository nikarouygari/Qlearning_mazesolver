import numpy as np
import random
import time 
import sys
from mazes import *

# OOP --------------------------------------------------------------------------------------------
class agent:
    def __init__(self,i,j):
        self.i = i
        self.j = j

    def locate(self):
        '''returns position of agent'''
        return self.i , self.j
    
    def vmove(self, direction):
        '''moves agent vertically'''
        direction = 1 if direction>0 else -1
        return agent(self.i+direction,self.j)

    def hmove(self, direction):
        '''moves agent horizentally'''
        direction = 1 if direction>0 else -1
        return agent(self.i,self.j+direction)

class maze:
    def __init__(self,rows=10,columns=10,flagcount = 0, flagcount0 = 0):
        self.env = np.zeros((rows,columns))     # creats a zero matrix
        self.q = np.zeros((rows*columns,4))
        self.agent = agent(0,0)
        
        self.flagcount0 = flagcount0
        self.flagcount = flagcount
        self.score = 0

        nr , nc = self.env.shape
        self.size = nr * nc

    def copy(self):
        nr , nc = self.env.shape
        m= maze(nr , nc , self.flagcount , self.flagcount0)
        m.env = self.env.copy()
        return m


    def agent_state(self, agent): ########
        nr, nc =self.env.shape
        return agent.i * nc + agent.j

    
    def agent_in_board(self,agent):
        '''checks if agent is in board'''
        i , j = agent.i , agent.j
        nr , nc = self.env.shape       # array dimension
        return i >= 0 and i < nr and j >=0 and j < nc

    def healthy(self,agent):
        '''checks if agent is in a safe hous(not wall)'''
        return self.env[agent.i,agent.j] != -1

    def valid_agent(self,agent):
        '''is agent valid ??'''
        return self.agent_in_board(agent) and self.healthy(agent)
    
    def all_actions(self):
        '''all actions agent can make'''
        a=self.agent
        return [ 
            (0 , a.vmove(-1)),
            (1 , a.hmove(1)),
            (2 , a.vmove(1)),
            (3 , a.hmove(-1)),
        ]

    def possible_moves(self): ##########################
        '''wont use this function : all moves are valid. we forbid them by adding high - reward'''
        a = self.agent
        states = [ 
            0,a.vmove(-1),
            a.hmove(1),
            a.vmove(1),
            a.hmove(-1),
        ]
        return [(s,ii) for (ii,s) in enumerate(states) if self.valid_agent(s)]
    
    def create_children(self):
        moves = self.all_actions(self)
        return moves
    
    def bfs(self):
        open , closed ,path= [],[],[]
        open.append(agent(0,0))
        while not self.reached_goal():
            agent = open[0]
            for child in self.create_children():
                if child[1] not in closed :
                    open.append(child)

            closed.append(agent[0])
            del open[0]
            path . append (agent[0])



    def take_flag(self):
        '''removes flag from board. adds 10 to score'''
        a = self.agent
        if self.env[a.i,a.j]==4:
            self.env[a.i,a.j] = 0
            self.flagcount -= 1
            self.score += 0.7/self.flagcount0

    def get_hurt(self):
        '''add - score if hit wall'''
        a = self.agent
        if self.env[a.i, a.j] == -1:
            self.score -= 0.5

    def wave_at_death(self):
        '''add -1 score if agent is out of board'''
        a = self.agent
        if not self.agent_in_board(a):
            self.score -= 0.8
        

    def do_a_move(self,agent):
        '''moves to new state if its valid, adds up the score of moving'''
        if self.valid_agent(agent):
            self.agent = agent
        self.score += 100 if self.reached_goal() else -0.04
        self.take_flag()
        self.get_hurt()
        self.wave_at_death()
    
    def no_flag_left(self):
        '''true if no flags are left'''
        return self.flagcount == 0
    
    def reached_goal(self):
        '''true if reached goal state'''
        a= self.agent
        return self.env[a.i,a.j]==1 and self.no_flag_left()


    def visualize(self):

        if self.agent_in_board(self.agent): ##################3 error
            e = self.env.copy()
            m = self.agent
            e[m.i, m.j] = 6
            print(e)

    def play(self  , qtable) : 
        pass


class Qlearn:
    def __init__(self, num_states, num_actions, lr =0.1 , d_factor=1.0):
        self.q=np.zeros((num_states, num_actions))
        self.a= lr
        self.g= d_factor

    def update(self, st , at ,rt , st1):
        '''updates q table : st = n_house , at = n_action , x of house / rt is reward / st1 = next state'''
        q=self.q
        a=self.a
        g=self.g
        q[st, at] = (1 - a)*q[st,at] + a * (rt + g * np.max(q[st1]))

    def visualize(self):
        print(self.q)

    def run_episode(self , maze , n_episode = 1, score_limit = -0.5 ):
        
        while not maze.reached_goal() :

            moves=maze.all_actions()
            move =random.choice(moves)
            # 
            at= move[0]
            st = maze.agent_state(maze.agent)
            # make move
            maze.do_a_move(move[1])
            rt = maze.score
            # next state : if move impossible will return our state
            st1=maze.agent_state(maze.agent)
            # update q table
            # maze.visualize()
            self.update(st,at,rt,st1)
                #time.sleep(0.5)
                # terminate (not solvable or wandering) too long episodes
            if rt <= score_limit * maze.size :
                break

    def train(self , maze0 , n_episodes = 1, score_limit = -0.5 ):

        maze = maze0.copy()
        for n in range(n_episodes):
            maze = maze0.copy()
            self.run_episode (maze)


# PRO --------------------------------------------------------------------------------------------

# mazes
m4 = maze4x4(maze(4,4))
m10 = maze10x10(maze())

# 4x4 tab
print('board 4 x 4')
m4.visualize()
q=Qlearn(16,4)
q.train(m4 ,100)
print('\n')
print('q table')
q.visualize()
print('q table')

# space
print('\n')

# 10x10 tab
print('board 10 x 10')
m10.visualize()
q=Qlearn(100,4)
q.train(m10 ,100)
print('\n')
print('q table')
q.visualize()