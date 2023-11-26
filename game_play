from cmu_graphics import *
import random
import copy




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
    app.moves=0


def redrawAll(app):
    if app.gameWon==False:
        drawGameState(app,app.carList)
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
    for car in app.carList:
        carLeft,carTop= getCellLeftTop(app, car.row, car.col)
        carWidth, carHeight = getCellSize(app)
        if carLeft<=mouseX<=carLeft+(carWidth*car.dx) and carTop<=mouseY<=carTop+(carHeight*car.dy):
            car.selected=not(car.selected)
        else: 
            car.selected=False

def onKeyPress(app,key):
    if app.gameWon==True:
        if key=='r':
            appBegin(app)
    else:
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


def main():
    runApp()


main()