import numpy as np
from ezgraphics import GraphicsWindow
import sys
import heapq
from class_infor import *
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

def surround_update(Maze, Mazeinfor, snode, s_goal, counter, Queue, close_open_list):
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
            successor.h = Manhattan(successor, s_goal)
            successor.search = counter
            heapq.heappush(Queue, successor)
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
            successor.h = Manhattan(successor, s_goal)
            successor.search = counter
            heapq.heappush(Queue, successor)

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
            successor.h = Manhattan(successor, s_goal)
            successor.search = counter
            heapq.heappush(Queue, successor)
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
            successor.h = Manhattan(successor, s_goal)
            successor.search = counter
            heapq.heappush(Queue, successor)
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


def ComputePath(Maze, Mazeinfor, counter, s_goal, Queue, close_open_list):
    # check whether queue is empty
    while (len(Queue) > 0):
        # print(len(Queue))
        '''
        for i in Queue:
            print("queue has [{} {}]".format(i.x, i.y))
        print("#######")
        '''

        '''
        tie breaking implementation for when 2 nodes in the heap have the same f value
        we tie break in 2 ways:
        1. by choosing the node with the smaller g value
        2. choosing the node the the larger g value
        used this to do time analysis on tie breaking
        '''
        
        ''' tie breaking by smaller g value - commented out to let other tie breaker work
        #tie breaking by smaller g value
        if len(Queue) > 1:
            snode1 = heapq.heappop(Queue)
            snode2 = heapq.heappop(Queue)

            if snode1.fValue() == snode2.fValue():
                if snode1.g > snode2.g:
                    heapq.heappush(Queue, snode1)
                    snode = snode2
                else: 
                    heapq.heappush(Queue, snode2)
                    snode = snode1
            else:
                heapq.heappush(Queue, snode2)
                snode = snode1
        else: 
            snode = heapq.heappop(Queue)
        '''

        if len(Queue) > 1:
            snode1 = heapq.heappop(Queue)
            snode2 = heapq.heappop(Queue)

            if snode1.fValue() == snode2.fValue():
                if snode1.g < snode2.g:
                    heapq.heappush(Queue, snode1)
                    snode = snode2
                else: 
                    heapq.heappush(Queue, snode2)
                    snode = snode1
            else:
                heapq.heappush(Queue, snode2)
                snode = snode1
        else: 
            snode = heapq.heappop(Queue);

        #snode = heapq.heappop(Queue)
        #print("pop point {} {}".format(snode.x, snode.y))
        xcoor = snode.x
        ycoor = snode.y
        close_open_list[xcoor][ycoor] = True
        if (snode.x == s_goal.x and snode.y == s_goal.y):
            return
        # update s's successors, executing step 5 to 13
        surround_update(Maze, Mazeinfor, snode, s_goal, counter, Queue, close_open_list)


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
    # keep moving until
    while (track != None):
        x = track.x
        y = track.y
        if (not map_info[x][y].isBlocked):
            detect(map_info[x][y], maze, map_info)
            position = track
            path.push(position.x, position.y)
            track = track.parent
        else:
            break
    # need to complete
    return position


def main():
    #seed the map in order to be able to generate the same map and compare run times of tie breaking
    np.random.seed(0)

    start = time.time()
    # generate a random foggy map
    maze = setup()
    # generate a information map
    map_info = setup_info()

    counter = 0
    # start from the begining, end at the goal stage
    s_start = map_info[0][0]

    # detect the block
    detect(s_start, maze, map_info)
    s_goal = map_info[size - 1][size - 1]
    path = point(-1, -1)
    while not (s_start.x == s_goal.x and s_start.y == s_goal.y):
        openlist = []
        close_open_list = [[False for i in range(size)] for j in range(size)]
        counter += 1
        s_goal.g = 0
        s_start.search = counter
        s_goal.search = counter
        # push the start stage information to queue
        s_goal.h = Manhattan(s_goal, s_start)
        heapq.heappush(openlist, s_goal)

        # print("push point {} {}".format(s_start.x, s_start.y))

        '''
        track record the current idea path from current start goal to the final goal
        '''
        ComputePath(maze, map_info, counter, s_start, openlist, close_open_list)
        if len(openlist) == 0:
            print("I cannot reach the target.")
            return

        '''
        while(ptr != None):
            print('track is [{} {}]'.format(ptr.x, ptr.y), end=' ')
            ptr = ptr.next
        '''
        s_start = take_action(s_start, maze, map_info, path)
        #print("move to point [{} {}]".format(s_start.x, s_start.y))
    	# print("current path end is [{} {}]".format(path_ptr.x, path_ptr.y))
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
    main()
