import numpy as np
from ezgraphics import GraphicsWindow
import sys
import heapq
from class_infor import *

size = 31
#initialize the information matrix
def setup_info():
	grid = makeGrid()
	grid[0][0] = node()
	start = grid[0][0]
	start.x = 0
	start.y = 0
	start.h = (size - 1) * 2
	start.g = 0


	grid[size - 1][size - 1] = node()
	end =grid[size - 1][size - 1]
	end.x = size - 1
	end.y = size - 1
	end.h = 0
	end.g = sys.maxint
	return grid

def isValid(x, y):
	return ((x >= 0) and (x < size) and (y >= 0) and (y < size))

'''
update the surrounding node of the current node s
It takes 3 parameters: 
Mazeinfor: the information matrix
snode: the current stage node
counter: the iteration time of the A* search

Notice:
currently I don't think we need to check counter, because I think there
is no conditon in which g(succ(s, a) would be not bigger than g(s) + c(s, a)

Please tell me if I am wrong, because I am probably wrong
'''

def surround_update(Maze, Mazeinfor, snode, s_goal, counter, Queue, closelist):
	xcoor = snode.x
	ycoor = snode.y
	#update left successor
	if(isValid(xcoor - 1, ycoor) and (not closelist[xcoor - 1][ycoor])\
		and (not Mazeinfor[xcoor - 1][ycoor].isBlocked)) :
		#this is equal to check if succ(s, a) < counter
		if(not isinstance(Mazeinfor[xcoor - 1][ycoor], node)):
			Mazeinfor[xcoor -1][ycoor] = node()
		successor = Mazeinfor[xcoor -1][ycoor]
		if(not successor.isBlocked):
			successor.parent = snode
			successor.g = snode.g + 1
			successor.x = xcoor - 1
			successor.y = ycoor
			successor.h = Manhattan(successor, s_goal)
			successor.search = counter
			heapq.push(Queue, successor)


	#update right successor
	
	if(isValid(xcoor + 1, ycoor) and (not closelist[xcoor + 1][ycoor])\
		(not Mazeinfor[xcoor + 1][ycoor].isBlocked)):
		if(not isinstance(Mazeinfor[xcoor + 1][ycoor], node)):
			Mazeinfor[xcoor + 1][ycoor] = node()
		successor = Mazeinfor[xcoor + 1][ycoor]
		if(not successor.isBlocked):
			successor.parent = snode
			successor.parent = snode
			successor.g = snode.g + 1
			successor.xcoor = xcoor + 1
			successor.ycoor = ycoor
			successor.h = Manhattan(successor, s_goal)
			successor.search = counter
			heapq.push(Queue, successor)

	#update downward successor
	if(isValid(xcoor, ycoor - 1) and (not closelist[xcoor][ycoor - 1])\
		(not Mazeinfor[xcoor][ycoor - 1].isBlocked)):
		if(not isinstance(Mazeinfor[xcoor][ycoor - 1], node)):
			Mazeinfor[xcoor][ycoor - 1] = node()
		successor = Mazeinfor[xcoor][ycoor - 1]
		if(not successor.isBlocked):
			successor.parent = snode
			successor.g = snode.g + 1
			successor.xcoor = xcoor
			successor.ycoor = ycoor - 1
			successor.h = Manhattan(successor, s_goal)
			successor.search = counter
			heapq.push(Queue, successor)

	#update upward successor
	if(isValid(xcoor, ycoor + 1) and (not closelist[xcoor][ycoor + 1])\
		(not Mazeinfor[xcoor][ycoor + 1].isBlocked)):
		if(not isinstance(Mazeinfor[xcoor][ycoor + 1], node)):
			Mazeinfor[xcoor][ycoor + 1] = node()
		successor = Mazeinfor[xcoor][ycoor + 1]
		if(not successor.isBlocked):
			successor.parent = snode
			successor.g = snode.g + 1
			successor.xcoor = xcoor
			successor.ycoor = ycoor + 1
			successor.h = Manhattan(successor, s_goal)
			successor.search = counter
			heapq.push(Queue, successor)

	

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




'''
	detect function mimic the sensor detection, to be more specific, 
	suppose the agent standing at the stage s, using the real word information
	maze to update the surrounding information to map_info 
'''

def detect(s, maze, Mazeinfor):
	xcoor = s.x
	ycoor = s.y
	if(isValid(xcoor - 1, ycoor)) :
		#this is equal to check if succ(s, a) < counter
		if(not isinstance(Mazeinfor[xcoor - 1][ycoor], node)):
			Mazeinfor[xcoor -1][ycoor] = node()
		successor = Mazeinfor[xcoor -1][ycoor]
		successor.isBlocked = maze[xcoor -1][ycoor].ifBlocked

	if(isValid(xcoor + 1, ycoor)):
		if(not isinstance(Mazeinfor[xcoor + 1][ycoor], node)):
			Mazeinfor[xcoor + 1][ycoor] = node()
		successor = Mazeinfor[xcoor + 1][ycoor]
		successor.isBlocked = maze[xcoor + 1][ycoor].ifBlocked

	if(isValid(xcoor, ycoor - 1)):
		if(not isinstance(Mazeinfor[xcoor][ycoor - 1], node)):
			Mazeinfor[xcoor][ycoor - 1] = node()
		successor = Mazeinfor[xcoor][ycoor - 1]
		successor.isBlocked = maze[xcoor][ycoor - 1].ifBlocked

	if(isValid(xcoor, ycoor + 1)):
		if(not isinstance(Mazeinfor[xcoor][ycoor + 1], node)):
			Mazeinfor[xcoor][ycoor + 1] = node()
		successor = Mazeinfor[xcoor][ycoor + 1]
		successor.isBlocked = maze[xcoor][ycoor + 1].ifBlocked


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


def Manhattan(start, goal):
	return (abs(goal.x - start.x) + abs(goal.y - start.y))



def ComputePath(Maze, Mazeinfor, counter, s_goal, Queue, closelist):
	#check whether queue is empty
	while(len(Queue) > 0):
		snode = heapq.heappop(Queue)
		xcoor = snode.x
		ycoor = snode.y
		closelist[xcoor][ycoor] = True
		if(snode.x == s_goal.x and snode.y == s_goal.y):
			#update s's successors, executing step 5 to 13
			surround_update(Maze ,Mazeinfor, snode, s_goal,counter, Queue, closelist)


'''
traceback function serves to record the current ideal path that the agent 
estimate from the current position to the destination

In the form of a linked list
'''
def traceback(map_info, s_goal):
	 
	tracklist = node()
	ptr = s_goal
	#while ptr hasn't reach the start node
	while(ptr.g != 0):
		tracklist.addFront(ptr)
		ptr = ptr.parent

	tracklist.addFront(ptr)
	return tracklist.next


def take_action(track, maze, map_info):
	ptr = track
	x = ptr.x
	y = ptr.y
	position = None
	if(map_info[x][y].g != 0):
		print("wrong start point")
		exit(0)
	else:
		#keep moving until 
		while(ptr != None):
			x = ptr.x
			y = ptr.y
			detect(map_info[x][y], maze, map_info)
			if(not map_info[x][y].isBlocked):
				position = ptr
			else:
				break
			ptr = ptr.next
	#need to complete
	return position

	

def main():
	#generate a random foggy map
	maze = setup()

	#generate a information map
	map_info = setup_info()

	counter = 0
	#start from the begining, end at the goal stage
	s_start = map_info[0][0]

	#detect the block
	detect(s_start, maze, map_info)
	s_goal = map_info[size - 1][size - 1]

	while not (s_start.x == s_goal.x and s_start.y == s_goal.y):
		openlist = []
		closelist = [[False for i in range(size)] for j in range(size)]
		counter += 1
		s_start.g = 0
		s_start.search = counter
		s_goal.search = counter
		#push the start stage information to queue
		s_start.h = Manhattan(s_start, s_goal)
		heapq.push(openlist, s_start)
		ComputePath(map_foggy, map_info, counter, s_goal, openlist, closelist)

		## TODO Boyang, can you double check the variable above? --> map-foggy: undeclared
		if len(openlist) == 0:
			print("I cannot reach the target.")
			return


		'''
		follow the tree pointers from s_goal to s_start, use a linkedlist to record
		the path, and then move the agent to the goal stage
		''' 
		track = traceback(map_info)

		s_start = take_action(track, maze, map_info)

		print("I reached the target")
		return


#draw()










#
