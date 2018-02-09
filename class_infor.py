class Cell:
    def __init__(self, xPos, yPos, if_blocked, ifVisited=False):
        self.x = xPos
        self.y = yPos
        self.ifBlocked = if_blocked
        self.visited = ifVisited

    def visit(self):
        self.visited = True

'''
this is the data type of each cell, which store the information of the location,
f value, h value, and indirectly store the g value, an boolean value determine whether
the cell is fully expanded or not
'''

class node:
	def __init__(self, xcoor, ycoor, f, h):
		self.x = xcoor
		self.y = ycoor
		self.f = f
		self.h = h
		self.ifExpanded = False

	def __lt__(self, other):
		#define a new rule to make comparison based on the g value of two cells
		return self.f - self.h < other.f - other.h

	def __eq__(self, other):
		return self.f - self.h < other.f - other.h


