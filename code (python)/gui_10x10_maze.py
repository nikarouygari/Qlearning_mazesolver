import numpy as np
import random
import time 
import pygame
import sys
from mazes import *

# graphics -----------------------------------------------------------------------------------------------
WHITE , BLUE , RED , GREEN = (255 , 255 , 255) , (0 , 0 ,255) , (255 ,0 ,0) , (0,255,0)



def set_screen_qtable(screen , ns = 100 , na = 4 , wr = 34 , wh = 34):
    
    head_width = 100
    head_height = wh
    width , height = wr*ns//2 + head_width , (wh*na + head_height)*2

    font = pygame.font.SysFont('Arial',15)


            #label1 = font.render(str(), 1, FONT_COLOR)
            #label2 = font.render(str(self.players[0].name) + ' wins!', 1, FONT_COLOR)

    for j in range(0 , na):
        for i in range(0 , ns):
            #ns * j + ns

            pygame.draw.rect(screen, RED , (wr*i+head_width ,0 , wr , head_height))
            pygame.draw.rect(screen, RED , (wr*i+head_width , wh*na+head_height , wr , head_height))

            pygame.draw.rect(screen, BLUE , (0 , wh*(j)+head_height , head_width , wh))
            pygame.draw.rect(screen, BLUE , (0 , wh*(j+na)+head_height*2 , head_width , wh))

            pygame.draw.rect(screen, WHITE , (wr*i+head_width , wh*j+head_height , wr , wh ),1 )
            pygame.draw.rect(screen, WHITE , (wr*i+head_width , wh*(j+na)+head_height*2 , wr , wh ),1 )

    for i in range(1 , ns//2 +1 ):
        label = font.render(str(i), 2, WHITE)
        screen.blit(label ,(wr*i+head_width-20 , 0))

    for i in range(ns//2 +1 , ns +1 ):
        label = font.render(str(i), 2, WHITE)
        screen.blit(label ,(wr*i+head_width*2-20-width , head_height + na*wh))

    act = ('up' , 'right' , 'down' , 'left')
    for i in range(0,4):
        label = font.render(act[i], 2, WHITE)
        screen.blit(label ,(10, wh*i+head_height))

    act = ('up' , 'right' , 'down' , 'left')
    for i in range(0,4):
        label = font.render(act[i], 2, WHITE)
        screen.blit(label ,(10, wh*i+head_height*2 + na *wh))

        

    pygame.display.update()

def set_screen_board(screen ,maze , episode, a = 10 , h = 50 ,h2 = 34 , ns =100 , na = 4):
    head_width = 75
    head_height = h2 *(na+1)*2 + 75
    width , height = a * h , a * h
    font = pygame.font.SysFont('Arial',15)
    
    for j in range(0 , a):
        for i in range(0 , a):
            #ns * j + ns

            pygame.draw.rect(screen, WHITE , (h*i+head_width , h*j+head_height , h , h ),1 )

    for j in range(0,a):
        for i in range(0,a):
            val = maze[j][i]
            if val == -1 :
                pygame.draw.rect(screen, RED , (h*i+head_width , h*j+head_height , h , h ) )
            elif val == 4 :
                pygame.draw.rect(screen, BLUE , (h*i+head_width , h*j+head_height , h , h ) )
            elif val == 1 :
                pygame.draw.rect(screen, GREEN , (h*i+head_width , h*j+head_height , h , h ))
            elif val == 6 :
                pygame.draw.rect(screen, WHITE , (h*i+head_width , h*j+head_height , h , h ) )
        
    text_x , text_y = head_width + a * h + 75 , head_height 
    font1 = pygame.font.SysFont('Arial',60)

    label = font1.render('episode : ' + str(episode) , 2, WHITE)
    screen.blit(label ,(text_x , text_y))


    pygame.display.update()

def update_screen_qtabe(screen , q , h = 34):
    ns , na = q.shape
    font = pygame.font.SysFont('Arial',15)
    head_width , head_height = 100 , h
    width  = h*ns//2
    
    set_screen_qtable(screen)
    for j in range(0,na):
        for i in range(0,ns//2):
            val = q[i][j] 
            label = font.render(str("{:.2f}".format(val)), 2, WHITE)
            screen.blit(label ,(h*i+head_width+2 , h*j+head_height))

    for j in range(0,na):
        for i in range(ns//2 , ns ):
            val = q[i][j] 
            label = font.render(str("{:.2f}".format(val)), 2, WHITE)
            screen.blit(label ,(h*i+head_width-h *ns//2+2 , h*j+head_height*2 + na *h))

    pygame.display.update() 

def set_screen(maze ,episode = 0, h=34):
    pygame.init()
    screen = pygame.display.set_mode((1800,1000))
    set_screen_qtable(screen)
    set_screen_board(screen , maze , episode)

def update_screen(maze , q, episode):
    screen = pygame.display.set_mode((1800,1000))
    set_screen_board(screen , maze, episode)
    update_screen_qtabe(screen , q)


# oop ------------------------------------------------------------------------------------------------------
# score : state
# 0 : free 
# 1 : goal
# -1: wall
# 4 : flag


# set up the maze board
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


    def take_flag(self):
        '''removes flag from board. adds 10 to score'''
        a = self.agent
        if self.env[a.i,a.j]==4:
            self.env[a.i,a.j] = 0
            self.flagcount -= 1
            self.score += 7/self.flagcount0

    def get_hurt(self):
        '''add - score if hit wall'''
        a = self.agent
        if self.env[a.i, a.j] == -1:
            self.score -= 5

    def wave_at_death(self):
        '''add -1 score if agent is out of board'''
        a = self.agent
        if not self.agent_in_board(a):
            self.score -= 8
        

    def do_a_move(self,agent):
        '''moves to new state if its valid, adds up the score of moving'''
        if self.valid_agent(agent):
            self.agent = agent
        self.score += 1000 if self.reached_goal() else -0.04
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

        self.agent_in_board(self.agent) ##################3 error
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

    def visualize(self,maze , episode):
        q , m = self.q , maze.env
        update_screen(m , q , episode)

    def run_episode(self , maze , n_episode = 1, score_limit = -1 ):
        set_screen(maze.env)
        while not maze.reached_goal() :
            #if n_episodes -a <n_episodes : break
            pygame.display.update()
            for event in pygame.event.get():
                # close it and exit the program
                if event.type == pygame.QUIT:
                    sys.exit()
                # choose move
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
            self.visualize( maze , n_episode)
                #time.sleep(0.5)
                # terminate (not solvable or wandering) too long episodes
            if rt <= score_limit * maze.size :
                break

    def train(self , maze0 , n_episodes = 1 ):
        pygame.init()
        for n in range(0,n_episodes) :
            maze = maze0.copy()
            self.run_episode (maze , n_episodes - n)

        while True :
            pygame.display.update()
            for event in pygame.event.get():
                # close it and exit the program
                if event.type == pygame.QUIT:
                    sys.exit()


        


# test board -------------------------------------------------------------------------
'''write action sequence to solve board'''

def action_sequence(q):
    lst = [('up',0),('right',1),('down' , 2),('left' , 3)]
    open , closed = [] , []

    nr , nc = q.shape




# PRO ----------------------------------------------------------------------------------
m10 = maze10x10(maze())

q=Qlearn(100,4)
q.train(m10)

