from cmu_graphics import *
import random
from PIL import Image
import os, pathlib


N = 6

def generateBoard(level):
    #take a board with cars on it, see if its solveable  
    # recquires a certain number of moves to solve for a level
    #only then return the board and carList
    if level=='easy':
       reqdMoves=20
    elif level=='medium':
       reqdMoves=30
    elif level=='continuous':
       reqdMoves=20
    else:
       reqdMoves=40
    while True:
        board, carList = loadBoard()
        moves = solveMyGame(board)
        if moves!=None and reqdMoves<=len(moves)<reqdMoves+10:
           return board, carList
        

class Vehicle:
    #for OOP inspired by https://github.com/CirXe0N/RushHourSolver/blob/master/models/vehicle.py
    def __init__(self, name):
        self.name=name
        self.orientation=''
        self.length=0
        self.startRow=0
        self.startCol=0
        self.endRow=0
        self.endCol=0
        self.dx=1
        self.dy=1
        self.selected=False
        # colorList=['blue','orange','green','pink','yellow','purple']
        colorList=[gradient('tomato', 'salmon', 'peachPuff',start='left'),
                   gradient('salmon', 'peachPuff', 'lemonChiffon',start='left'),
                   gradient('peachPuff', 'lemonChiffon', 'khaki',start='left'),
                   gradient('lemonChiffon', 'khaki', 'greenYellow',start='left'),
                   gradient('khaki', 'greenYellow', 'darkCyan',start='left'),
                   gradient('greenYellow', 'darkCyan', 'mediumTurquoise',start='left'),
                   gradient('darkCyan', 'mediumTurquoise', 'mediumSlateBlue',start='left'),
                   gradient('mediumTurquoise', 'mediumSlateBlue', 'mediumVioletRed',start='left')]
        if name=='Bug':
            self.color=gradient('darkRed', 'fireBrick','crimson',start='left-top')
        else:
            self.color=colorList[random.randint(0,len(colorList)-1)]
    
    def setLocation(self,row,col):
        self.startRow=row
        self.startCol=col
    
    def setPosition(self,endRow,endCol):
        self.endRow=endRow
        self.endCol=endCol
        self.dx=self.endCol-self.startCol+1
        self.dy=self.endRow-self.startRow+1

        if self.dx==1:
            self.length=self.dy
            self.orientation='v'
        else:
            self.length=self.dx
            self.orientation='h'

    def __repr__(self):
        return f'{self.name}, {self.orientation}, {self.length} , {self.startRow}, {self.startCol}'
    

    def moveForward(self):
        if self.orientation == 'h':
            self.startCol += 1
            self.endCol += 1

        if self.orientation == 'v':
            self.startRow += 1
            self.endRow += 1

    def moveBackward(self):
        if self.orientation == 'h':
            self.startCol -= 1
            self.endCol -= 1

        if self.orientation == 'v':
            self.startRow -= 1
            self.endRow -= 1
    
    def getLocations(self):
        occupiedIndices=[]

        if self.orientation=='h':
            delta = self.dx
            for index in range(0, delta + 1):
                location = (self.startRow, self.startCol+index)
                occupiedIndices.append(location)

        if self.orientation=='v':
            delta = self.dy
            for index in range(0, delta + 1):
                location = (self.startRow+index, self.startCol)
                occupiedIndices.append(location)

        self.occupied = occupiedIndices
        return occupiedIndices

            
    def drawCars(self, app): #place cars on the board, same logic as draw cells
        cellLeft, cellTop = getCellLeftTop(app, self.startRow, self.startCol)
        cellWidth, cellHeight = getCellSize(app)
        numberOfCells=self.length
        if self.selected==True: #if click on the car
            drawRect(cellLeft, cellTop, cellWidth*int(self.dx), cellHeight*int(self.dy),
                    fill=self.color, border='antiqueWhite',
                    borderWidth=2, opacity=50)
            drawLabel(self.name.upper(), cellLeft+cellWidth*int(self.dx)/2, cellTop+cellHeight*int(self.dy)/2,
                      fill='black', size=12 )
        else:
            drawRect(cellLeft, cellTop, cellWidth*int(self.dx), cellHeight*int(self.dy),
                    fill=self.color, border='antiqueWhite',
                    borderWidth=2)
            drawLabel(self.name.upper(), cellLeft+cellWidth*int(self.dx)/2, cellTop+cellHeight*int(self.dy)/2,
                      fill='black', size=12 )



def loadBoard():
  #CITATIONS: https://replit.com/@KLde/RushHourTrafficJamSolver#main.py
  #just load a board with cars on it
  carList=[]
  board = [['.'] * 6 for i in range(N)]
  startCol = 0
  board[2][startCol] = board[2][startCol + 1] = 'Bug'
  car=Vehicle('Bug')
  carList.append(car)
  car.setLocation(2,startCol)
  car.setPosition(2, startCol+1)
  attempts = 0
  for i in range(random.randrange(6, 10)):
    carLength = random.randrange(2, 4)
    while True:
      vertical = random.randrange(2) == 0
      row = random.randrange(N - (carLength - 1) * int(vertical))
      col = random.randrange(N - (carLength - 1) * int(not vertical))
      isClear = True
      for j in range(carLength):
        if board[row + j * int(vertical)][col + j * int(not vertical)] != '.':
          isClear = False
          break

      if isClear:
        carName= chr(ord('a' if vertical else 'A') + i)
        car=Vehicle(carName)
        carList.append(car)
        car.setLocation(row,col)
        for j in range(carLength):
          board[row + j * int(vertical)][col + j * int(not vertical)] = carName
          if vertical==True:
            car.setPosition(row+carLength-1, col)
          else:
            car.setPosition(row, col+carLength-1)
        break

      attempts += 1
      if attempts > 1000:
        break

  return board, carList



def boardToString(board):
  return '\n'.join(''.join(_) for _ in board)



def copyBoard(board):
  return [_[:] for _ in board]



  

def isSolved(board):
  # Find any obstacles between the bug and the exit
  # makes the solver a couple steps smaller than checking if bug at last position
  for i in range(N - 1, -1, -1):
    char = board[2][i]
    if char== '.':
      continue
    elif char == 'Bug':
      return True
    else:
      return False

  return True


def getNeighbors(board):
  #CITATIONS: https://replit.com/@KLde/RushHourTrafficJamSolver#main.py
  #generate all possible next board configuarions from the current
  #node generation for BFS

  seenChars = set(['.'])
  neighborBoards = []
  for r in range(N):
    for c in range(N):
      char = board[r][c]
      if char not in seenChars:
        seenChars.add(char)
        drow = 0
        dcol = 0
        if char=='Bug':
          isVertical=False
        else:
          isVertical = not char.isupper()
        if isVertical:
          drow = 1
        else:
          dcol = 1

        #find the start and end row and col for the current car in the board

        startRow, endRow = r, r
        startCol, endCol = c, c
        while startRow - drow >= 0 and startCol - dcol >= 0 and board[startRow - drow][startCol - dcol] == char:
          startRow -= drow
          startCol -= dcol

        while endRow + drow < N and endCol + dcol < N and board[endRow + drow][endCol + dcol] == char:
          endRow += drow
          endCol += dcol

        #make sure move within bounds and isLegal


        if startRow - drow >= 0 and startCol - dcol >= 0 and board[startRow - drow][startCol - dcol] == '.':
          next_state = copyBoard(board)
          next_state[startRow - drow][startCol - dcol] = char
          next_state[endRow][endCol] = '.'
          newMove=[char,-1]
          neighborBoards.append([newMove,next_state])

        if endRow + drow < N and endCol + dcol < N and board[endRow + drow][endCol + dcol] == '.':
          next_state = copyBoard(board)
          next_state[startRow][startCol] = '.'
          next_state[endRow + drow][endCol + dcol] = char
          newMove=[char,1]
          neighborBoards.append((newMove,next_state))
  return neighborBoards


def solveMyGame(board):
    #bfs algo for board Solving

    #CODE CITATIONS: used bfs pseudocode from the TP Guide on pathfinding 
    # https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf

    #used bfs pseudocode from 
    # https://medium.com/swlh/programming-puzzle-rush-hour-traffic-jam-3ee513e6c4ab


  queue = [([], [board])]
  seenConfigurations = set()

  while queue:
    moves, path = queue.pop(0)
    if isSolved(path[-1]):
      return moves
    for newMove, newBoard in getNeighbors(path[-1]):
      if boardToString(newBoard) not in seenConfigurations:
        seenConfigurations.add(boardToString(newBoard))
        queue.append((moves+newMove, path + [newBoard]))

  return None




def isLegalMove(car, moveX,moveY,board ):
    #check nextCell within bounds and is Empty
    if moveX in (-1,1):
        if moveX==1: #if moving right, check immediate right cell is empty and within bounds
            if (car.startCol+car.length-1<5) and (board[car.startRow][car.startCol+car.length]== '.'):
                return True
        else:
            if (car.startCol>0) and (board[car.startRow][car.startCol-1]== '.'):
                return True
    elif moveY in (-1,1):
        if moveY==1:
            if (car.startRow+car.length-1<5) and (board[car.startRow+car.length][car.startCol]== '.') :
                return True
        else:
            if car.startRow>0 and (board[car.startRow-1][car.startCol]== '.'):
                return True
    return False



def onAppStart(app):
    appBegin(app)
    


def drawStartScreen(app):
    #start Screen
    drawImage(app.backgroundImage,0,0)
    drawRect(0,30,app.width,app.height-60,fill='black',opacity=50)
    drawLabel('112-Debugged', app.width/2,app.height/3,size=30, bold=True,fill='antiqueWhite')
    drawRect(app.width/2,app.height/2,60,20,fill='antiqueWhite',align='center')
    drawLabel('PLAY',app.width/2,app.height/2,size=16, fill='black')
    drawRect(app.width/2,app.height*3/4,90,20,fill='antiqueWhite',align='center')
    drawLabel('Instructions',app.width/2,app.height*3/4,size=16, fill='black')

def drawInstructionScreen(app):
    #instruction screen
    drawImage(app.backgroundImage,0,0)
    drawRect(0,30,app.width,app.height-60,fill='black',opacity=50)
    drawLabel('Click on a car to select it' , app.width/2 ,app.height/4 , size=20,fill='antiqueWhite')
    drawLabel('Use the arrow keys to move the car' , app.width/2 ,app.height/4+30 , size=18,fill='antiqueWhite')
    drawLabel('Goal is to get the red car next to the exit' , app.width/2 ,app.height/4+60 , size=18,fill='antiqueWhite')
    drawLabel('Press s to get the solutions' , app.width/2 ,app.height/4+90 , size=18,fill='antiqueWhite')
    drawLabel('Press h to get the next move' , app.width/2 ,app.height/4+120 , size=18,fill='antiqueWhite')
    drawLabel('Speed Run: solve as many boards in 2 mins' , app.width/2 ,app.height/4+150 , size=18,fill='antiqueWhite')
    drawRect(app.width/2,app.height*3/4,90,20,fill='antiqueWhite',align='center')
    drawLabel('Back',app.width/2,app.height*3/4,size=16, fill='black')


def appBegin(app):   
    #wrapper onAppStart
    app.rows = 6
    app.cols = 6
    app.boardLeft = 50
    app.boardTop = 70
    app.boardWidth = app.width-100
    app.boardHeight = app.height-100
    app.cellBorderWidth = 2
    app.level=''
    app.carList=[]
    app.boardList=[]
    app.gameWon=False
    app.startScreen=True
    app.instructionScreen=False
    app.levelScreen=False
    app.gameScreen=False
    app.moves=0
    app.secondsLeft=120
    #solve every puzzle given time
    #updated in onMousePress
    #easy puzzle 45s
    #medium 90s
    #hard 120s
    app.gameLost=False
    app.stepsPerSecond=1
    app.solutionScreen=False
    app.hintScreen=False
    #https://www.pexels.com/photo/motherboard-and-fan-behind-wire-mesh-8108722/
    app.backgroundImage=Image.open("Background.jpg")
    app.backgroundImage = CMUImage(app.backgroundImage)
    app.gameCount=0
   


def redrawAll(app):
    if app.gameScreen==True:
        drawGameState(app)
    elif app.solutionScreen==True:
        solution=solveMyGame(app.boardList)
        drawSolutionScreen(app,solution)
    elif app.hintScreen==True:
        solution=solveMyGame(app.boardList)
        drawHintScreen(app,solution)
    elif app.startScreen==True:
        drawStartScreen(app)
    elif app.instructionScreen==True:
        drawInstructionScreen(app)
    elif app.levelScreen==True:
        drawLevelScreen(app)
    elif app.gameLost==True:
       drawLossState(app)
    else:
        if app.level!='continuous':
            drawWonState(app)
        else: 
           drawContinue(app)

def onStep(app):
   #timer manipulation
   if app.secondsLeft==0:
      #if time runs out, you lose
      app.gameScreen=False
      app.gameLost=True
   elif app.gameScreen==True or app.solutionScreen==True:
      app.secondsLeft-=1

def drawSolutionScreen(app, solutionList):
   #solutions listed out
   drawImage(app.backgroundImage,0,0)
   drawRect(0,30,app.width,app.height-60,fill='black',opacity=50)
   drawLabel('MOVES TO SOLVE', app.width/2,40,fill='antiqueWhite',bold=True,size=20)
   for i in range(0,len(solutionList)-1,2):
      carName=solutionList[i].upper()
      carDir=solutionList[i+1]
      if carDir==1:
         carDir='Forward'
      else:
         carDir='Backward'
      if i<20:
        drawLabel(f'{carName}: {carDir}',app.width/2-50,60+i*10,size=12, fill='antiqueWhite')
      else:
        drawLabel(f'{carName}: {carDir}',app.width/2+50,60+(i-20)*10,size=12, fill='antiqueWhite')
   drawLabel('Press s to go back to the game', app.width/2,app.height-50,size=12, fill='antiqueWhite')

def drawHintScreen(app, solutionList):
   #give next move
   drawImage(app.backgroundImage,0,0)
   drawRect(0,30,app.width,app.height-10,fill='black',opacity=50)
   drawLabel('NEXT MOVE', app.width/2,app.height/2-20,fill='antiqueWhite',bold=True,size=20)
   if len(solutionList)>=1:
      carName=solutionList[0].upper()
      carDir=solutionList[1]
      if carDir==1:
            carDir='Forward'
      else:
            carDir='Backward'
      drawLabel(f'{carName}: {carDir}',app.width/2,app.height/2,size=12, fill='antiqueWhite')
   drawLabel('Press h to go back to the game', app.width/2,app.height/2+50,size=12, fill='antiqueWhite')
      
   
def drawLevelScreen(app):
    #add buttons for levels
    drawImage(app.backgroundImage,0,0)
    for i in range(4):
        drawRect(app.width/2,app.height/5*(i+1),90,20,fill='antiqueWhite',align='center')
    drawLabel('Easy', app.width/2, app.height/5, size=16, fill='black')
    drawLabel('Medium', app.width/2, app.height/5*2, size=16, fill='black')
    drawLabel('Hard', app.width/2, app.height/5*3, size=16, fill='black')
    drawLabel('SpeedRun', app.width/2, app.height/5*4, size=16, fill='black')
    drawRect(app.width/5*4, app.height/5*4,50,20,fill='antiqueWhite',align='center')
    drawLabel('Back', app.width/5*4, app.height/5*4, size=16, fill='black')
        
def drawGameState(app):  
    #draw the game
    drawImage(app.backgroundImage,0,0)
    drawBoard(app)
    for car in app.carList:
        car.drawCars(app)
    drawBoardBorder(app)
    exitX=app.boardLeft+app.boardWidth
    exitY=app.boardTop+(app.boardHeight/app.rows)*2
    drawLine(exitX,exitY,exitX,exitY+(app.boardHeight/app.rows),fill='red',lineWidth=5)
    drawLabel('EXIT',exitX+10,exitY+(app.boardHeight/(2*app.rows)), fill='red', rotateAngle=90)
    drawRect(50,20,70,40,fill=None,border='antiqueWhite')
    drawLabel('Moves', 85,30,size=12,fill='antiqueWhite')
    drawLabel(app.moves,85,45,size=12,fill='antiqueWhite')
    drawRect(280,20,70,40,fill=None,border='antiqueWhite')
    drawLabel('Time Left', 315,30,size=12,fill='antiqueWhite')
    drawLabel(app.secondsLeft,315,45,size=12,fill='antiqueWhite')

def drawWonState(app):
    #if game Won
    drawImage(app.backgroundImage,0,0)
    drawRect(0,30,app.width,app.height-10,fill='black',opacity=50)
    drawLabel(f'You won in {app.moves} moves',app.width/2,app.height/2,size=24,fill='antiqueWhite',bold=True)
    drawLabel('Press r to replay', app.width/2,app.height/2+30,fill='antiqueWhite')

def drawContinue(app):
    #if in continuos mode
    drawImage(app.backgroundImage,0,0)
    drawRect(0,30,app.width,app.height-10,fill='black',opacity=50)
    drawLabel(f'You won {app.gameCount} game(s)',app.width/2,app.height/2,size=24,fill='antiqueWhite',bold=True)
    drawLabel('Press any key to load next Board', app.width/2,app.height/2+30,fill='antiqueWhite')


def drawLossState(app):
    #if gameOver
    drawImage(app.backgroundImage,0,0)
    drawRect(0,30,app.width,app.height-10,fill='black',opacity=50)
    drawLabel(f'Game Over',app.width/2,app.height/2,size=24,fill='antiqueWhite',bold=True)
    drawLabel('Press r to replay', app.width/2,app.height/2+30,fill='antiqueWhite')

def drawBoard(app):
    #from CMU CS Academy: https://academy.cs.cmu.edu/notes/5504

    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='antiqueWhite',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    #draw individual cell
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='antiqueWhite',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    #get cell coordinates
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    #get cell width and height
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)


def onMousePress(app,mouseX,mouseY):
    if app.startScreen==True:
        #if on start page
        if app.width/2-30<=mouseX<=app.width/2+30 and app.height/2-10<=mouseY<=app.height/2+10:
            #if click PLAY
            app.levelScreen=True
            app.startScreen=False
        elif app.width/2-45<=mouseX<=app.width/2+45 and app.height*3/4-10<=mouseY<=app.height*3/4+10:
            #if click Instructions
            app.instructionScreen=True
            app.startScreen=False
    elif app.levelScreen==True:
        #if on level Page
        if app.width/5*4-25<=mouseX<=app.width/5*4+25 and app.height/5*4-10<=mouseY<=app.height/5*4+10:
           #if click BACK
           app.levelScreen=False
           app.startScreen=True
        if app.width/2-45<=mouseX<=app.width/2+45 and app.height/5-10<=mouseY<=app.height/5+10:
            #if click easy
            app.level='easy'
            app.secondsLeft=45
            app.boardList,app.carList=generateBoard(app.level)
            app.gameScreen=True
            app.levelScreen=False
        elif app.width/2-45<=mouseX<=app.width/2+45 and app.height/5*2-10<=mouseY<=app.height/5*2+10:
            #if click medium
            app.level='medium'
            app.secondsLeft=90
            app.boardList,app.carList=generateBoard(app.level)
            app.gameScreen=True
            app.levelScreen=False
        elif app.width/2-45<=mouseX<=app.width/2+45 and app.height/5*3-10<=mouseY<=app.height/5*3+10:
            #if click hard
            app.level='hard'
            app.secondsLeft=120
            app.boardList,app.carList=generateBoard(app.level)
            app.gameScreen=True
            app.levelScreen=False
        elif app.width/2-45<=mouseX<=app.width/2+45 and app.height/5*4-10<=mouseY<=app.height/5*4+10:
           #if click speed Run
           app.level='continuous'
           app.secondsLeft=120
           app.boardList,app.carList=generateBoard(app.level)
           app.gameCount+=1
           app.gameScreen=True
           app.levelScreen=False
    elif app.instructionScreen==True:
        #if on instruction page click BACK
        if app.width/2-45<=mouseX<=app.width/2+45 and app.height*3/4-10<=mouseY<=app.height*3/4+10:
            app.instructionScreen=False
            app.startScreen=True
    elif app.gameScreen==True:
        #if playing game
        for car in app.carList:
            #if click within a car not(select) it
            #if click anywhere else unselect current selection
            carLeft,carTop= getCellLeftTop(app, car.startRow, car.startCol)
            carWidth, carHeight = getCellSize(app)
            if carLeft<=mouseX<=carLeft+(carWidth*car.dx) and carTop<=mouseY<=carTop+(carHeight*car.dy):
                car.selected=not(car.selected)
            else: 
                car.selected=False

def onKeyPress(app,key):
    if app.gameWon==True and app.level=='continuous':
      #press any key to continue when mode=SpeedRun
      app.moves=0
      app.boardList,app.carList=generateBoard(app.level)
      app.gameCount+=1
      app.gameScreen=True
      app.gameWon=False
    if key=='r':
        #replay
        if app.gameWon==True or app.gameScreen==True or app.gameLost==True:
          appBegin(app)
    elif app.gameScreen==True or app.solutionScreen==True or app.hintScreen==True:
        if key=='s':
            #solution
            #solution=solveMyGame(app.boardList)
            app.solutionScreen=not app.solutionScreen
            if app.solutionScreen==True:
               app.gameScreen=False
            else:
               app.gameScreen=True
        if key=='h':
           #hint Generator
           app.hintScreen=not app.hintScreen
           if app.hintScreen==True:
              app.gameScreen=False
           else:
              app.gameScreen=True
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
                if isLegalMove(car, dx ,dy,app.boardList):
                    car.startRow+=dy
                    car.startCol+=dx
                    app.moves+=1
                    carList=app.carList
                    app.boardList=unpack(app,carList)
                    if car.name=='Bug' and car.startCol==4:
                        app.gameWon=True
                        app.gameScreen=False

def unpack(app,carList):
    #go from the coordinate list of cars to a 2D board repr
    board=[]
    for row in range(app.rows):
        rowList=[]
        for col in range(app.cols):
            rowList.append('.')
        board.append(rowList)
    for car in carList:
        for row in range(car.dy):
            for col in range(car.dx):
                board[car.startRow+row][car.startCol+col]=car.name
    return board
    
def main():
    runApp()
    


main()