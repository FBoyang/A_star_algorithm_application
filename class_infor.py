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
	def __init__(self, block = False):
		self.x = 0
		self.y = 0
		self.h = 0
		self.g = 0
		self.search = 0
		self.parent = None
		self.next = None
		self.isBlocked = block


	def __lt__(self, other, c = 100*100):
		#define a new rule to make comparison based on the f value of two cells
		return c * (self.g + self.h) - self.g < c * (other.g + other.h) - other.g


	def addFront(self, node):
		restlist = self.next
		self.next = node
		node.next = restlist

class point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.next = None

	def push(self, x, y):
		new = point(x, y)
		restlist = self.next
		self.next = new
		new.next = restlist

