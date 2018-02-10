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
g value, h value, and indirectly store the f value, an boolean value determine whether
the cell is fully expanded or not
'''

class node:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.h = 0
		self.g = 0
		self.search = 0
		self.parent = None
		self.isBlocked = False


	def __lt__(self, other):
		#define a new rule to make comparison based on the f value of two cells
		return self.g + self.h < other.g + other.h

	def __eq__(self, other):
		return self.g + self.h == other.g + other.h

