import time
start = time.process_time()


def createStateArr(s:str):
    return list(map(lambda x: int(x),s.split(" ")))
def getStateString(s):
    return ' '.join(map(lambda x: str(x), s))
def compareStates(s1, s2):
    return getStateString(s1) == getStateString(s2)

def checkCompletion(s):
    return compareStates(s, end_state)


initial_state = createStateArr("2 4 5 7 8 3 1 11 14 6 10 12 9 13 0 15")
# initial_state = createStateArr("1 2 3 4 5 6 7 8 0 10 11 12 9 13 14 15")
# initial_state = createStateArr("1 2 3 4 5 6 7 8 10 0 11 12 9 13 14 15")
end_state = createStateArr("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0")


LEFT, RIGHT, UP, DOWN = "LEFT RIGHT UP DOWN".split(" ")




def printItStr(state):
    s = ""
    for i in range(4):
        s+=(' '.join(map(lambda x: str(x).rjust(3, " "), state[i*4:i*4+4])))
        if i != 3:
            s += "\n"
    s += ""
    return s

def printIt(state):
    print(printItStr(state))

def get2dPos(indx):
    return [indx//4, indx%4]
def get1dPos(x,y):
    return x*4+y

def getPossibleMoves(state):
    indx = state.index(0)
    x,y = get2dPos(indx)
    possible_moves = []
    if x>0: possible_moves.append(UP)
    if x<3: possible_moves.append(DOWN)
    if y>0: possible_moves.append(LEFT)
    if y<3: possible_moves.append(RIGHT) 
    return possible_moves

def makeMove(state, move):
    nstate = [*state]
    zeroIndx = state.index(0)
    zx,zy = get2dPos(zeroIndx)
    nzx, nzy = zx, zy
    if move == UP: nzx = zx-1
    if move == DOWN: nzx = zx+1
    if move == LEFT: nzy = zy-1
    if move == RIGHT: nzy = zy+1
    nzpos = get1dPos(nzx, nzy)
    nstate[zeroIndx] = nstate[nzpos]
    nstate[nzpos] = 0
    return nstate

def getManhattan(state):
    sm = 0
    for v in state:
        a,b = get2dPos(end_state.index(v))
        c,d = get2dPos(state.index(v))
        # print((a,b), (c,d), abs(a-c)+abs(b-d))
        sm += abs(a-c)+abs(b-d)
    return sm


class Node:
    def __init__(self, state, parent=None, depth=1, statepath=[], isExplored=False, MAX_DEPTH=1):
        self.state = state
        self.stateString = getStateString(self.state)
        self.parent = parent
        self.childNodes = []
        self.depth = depth
        self.manhattan = getManhattan(self.state)
        self.cost = self.manhattan + self.depth
        self.solved = False
        self.explored = isExplored
        self.statepath = statepath
        self.MAX_DEPTH=MAX_DEPTH
    def isSolved(self):
        return checkCompletion(self.state)
    def setExplored(self):
        self.explored = True
    def expand(self):
        expandableMoves = getPossibleMoves(self.state)
        childNodes = []
        for v in  expandableMoves:
            nstate = makeMove(self.state, v)
            stateStr = getStateString(nstate)
            if stateStr in self.statepath:
                continue
            if self.depth > self.MAX_DEPTH:
                continue
            # setIsExplored = (stateStr in self.statepath) or (self.depth>MAX_DEPTH)
            setIsExplored = False
            # print(self.statepath)
            nnode = Node(nstate, parent=self, depth=self.depth+1, statepath=self.statepath+[stateStr], isExplored=setIsExplored, MAX_DEPTH=self.MAX_DEPTH)
            childNodes.append(nnode)
        childNodes.sort(key=lambda x:x.cost)
        self.childNodes = childNodes
        return childNodes
    def setSolved(self):
        self.solved = True
        if self.parent:
            self.parent.setSolved()
    def __repr__(self):
        sstr = printItStr(self.state)
        
        return f"\n\n<state=\n{sstr}\ndepth={self.depth}\ncost={self.cost}\n>\n\n"
    

ITERATION_LIMIT = 2**128
MAX_DEPTH = 2**32

r = range(MAX_DEPTH, MAX_DEPTH+1)

tot_itr = 0
def solve(initial_statem, MAX_DEPTH):
    global tot_itr
    
    inode = Node(initial_state, MAX_DEPTH=MAX_DEPTH)
    # print(inode)
    inode.expand()

    child_nodes_stack = [*inode.childNodes]

    k = -1
    while not inode.isSolved() and k < ITERATION_LIMIT:
        tot_itr += 1
        k+=1
        if child_nodes_stack and not child_nodes_stack[0].explored:
            inode = child_nodes_stack[0]
            inode.setExplored()
            child_nodes_stack = [*inode.expand()]
            # print(inode, 'w')
        else:
            if child_nodes_stack:
                child_nodes_stack.pop(0)
            else:
                if inode.parent:
                    inode = inode.parent
                    child_nodes_stack = [*inode.childNodes]
                    child_nodes_stack = list(filter(lambda x:not x.explored, child_nodes_stack))
                else:
                    break
    

        pass
    
    if inode.isSolved():
        return [True, inode, k]
    else:
        return [False]
    # # print("SOLVED" if  else "ITERATION LIMIT")
    # if inode.isSolved():
    #     print("SOLVED")
    #     print(dict(k = k))
    #     path = []
    #     x = inode
    #     while x:
    #         path += [x.state]
    #         x = x.parent
    #     path.reverse()
    #     for p in path:
    #         print(Node(p))
    #     # print(f"depth = {inode.depth}")


    
    return


for i in r:
    sln = solve(initial_state, i)
    if sln[0]:
        s = sln[1]
        path = []
        x = s
        while x:
            path += [x.state]
            x = x.parent
        path.reverse()
        # for p in path:
        #     print()
        #     print(printItStr(p))
        #     print()
        print("QUEST: ", printItStr(initial_state), sep="\n")
        print(f"SOLVED IN:  {len(path)-1} steps")
        print("MAX ITERATIONS: ",ITERATION_LIMIT)
        print("MAX DEPTH SET: ", MAX_DEPTH)
        print("END STATE REACH CHECK: ", printItStr(path[-1]), sep="\n")
        print()
        
        break
    else:
        print("INCREASIN ITR", i)





print("TIME TAKEN FOR SIMULATION: ", time.process_time() - start, "seconds")