def maze4x4(m):
    e=m.env
    e[3,3]=1
    e[0,1:3]=-1
    e[1,2]=4
    e[3,1]=4
    e[2,1]=-1
    m.flagcount=2
    m.flagcount0 = 2
    return m

def maze10x10(m):
    e=m.env
    #goal
    e[9,9] = 1
    #flags
    e[1,3] ,e[2,1] ,e[2,6] ,e[4,1] ,e[4,5] ,e[7,1] ,e[9,8] = 4,4,4,4,4,4,4
    #walls
    e[0,1] ,e[1,5] ,e[2,5] ,e[3,0:2] = -1, -1, -1, -1
    e[3,3:5] , e[3,6] , e[4,2] , e[4,4] = -1, -1, -1, -1
    e[4,6:9] , e[5,2] , e[5,4] , e[7,6:10] = -1, -1, -1, -1
    e[8,1:6] , e[9,7] = -1 , -1
    # count of flags
    m.flagcount= 7
    m.flagcount0= 7
    return m