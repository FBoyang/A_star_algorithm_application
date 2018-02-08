import numpy as np
from ezgraphics import GraphicsWindow


# Make the grid, having the top left and bottom right block set to unblocked and seen
def setup():
    grid = makeGrid()
    for i in range(101):
        for j in range(101):
            # Initialize each object
            if (i == 0 and j == 0) or (i == 100 and j == 100):
                grid[i][j] = Cell(i, j, False, True)
            else:
                grid[i][j] = Cell(i, j, randomization())
    return grid


# Return false for unblocked, true for blocked
def randomization():
    temp = np.random.choice([0, 1], 1, p=[0.3, 0.7])
    if temp[0] == 1:
        return False
    return True


# making a grid as [101][101]
def makeGrid():
    grid = [[0 for x in range(101)] for y in range(101)]
    return grid


def draw(windowSize=550, off=5):
    win = GraphicsWindow(windowSize, windowSize)
    canvas = win.canvas()
    offset_x = off  # Distance from left edge.
    offset_y = off  # Distance from top.
    cell_size = off  # Height and width of checkerboard squares.

    grid = setup()

    for i in range(101):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(101):  # So does j.
            cell = grid[i][j]
            if not cell.ifBlocked:
                color = 'white'
            else:
                color = 'black'

            # if i == 0 and j == 0:
            #     color = 'red'
            canvas.setFill(color)
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


draw()