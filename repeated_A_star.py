import numpy as np
from ezgraphics import GraphicsWindow
import sys


size = 31
#initialize the information matrix
def setup_info():
	grid = makeGrid()
	grid[0][0] = node(0, 0, (size - 1) * 2, (size - 1) * 2)
	grid[size - 1][size - 1] = node(size - 1, size -1, sys.maxint, 0)

#update the information matrix
def update_info():



# Make the grid, having the top left and bottom right block set to unblocked and seen
def setup():
    grid = makeGrid()
    for i in range(size):
        for j in range(size):
            # Initialize each object
            if (i == 0 and j == 0) or (i == size - 1 and j == size -1):
                #Cell(x coor, y coor, if_blocked, if_visited)
                grid[i][j] = Cell(i, j, False, True)
            else:
                grid[i][j] = Cell(i, j, randomization())
    return grid


# Return false for unblocked, true for blocked
def randomization():
    temp = np.random.choice([0, 1], 1, p=[0.2, 0.8])
    if temp[0] == 1:
        return False
    return True


# making a grid as [101][101]
def makeGrid():
    grid = [[0 for x in range(size)] for y in range(size)]
    return grid


def draw(windowSize=size * 50, off=50):
    win = GraphicsWindow(windowSize, windowSize)
    canvas = win.canvas()
    offset_x = off  # Distance from left edge.
    offset_y = off  # Distance from top.
    cell_size = off  # Height and width of checkerboard squares.

    grid = setup()
    #start

    for i in range(size):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(size):  # So does j.
            cell = grid[i][j]
            if not cell.ifBlocked:
                color = 'white'
            else:
                color = 'black'

            # if i == 0 and j == 0:
            #     color = 'red'
            canvas.setFill(color)
            #draw cell_size * cell_size rectangle at point (offset_x + i * cell_size, offset_y + j * cell_size) 
            canvas.drawRect(offset_x + i * cell_size, offset_y + j * cell_size,
                            cell_size, cell_size)
    win.wait()





#draw()




#generate a random foggy map
map_foggy = setup()

#generate a information map
map_info = setup_info()

#



