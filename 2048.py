from tkinter import *
import random
import math

def keyPressed(event):
    if canvas.data.gameOver == False:
        if event.keysym == 'Down':
            moveDown()
            mergeDown()
            moveDown()
        if event.keysym == 'Left':
            moveLeft()
            mergeLeft()
            moveLeft()
        if event.keysym == "Right":
            moveRight()
            mergeRight()            
            moveRight()
        if event.keysym == 'Up':
            moveUp()
            mergeUp()
            moveUp()
    hasReached2048()
    # if isOver() == True:
    #     canvas.data.gamaOver = True
    if canvas.data.win == False:
        newPiece()
    if event.keysym == 'r':
        canvas.delete(ALL)
        init()
        timerFired()
    redrawAll()

####################
# keyboard control
####################
def moveLeft():
    height = len(canvas.data.board)
    width = len(canvas.data.board[0])
    board = canvas.data.board
    for i in range(height):
        for j in range(width-1, -1, -1):
            k = j
            while k - 1 >= 0 and board[i][k-1] == 0:
                temp = board[i][k]
                board[i][k] = board[i][k-1]
                board[i][k-1] = temp
                k -= 1
    canvas.data.board = board   

def moveRight():
    height = len(canvas.data.board)
    width = len(canvas.data.board[0])
    board = canvas.data.board
    for i in range(height):
        for j in range(width):
            k = j
            count = 0
            while k + 1 < width and board[i][k+1] == 0:
                temp = board[i][k]
                board[i][k] = board[i][k+1]
                board[i][k+1] = temp
                k += 1
                count += 1
    canvas.data.board = board

def moveUp():
    board = canvas.data.board
    canvas.data.board = transpose(board)
    moveLeft()
    canvas.data.board = transpose(canvas.data.board)


def moveDown():
    board = canvas.data.board
    canvas.data.board = transpose(board)
    moveRight()
    canvas.data.board = transpose(canvas.data.board)

def transpose(arr):
    result = [([0] * len(arr[0])) for i in range(len(arr))]
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            result[i][j] = arr[j][i]
    return result
#########################
#########################

def hasReached2048():
    # if you get to 2048 you win the game
    for i in range(len(canvas.data.board)):
        if 2048 in canvas.data.board[i]:
            canvas.data.win = True

def isOver():
    board = canvas.data.board
    for i in range(len(board)):
        for j in range(len(board[0])):
            if canMove(i, j):
                return False
    return True

def canMove(i, j):
    # check if the pieces around the element at i, j is the same as the element
    board = canvas.data.board
    result = [True, True, True, True]
    if i - 1 < 0:
        result[0] = False
    elif board[i-1][j] != board[i][j]:
        result[0] = False
    if i == len(board) - 1:
        result[1] = False
    elif board[i+1][j] != board[i][j]:
        result[1] = False
    if j - 1 < 0:
        result[2] = False
    elif board[i][j-1] != board[i][j]:
        result[2] = False
    if j == len(board[0]) - 1:
        result[3] = False
    elif board[i][j+1] != board[i][j]:
        result[3] = False
    if True not in result:
        return False
    return True

def newPiece():
    board = canvas.data.board
    height = len(canvas.data.board)
    width = len(canvas.data.board[0])
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    while (board[x][y] != 0):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
    num = random.randint(1, 2)
    canvas.data.board[x][y] = num * 2

##############
# merge
##############
def mergeLeft():
    board = canvas.data.board
    height = len(canvas.data.board)
    width = len(canvas.data.board[0])
    for i in range(height):
        for j in range(width - 1):
            if (board[i][j] == board[i][j+1]):
                board[i][j] += board[i][j]
                board[i][j+1] = 0
    canvas.data.board = board

def mergeRight():
    board = canvas.data.board
    height = len(canvas.data.board)
    width = len(canvas.data.board[0])
    for i in range(height):
        for j in range(width-1, -1, -1):
            if board[i][j] == board[i][j-1]:
                board[i][j] += board[i][j]
                board[i][j-1] = 0
    canvas.data.board = board

def mergeDown(): 
    board = canvas.data.board
    height = len(canvas.data.board)
    width = len(canvas.data.board[0])
    canvas.data.board = transpose(board)
    mergeRight()
    canvas.data.board = transpose(canvas.data.board)

def mergeUp():
    board = canvas.data.board
    height = len(canvas.data.board)
    width = len(canvas.data.board[0])
    canvas.data.board = transpose(board)
    mergeLeft()
    canvas.data.board = transpose(canvas.data.board)
###########################
###########################


################
# draw the board
################
def drawCell(row, col, color): 
    # draw outter rectangle
    x1 = canvas.data.margin + col * canvas.data.cellSize
    y1 = canvas.data.upperMargin + row * canvas.data.cellSize
    x2 = x1 + canvas.data.cellSize
    y2 = y1 + canvas.data.cellSize

    # draw inner rectangle
    x3 = x1 + canvas.data.cellMargin
    y3 = y1 + canvas.data.cellMargin
    x4 = x2 - canvas.data.cellMargin
    y4 = y2 - canvas.data.cellMargin

    canvas.create_rectangle(x1, y1, x2, y2)
    canvas.create_rectangle(x3, y3, x4, y4, fill = color)
    canvas.create_text(80, 20, text='Press \'r\' to restart')

    # draw the number
    if canvas.data.board[row][col] is not 0:
        xCenter = x1 + canvas.data.cellSize // 2
        yCenter = y1 + canvas.data.cellSize // 2
        canvas.create_text(xCenter, yCenter, 
            text = str(canvas.data.board[row][col]), font = "Belvetica 16 bold")    

def drawBoard():
    for i in range(canvas.data.rows):
        for j in range(canvas.data.cols):
            if canvas.data.board[i][j] == 0:
                color = '#cdc1b4'
            else:
                num = int(math.log2(canvas.data.board[i][j]))
                color = canvas.data.pieces[num - 1]
            drawCell(i, j, color)

def drawWinningPage():
    drawBoard()
    canvas.create_text(canvas.data.canvasWidth // 2, 
        canvas.data.canvasHeight // 2, text="YOU WIN!")
    canvas.create_text(canvas.data.canvasWidth // 2 - 5, 
        canvas.data.canvasHeight + 10, text='Press \'r\' to restart')

def drawGameOver():
    drawBoard()
    canvas.create_text(canvas.data.canvasWidth // 2, 
        canvas.data.canvasHeight // 2, text="DEAD END!")
    canvas.create_text(canvas.data.canvasWidth // 2 - 5, 
        canvas.data.canvasHeight + 10, text='Press \'r\' to restart')
####################
def timerFired():
    if canvas.data.gameOver:
        drawGameOver()
        return
    elif canvas.data.win:
        drawWinningPage()
        return
    drawBoard()
    redrawAll()
    delay = canvas.data.delayTime
    canvas.after(delay, timerFired)

def redrawAll():
    if canvas.data.gameOver == True:
        drawGameOver()
        return
    if canvas.data.win == True:
        drawWinningPage()
        return
    else:
        canvas.delete(ALL)
        drawBoard()
####################
def init():
    ## initialize different pieces
    piece2 = '#eee4da'
    piece4 = '#ede0c8'
    piece8 = '#f2b179'
    piece16 = '#f59563'
    piece32 = '#f67c5f'
    piece64 = '#f65e3b'
    piece128 = '#edcf72'
    piece256 = '#edcc61'
    piece512 = '#edc850'
    piece1024 = '#edc53f'
    piece2048 = '#edc22e'

    rows = canvas.data.rows
    cols = canvas.data.cols
    x1 = random.randint(0, 3)
    y1 = random.randint(0, 3)
    x2 = random.randint(0, 3)
    y2 = random.randint(0, 3)
    firstPiece = random.randint(1, 2)
    secondPiece = random.randint(1, 2)
    while x1 == x2 and y1 == y2:
        x2 = random.randint(0, rows-1)
        y2 = random.randint(0, cols-1)
    canvas.data.pieces = [piece2, piece4, piece8, piece16, piece32, piece64,
        piece128, piece256, piece512, piece1024, piece2048]
    canvas.data.board = [([0] * cols) for i in range(rows)]
    canvas.data.board[x1][y1] = firstPiece * 2
    canvas.data.board[x2][y2] = secondPiece * 2
    canvas.data.delayTime = 300
    canvas.data.gameOver = False
    canvas.data.win = False

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    rows = 4
    cols = 4
    margin = 25
    upperMargin = 50
    cellSize = 100
    canvasWidth = 2 * margin + cols * cellSize
    canvasHeight = upperMargin + margin + rows * cellSize
    canvas = Canvas(root, width = canvasWidth, height = canvasHeight)
    canvas.pack()
    # make the window non-resizable
    root.resizable(width = 0, height = 0)

    # set up canvas data and call init()
    class Struct(): pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.margin = margin
    canvas.data.upperMargin = upperMargin
    canvas.data.cellSize = cellSize
    canvas.data.cellMargin = 2
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight    

    # setup event
    init()
    root.bind("<Key>", keyPressed)
    # launch the app
    timerFired()
    # This call BLOCKS (so your program waits until you close the window!)
    root.mainloop()

run()