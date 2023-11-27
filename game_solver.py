from cmu_graphics import *
from game_play import *
#solver for rush hour:

#load current board,
#loop over all the cars in the board and find if they are moveable,
#move each of them and store it as a neighbour state
#find a way to list the path you take 
#maybe sth like [new game state, next step made]
#bfs
#if solution found then return the steps list 
#nodal search on the graph 
#lastly return None


#for board generation:
#place the 'bug' at the rightmost on the third row,
#place cars A-I in the board wherever possible randomly
#shuffle them around by selecting one car at random and making one random move 
#set difficulty by putting an upper bound on the number of moves,
#if number of moves not reachable regenerate? until you reach the move counrt and intitalise it as your first state.

#maybe save the states so it can be used as the solver too??

#eventually try adding cutouts(blocks) into the board, maybe as part of another level

def solveMyGame(app,board):
    boardQueue=[(0, board)]
    seenConfigurations=set()
    seenConfigurations.add(boardListToString(board))
    mapping={}
    mapping[boardListToString(board)]=None
    while boardQueue!=[]:
        configNum, currentBoard = boardQueue.pop(0)
        print(configNum)
        if currentBoard[2][5] =='Bug':
            print('i reach here')
            resultList=[]
            node=boardListToString(currentBoard)
            for key in mapping:
                if key==node:
                    resultList.insert(0,mapping[key])
                    node=mapping[key]
                    if node==None:
                        return resultList
                    continue
        for nextConfig in getNeighbour(app,currentBoard):
            if boardListToString(nextConfig) not in seenConfigurations:
                print('i got here')
                seenConfigurations.add(boardListToString(nextConfig))
                boardQueue.append((configNum+1, nextConfig))
                print(len(boardQueue))
                mapping[boardListToString(nextConfig)] = currentBoard
    return None

def getNeighbour(app,board): #working!!!! yayyy!!!


    #loop through all the cars in the board
    #move each one thats moveable
    #append this into a list
    #return to board config
    #continue loop
    #return list


    neighbourStates=[]
    for i in range(len(app.carList)):
            car=app.carList[i]
            for move in (-1,1):
                if car.orientation=='h':
                    if isLegalMove(app,car,move,0):
                        car.col+=move
                        newBoard=unpack(app,app.carList)
                        neighbourStates.append(newBoard)
                        car.col-=move
                else:
                    if isLegalMove(app,car,0,move):
                        car.row+=move
                        newBoard=unpack(app,app.carList)
                        neighbourStates.append(newBoard)
                        car.row-=move
    return neighbourStates

def boardListToString(board):
    result=''
    for row in range(len(board)):
        rowstr=''
        for col in range(len(board)):
            rowstr+=str(board[row][col])+' '
        result+=rowstr+'\n'
    return result
