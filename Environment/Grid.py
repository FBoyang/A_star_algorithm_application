import numpy as np
from ezgraphics import GraphicsWindow


# Make the grid, having the top left and bottom right block set to unblocked and seen
def setup():
    grid = makeGrid()
    for i in range(31):
        for j in range(31):
            # Initialize each object
            if (i == 0 and j == 0) or (i == 30 and j == 30):
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
    grid = [[0 for x in range(31)] for y in range(31)]
    return grid


def draw(windowSize=1050, off=50):
    win = GraphicsWindow(windowSize, windowSize)
    canvas = win.canvas()
    offset_x = off  # Distance from left edge.
    offset_y = off  # Distance from top.
    cell_size = off  # Height and width of checkerboard squares.

    grid = setup()
    #start

    for i in range(31):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(31):  # So does j.
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


class Cell:
    def __init__(self, xPos, yPos, if_blocked, ifVisited=False):
        self.x = xPos
        self.y = yPos
        self.ifBlocked = if_blocked
        self.visited = ifVisited

    def visit(self):
        self.ifVisited = True


#draw()
