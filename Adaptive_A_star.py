import numpy as np
from ezgraphics import GraphicsWindow
import sys
import heapq
from class_infor2 import *
import time
size = 101


# initialize the information matrix
def setup_info():
    grid = makeGrid()
    grid[0][0] = node()
    start = grid[0][0]
    start.x = 0
    start.y = 0
    start.h = (size - 1) * 2
    start.g = 0

    grid[size - 1][size - 1] = node()
    end = grid[size - 1][size - 1]
    end.x = size - 1
    end.y = size - 1
    end.h = 0
    end.g = sys.maxsize
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



'''
Important!!!!
declaration about why don't need to set g value to infinity:
because the cost always has a constant 1.
The close list and the open list can be merge into one list: close_open_list,
because any node's g value that already in the open list don't need to be further updated
if location (x, y) in close_open_list has value true, it is either in the close list,
or already in the open list which won't need to be modified.
'''

def surround_update(Maze, Mazeinfor, snode, s_goal, Queue, close_open_list, visited_list):
    xcoor = snode.x
    ycoor = snode.y

    # update right successor

    if (isValid(xcoor + 1, ycoor) and (not close_open_list[xcoor + 1][ycoor])):
        close_open_list[xcoor + 1][ycoor] = True
        if (not isinstance(Mazeinfor[xcoor + 1][ycoor], node)):
            Mazeinfor[xcoor + 1][ycoor] = node()
        successor = Mazeinfor[xcoor + 1][ycoor]
        if (not successor.isBlocked):
            successor.parent = snode
            successor.g = snode.g + 1
            successor.x = xcoor + 1
            successor.y = ycoor
            if(successor.nh == -1):
            	successor.h = Manhattan(successor, s_goal)
            else:
                successor.h = successor.nh
            MinHeap.push(Queue, successor)
            visited_list.append(successor)
    # print("push point {} {}".format(xcoor + 1, ycoor))

    # update left successor
    if (isValid(xcoor - 1, ycoor) and (not close_open_list[xcoor - 1][ycoor])):
        close_open_list[xcoor - 1][ycoor] = True
        # this is equal to check if succ(s, a) < counter
        if (not isinstance(Mazeinfor[xcoor - 1][ycoor], node)):
            Mazeinfor[xcoor - 1][ycoor] = node()
        successor = Mazeinfor[xcoor - 1][ycoor]
        if (not successor.isBlocked):
            successor.parent = snode
            successor.g = snode.g + 1
            successor.x = xcoor - 1
            successor.y = ycoor
            if(successor.nh == -1):
            	successor.h = Manhattan(successor, s_goal)
            else:
                successor.h = successor.nh
            MinHeap.push(Queue, successor)
            visited_list.append(successor)

    # print("push point {} {}".format(xcoor - 1, ycoor))

    

    # update downward successor
    if (isValid(xcoor, ycoor - 1) and (not close_open_list[xcoor][ycoor - 1])):
        close_open_list[xcoor][ycoor - 1] = True
        if (not isinstance(Mazeinfor[xcoor][ycoor - 1], node)):
            Mazeinfor[xcoor][ycoor - 1] = node()
        successor = Mazeinfor[xcoor][ycoor - 1]
        if (not successor.isBlocked):
            successor.parent = snode
            successor.g = snode.g + 1
            successor.x = xcoor
            successor.y = ycoor - 1
            if(successor.nh == -1):
            	successor.h = Manhattan(successor, s_goal)
            else:
                successor.h = successor.nh
            MinHeap.push(Queue, successor)
            visited_list.append(successor)
    # print("push point {} {}".format(xcoor, ycoor - 1))

    # update upward successor
    if (isValid(xcoor, ycoor + 1) and (not close_open_list[xcoor][ycoor + 1])):
        close_open_list[xcoor][ycoor + 1] = True
        if (not isinstance(Mazeinfor[xcoor][ycoor + 1], node)):
            Mazeinfor[xcoor][ycoor + 1] = node()
        successor = Mazeinfor[xcoor][ycoor + 1]
        if (not successor.isBlocked):
            successor.parent = snode
            successor.g = snode.g + 1
            successor.x = xcoor
            successor.y = ycoor + 1
            if(successor.nh == -1):
            	successor.h = Manhattan(successor, s_goal)
            else:
                successor.h = successor.nh
            MinHeap.push(Queue, successor)
            visited_list.append(successor)
    # print("push point {} {}".format(xcoor, ycoor + 1))
    return


# Make the grid, having the top left and bottom right block set to unblocked and seen
def setup():
    grid = makeGrid()
    for i in range(size):
        for j in range(size):
            # Initialize each object
            if (i == 0 and j == 0) or (i == size - 1 and j == size - 1):
                # Cell(x coor, y coor, if_blocked, if_visited)
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
    # print("locate at [{} {}]".format(xcoor, ycoor))
    if (isValid(xcoor - 1, ycoor)):
        # this is equal to check if succ(s, a) < counter
        if (not isinstance(Mazeinfor[xcoor - 1][ycoor], node)):
            Mazeinfor[xcoor - 1][ycoor] = node()
        successor = Mazeinfor[xcoor - 1][ycoor]
        successor.isBlocked = maze[xcoor - 1][ycoor].ifBlocked

    if (isValid(xcoor + 1, ycoor)):
        if (not isinstance(Mazeinfor[xcoor + 1][ycoor], node)):
            Mazeinfor[xcoor + 1][ycoor] = node()
        successor = Mazeinfor[xcoor + 1][ycoor]
        successor.isBlocked = maze[xcoor + 1][ycoor].ifBlocked

    if (isValid(xcoor, ycoor - 1)):
        if (not isinstance(Mazeinfor[xcoor][ycoor - 1], node)):
            Mazeinfor[xcoor][ycoor - 1] = node()
        successor = Mazeinfor[xcoor][ycoor - 1]
        successor.isBlocked = maze[xcoor][ycoor - 1].ifBlocked

    if (isValid(xcoor, ycoor + 1)):
        if (not isinstance(Mazeinfor[xcoor][ycoor + 1], node)):
            Mazeinfor[xcoor][ycoor + 1] = node()
        successor = Mazeinfor[xcoor][ycoor + 1]
        successor.isBlocked = maze[xcoor][ycoor + 1].ifBlocked

    return


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


def draw(maze, path_list, off=10):
    win = GraphicsWindow(size * off * 1.2, size * off * 1.2)
    canvas = win.canvas()
    cell_size = off  # Height and width of checkerboard squares.
    # start

    for i in range(size):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(size):  # So does j.
            cell = maze[i][j]
            if not cell.ifBlocked:
                color = 'white'
            else:
                color = 'black'

            canvas.setFill(color)
            # draw cell_size * cell_size rectangle at point (offset_x + i * cell_size, offset_y + j * cell_size)
            canvas.drawRect(off + i * cell_size, off + j * cell_size, cell_size, cell_size)

    ptr = path_list.next
    while(ptr.next != None):
    	ptr = ptr.next

    while (ptr != None):
        xcoor = ptr.x
        ycoor = ptr.y
        canvas.setFill('red')
        canvas.drawRect(off + xcoor * cell_size, off + ycoor * cell_size, cell_size, cell_size)
        #print("path at [{} {}]".format(xcoor, ycoor))
        ptr = ptr.parent

    win.wait()


def Manhattan(start, goal):
    return (abs(goal.x - start.x) + abs(goal.y - start.y))


def ComputePath(Maze, Mazeinfor, s_goal, Queue, close_open_list, visited_list):
    global g_goal
    # check whether queue is empty
    while (len(Queue) > 0):
        # print(len(Queue))
        '''
        for i in range(len(Queue)):
            n = Queue._MinHeap__heap[i]
            print("[{} {} {} {}] ".format(n.x, n.y, n.g, n.g + n.h), end = "")
        print(" ")
        print(" ")
        '''
        snode = MinHeap.pop(Queue)
        #print("pop point {} {}".format(snode.x, snode.y))
        xcoor = snode.x
        ycoor = snode.y
        close_open_list[xcoor][ycoor] = True
        if (snode.x == s_goal.x and snode.y == s_goal.y):
            g_goal = snode.g
            return
        # update s's successors, executing step 5 to 13
        surround_update(Maze, Mazeinfor, snode, s_goal, Queue, close_open_list, visited_list)


def traceback(map_info, s_goal):
    tracklist = node()
    ptr = s_goal
    # while ptr hasn't reach the start node
    while (ptr.g != 0):
        tracklist.addFront(ptr)
        ptr = ptr.parent

    tracklist.addFront(ptr)
    return tracklist.next


'''
traceback function serves to record the current ideal path that the agent 
estimate from the current position to the destination
In the form of a linked list
'''


def final_trace(map_info, s_goal):
    tracklist = node()
    ptr = s_goal
    # while ptr hasn't reach the start node
    while (not (ptr.x == 0 and ptr.y == 0)):
        tracklist.addFront(ptr)
        ptr = ptr.parent
    # print("ptr is [{} {}]".format(ptr.x, ptr.y))

    tracklist.addFront(ptr)
    return tracklist.next


def take_action(track, maze, map_info, path):
    x = track.x
    y = track.y
    # print("check position [{} {}]".format(x, y))
    position = None
    if (map_info[x][y].g != 0):
        print("wrong start point")
        exit(0)
    else:
        # keep moving until
        while (track != None):
            x = track.x
            y = track.y
            if (not map_info[x][y].isBlocked):
                detect(map_info[x][y], maze, map_info)
                position = track
                path.push(position.x, position.y)
                track = track.next
            else:
                break
    # need to complete
    return position


def main():
    global g_goal
    start = time.time()
    # generate a random foggy map
    maze = setup()
    # generate a information map
    map_info = setup_info()

    # start from the begining, end at the goal stage
    s_start = map_info[0][0]
    # detect the block
    detect(s_start, maze, map_info)
    s_goal = map_info[size - 1][size - 1]
    s_start.nh = Manhattan(s_start, s_goal)
    path = point(-1, -1)
    while not (s_start.x == s_goal.x and s_start.y == s_goal.y):
        visited_list = []
        openlist = MinHeap()
        close_open_list = [[False for i in range(size)] for j in range(size)]
        s_start.g = 0
        # push the start stage information to queue
        s_start.h = s_start.nh
        MinHeap.push(openlist, s_start)
        visited_list.append(s_start)
        # print("push point {} {}".format(s_start.x, s_start.y))

        '''
        track record the current idea path from current start goal to the final goal
        '''
        ComputePath(maze, map_info, s_goal, openlist, close_open_list, visited_list)
        '''
        update the hnew value
        '''
        for i in visited_list:
            i.nh = g_goal - i.g

        track = traceback(map_info, s_goal)
        if len(openlist) == 0:
            print("I cannot reach the target.")
            return

        '''
        while(ptr != None):
            print('track is [{} {}]'.format(ptr.x, ptr.y), end=' ')
            ptr = ptr.next
        '''
        s_start = take_action(track, maze, map_info, path)
        #print("move to point [{} {}]".format(s_start.x, s_start.y))
        #print("current path end is [{} {}]".format(s_start.x, s_start.y))
    	# print("goal point is [{} {}]".format(s_goal.x, s_goal.y))

    '''
        follow the tree pointers from s_goal to s_start, use a linkedlist to record
        the path, and then move the agent to the goal stage
    '''
    # final_track = final_trace(map_info, s_goal)
    ptr = path.next
    '''
    while ptr != None:
        print("path is [{} {}]".format(ptr.x, ptr.y), end = " ")
        ptr = ptr.next
    '''
    end = time.time()
    print(end - start)
    draw(maze, path)

    return


if __name__ == "__main__":
    g_goal = 0
    main()