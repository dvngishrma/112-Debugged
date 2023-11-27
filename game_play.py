from cmu_graphics import *
import random
import copy
# from game_solver import *




carCoords=[['A','v',2,1,2],
            ['B','v',3,1,4],
            ['C','v',2,2,5],
            ['D','h',3,3,0],
            ['E','v',2,4,0],
            ['F','v',2,4,1],
            ['G','v',2,4,2],
            ['H','h',2,4,4],
            ['I','h',2,5,4],
            ['Bug','h',2,2,0]]


#easy to create the pieces and place them on the board, easy to update row col and move pieces around, solution generator might take some thinky thinky

#use 2 methods to represent the board, one with the cars and coordinates used to initialise the vehicle class
#second method 2-D list with all the positions mapped
#might want to switch between the two formats, depending on what functionality im using?

                
class Vehicle:
    def __init__(self, name, orient, length, row, col):
        self.name=name
        self.orientation=orient
        self.length=length
        self.row=row
        self.col=col
        
        if self.orientation=='h':
            self.dx=length
            self.dy=1
        else:
            self.dy=length
            self.dx=1
        self.selected=False
        colorList=['blue','orange','green','pink','yellow','purple']
        if name=='Bug':
            self.color='red'
        else:
            self.color=colorList[random.randint(0,len(colorList)-1)]
            
    def drawCars(self, app): #place cars on the board, same logic as draw cells
        cellLeft, cellTop = getCellLeftTop(app, self.row, self.col)
        cellWidth, cellHeight = getCellSize(app)
        numberOfCells=self.length
        if self.selected==True: #if click on the car
            drawRect(cellLeft, cellTop, cellWidth*self.dx, cellHeight*self.dy,
                    fill=self.color, border='white',
                    borderWidth=app.cellBorderWidth, opacity=50)
        else:
            drawRect(cellLeft, cellTop, cellWidth*self.dx, cellHeight*self.dy,
                    fill=self.color, border='black',
                    borderWidth=app.cellBorderWidth)
            
            


def unpack(app,carList):
    #go from the coordinate list of cars to a 2D board repr
    board=[]
    for row in range(app.rows):
        rowList=[]
        for col in range(app.cols):
            rowList.append(None)
        board.append(rowList)
    for car in carList:
        for row in range(car.dy):
            for col in range(car.dx):
                board[car.row+row][car.col+col]=car.name
    return board

def onAppStart(app):
    appBegin(app)
    

def drawStartScreen(app):
    drawRect(0,0,app.width,app.height,fill='lightBlue')
    drawLabel('112-Debugged', app.width/2,app.height/3,size=30, bold=True)
    drawRect(app.width/2,app.height/2,60,20,fill='black',align='center')
    drawLabel('PLAY',app.width/2,app.height/2,size=16, fill='white')
    drawRect(app.width/2,app.height*3/4,90,20,fill='black',align='center')
    drawLabel('instructions',app.width/2,app.height*3/4,size=16, fill='white')

def drawInstructionScreen(app):
    drawRect(0,0,app.width,app.height,fill='lightBlue')
    drawLabel('Click on a car to select it' , app.width/2 ,app.height/2 , size=20)
    drawLabel('Use the arrow keys to move the car' , app.width/2 ,app.height/2+30 , size=20)
    drawLabel('Goal is to get the red car next to the exit row' , app.width/2 ,app.height/2+60 , size=20)
    drawRect(app.width/2,app.height*3/4,90,20,fill='black',align='center')
    drawLabel('Back',app.width/2,app.height*3/4,size=16, fill='white')


def appBegin(app):   
    app.rows = 6
    app.cols = 6
    app.boardLeft = 50
    app.boardTop = 70
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.carList=[]
    for cars in carCoords:
        app.carList.append(Vehicle(cars[0],cars[1],cars[2],cars[3],cars[4]))
    app.boardList=unpack(app,app.carList)
    app.gameWon=False
    app.startScreen=True
    app.instructionScreen=False
    app.gameScreen=False
    app.moves=0


def redrawAll(app):
    if app.gameScreen==True:
        drawGameState(app,app.carList)
    elif app.startScreen==True:
        drawStartScreen(app)
    elif app.instructionScreen==True:
        drawInstructionScreen(app)
    else:
        drawWonState(app)
        
def drawGameState(app,cars):  
    drawBoard(app)
    for car in cars:
        car.drawCars(app)
    drawBoardBorder(app)
    exitX=app.boardLeft+app.boardWidth
    exitY=app.boardTop+(app.boardHeight/app.rows)*2
    drawLine(exitX,exitY,exitX,exitY+(app.boardHeight/app.rows),fill='white',lineWidth=10)
    drawLabel('EXIT',exitX+10,exitY+(app.boardHeight/(2*app.rows)), fill='red', rotateAngle=90)
    drawRect(50,20,70,40,fill=None,border='black')
    drawLabel('Moves', 85,30,size=12)
    drawLabel(app.moves,85,45,size=12)

def drawWonState(app):
    drawRect(0,0,app.width,app.height,fill='lightBlue')
    drawLabel(f'You won in {app.moves} moves',app.width/2,app.height/2,size=24)
    drawLabel('press r to replay', app.width/2,app.height/2+30)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)


def onMousePress(app,mouseX,mouseY):
    if app.startScreen==True:
        if 170<=mouseX<=230 and 190<=mouseY<=210:
            app.gameScreen=True
            app.startScreen=False
        elif 155<=mouseX<=245 and 290<=mouseY<=310:
            app.instructionScreen=True
            app.startScreen=False
    elif app.instructionScreen==True:
        if 155<=mouseX<=245 and 290<=mouseY<=310:
            app.instructionScreen=False
            app.startScreen=True
    for car in app.carList:
        carLeft,carTop= getCellLeftTop(app, car.row, car.col)
        carWidth, carHeight = getCellSize(app)
        if carLeft<=mouseX<=carLeft+(carWidth*car.dx) and carTop<=mouseY<=carTop+(carHeight*car.dy):
            car.selected=not(car.selected)
        else: 
            car.selected=False

def onKeyPress(app,key):
    # if key=='s':
    #     solution=solveMyGame(app,copy.deepcopy(app.boardList))
    #     print(solution)
    if app.gameWon==True:
        if key=='r':
            appBegin(app)
    elif app.gameScreen==True:
        for car in app.carList:
            if car.selected==True:
                if car.orientation=='h':
                    if key=='right':
                        dx=1
                        dy=0
                    elif key=='left':
                        dx=-1
                        dy=0
                    else:
                        dx=0
                        dy=0
                elif car.orientation=='v':
                    if key=='down':
                        dx=0
                        dy=1
                    elif key=='up':
                        dx=0
                        dy=-1
                    else:
                        dx=0
                        dy=0
                if isLegalMove(app,car, dx ,dy):
                    car.row+=dy
                    car.col+=dx
                    app.moves+=1
                    app.boardList=unpack(app,app.carList)
                    if car.name=='Bug' and car.col==4:
                        app.gameWon=True
                        app.gameScreen=False
    

def isLegalMove(app, car, moveX,moveY ):
    board=app.boardList
    if moveX in (-1,1):
        if moveX==1: #if moving right, check immediate right cell is empty and within bounds
            if (car.col+car.length-1<app.cols-1) and (board[car.row][car.col+car.length]== None):
                return True
        else:
            if (car.col>0) and (board[car.row][car.col-1]== None):
                return True
    elif moveY in (-1,1):
        if moveY==1:
            if (car.row+car.length-1<app.rows-1) and (board[car.row+car.length][car.col]== None) :
                return True
        else:
            if car.row>0 and (board[car.row-1][car.col]== None):
                return True
    elif moveX==0 and moveY==0:
        return True
    return False

# def solveMyGame(board,app,carList):
#     if board[2][4]=='Bug' and board[2][5]=='Bug' :
#         #base case: 'bug' car is in last two cols of third row 
#         return []
#     else:
#         for i in range(len(carList)):
#             car=carList[i]
#             for move in (-1,1):
#                 if car.orientation=='h':
#                     if isLegalMove(app,car,move,0):
#                         car.col+=move
#                         board=unpack(app,carList)
#                         print(f'tadaa = {board}')
#                         solution= solveMyGame(board,app,carList)
#                         if solution!= None:
#                             return [(car.name, move)]+ solution 
#                         car.col-=move
#                         board=unpack(app,carList)
#                 else:
#                     if isLegalMove(app,car,0,move):
#                         car.row+=move
#                         board=unpack(app,carList)
#                         print(f'newboard = {board}')
#                         solution=solveMyGame(board,app,carList)
#                         if solution!= None:
#                             return [(car.name, move)]+ solution 
#                         car.row-=move
#                         board=unpack(app,carList)               
#         return None

#dfs will not work 
#start by implementing bfs and then work to optimise to potentially A*
    
    #create a set of all seen before boards
        # def bfs_search(start_state, goal_state):
        #     queue = [[start_state]]
        #     seen_states = set()
        #     while queue:
        #         path = queue.pop(0)
        #         if path[-1] == goal_state:
        #         return True
        #         for next_state in get_next_states(path[-1]):
        #         if next_state not in seen_states:
        #             seen_states.add(next_state)
        #             queue.append(path + [next_state])
        #     return False
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

def main():
    runApp()


main()