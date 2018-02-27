import numpy as np
from ezgraphics import GraphicsWindow
import sys
from class_infor import *
import time
size = 81

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

def surround_update(Maze, Mazeinfor, snode, s_goal, Queue, close_open_list):
    xcoor = snode.x
    ycoor = snode.y
    global counter
    global canvas
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
            MinHeap.push(Queue, successor)
            counter += 1
            canvas.drawRect(10 + successor.x * 10, 10 + successor.y * 10, 10, 10)
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
            MinHeap.push(Queue, successor)
            counter += 1
            canvas.drawRect(10 + successor.x * 10, 10 + successor.y * 10, 10, 10)

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
            MinHeap.push(Queue, successor)
            counter += 1
            canvas.drawRect(10 + successor.x * cell_size, 10 + successor.y * 10, 10, 10)
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
            MinHeap.push(Queue, successor)
            counter += 1
            canvas.drawRect(10 + successor.x * cell_size, 10 + successor.y * 10, 10, 10)
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


def Manhattan(start, goal):
    return (abs(goal.x - start.x) + abs(goal.y - start.y))


def ComputePath(Maze, Mazeinfor, s_goal, Queue, close_open_list):
    # check whether queue is empty
    while (len(Queue) > 0):
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
            return
        # update s's successors, executing step 5 to 13
        surround_update(Maze, Mazeinfor, snode, s_goal, Queue, close_open_list)


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


def take_action_F(track, maze, map_info, path):
    global counter
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
                counter += 1
                track = track.next
            else:
                break
    # need to complete
    return position


def main_F():
    global counter
    global canvas
    global maze
    start = time.time()
    # generate a random foggy map
    # generate a information map
    map_info = setup_info()

    for i in range(size):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(size):  # So does j.
            cell = maze[i][j]

            canvas.setFill('white')
            # draw cell_size * cell_size rectangle at point (offset_x + i * cell_size, offset_y + j * cell_size)
            canvas.drawRect(10 + i * 10, 10 + j * 10, 10, 10)


    counter = 0
    # start from the begining, end at the goal stage
    s_start = map_info[0][0]

    # detect the block
    detect(s_start, maze, map_info)
    s_goal = map_info[size - 1][size - 1]
    path = point(-1, -1)
    while not (s_start.x == s_goal.x and s_start.y == s_goal.y):
        openlist = MinHeap()
        close_open_list = [[False for i in range(size)] for j in range(size)]
        s_start.g = 0
        # push the start stage information to queue
        s_start.h = Manhattan(s_start, s_goal)
        MinHeap.push(openlist, s_start)

        # print("push point {} {}".format(s_start.x, s_start.y))

        '''
        track record the current idea path from current start goal to the final goal
        '''
        canvas.setFill('blue')
        ComputePath(maze, map_info, s_goal, openlist, close_open_list)
        track = traceback(map_info, s_goal)
        if len(openlist) == 0:
            print("I cannot reach the target.")
            return

        '''
        while(ptr != None):
            print('track is [{} {}]'.format(ptr.x, ptr.y), end=' ')
            ptr = ptr.next
        '''
        s_start = take_action_F(track, maze, map_info, path)
        #print("move to point [{} {}]".format(s_start.x, s_start.y))
        #print("current path end is [{} {}]".format(s_start.x, s_start.y))
    	# print("goal point is [{} {}]".format(s_goal.x, s_goal.y))

    '''
        follow the tree pointers from s_goal to s_start, use a linkedlist to record
        the path, and then move the agent to the goal stage
    '''
    # final_track = final_trace(map_info, s_goal)
    ptr = path.next
    canvas.setFill('red')
    while(ptr.next != None):
    	ptr = ptr.next

    while (ptr != None):
        xcoor = ptr.x
        ycoor = ptr.y
        canvas.drawOval(10 + xcoor * 10 + 10*.2, 10 + ycoor * 10 + 10*.2, 10*.6, 10*.6)


        # canvas.drawRect(off + xcoor * cell_size, off + ycoor * cell_size, cell_size, cell_size)
        #print("path at [{} {}]".format(xcoor, ycoor))
        ptr = ptr.parent
    '''
    while ptr != None:
        print("path is [{} {}]".format(ptr.x, ptr.y), end = " ")
        ptr = ptr.next
    '''
    end = time.time()
    print("Time:" , end - start)
    canvas.setFill('red')
    for i in range(size):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(size):  # So does j.
            cell = maze[i][j]
            if cell.ifBlocked:
                canvas.setFill('black')
                # draw cell_size * cell_size rectangle at point (offset_x + i * cell_size, offset_y + j * cell_size)
                canvas.drawRect(10 + i * 10, 10 + j * 10, 10, 10)
    #draw(maze, path)

    return

def main_B():
    start = time.time()
    # generate a random foggy map
    global maze
    # generate a information map
    map_info = setup_info()

    counter = 0
    # start from the begining, end at the goal stage
    s_start = map_info[0][0]

    # detect the block
    detect(s_start, maze, map_info)
    s_goal = map_info[size - 1][size - 1]
    path = point(-1, -1)
    for i in range(size):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(size):  # So does j.
            cell = maze[i][j]

            canvas.setFill('white')
            # draw cell_size * cell_size rectangle at point (offset_x + i * cell_size, offset_y + j * cell_size)
            canvas.drawRect(10 + i * 10, 10 + j * 10, 10, 10)
    while not (s_start.x == s_goal.x and s_start.y == s_goal.y):
        openlist = MinHeap()
        close_open_list = [[False for i in range(size)] for j in range(size)]
        s_goal.g = 0
        s_start.search = counter
        s_goal.search = counter
        # push the start stage information to queue
        s_goal.h = Manhattan(s_goal, s_start)
        MinHeap.push(openlist, s_goal)

        # print("push point {} {}".format(s_start.x, s_start.y))

        '''
        track record the current idea path from current start goal to the final goal
        '''
        canvas.setFill('blue')
        ComputePath(maze, map_info, s_start, openlist, close_open_list)
        if len(openlist) == 0:
            print("I cannot reach the target.")
            return

        '''
        while(ptr != None):
            print('track is [{} {}]'.format(ptr.x, ptr.y), end=' ')
            ptr = ptr.next
        '''
        s_start = take_action_B(s_start, maze, map_info, path)
        #print("move to point [{} {}]".format(s_start.x, s_start.y))
    	# print("current path end is [{} {}]".format(path_ptr.x, path_ptr.y))
    	# print("goal point is [{} {}]".format(s_goal.x, s_goal.y))

    '''
        follow the tree pointers from s_goal to s_start, use a linkedlist to record
        the path, and then move the agent to the goal stage
    '''
    # final_track = final_trace(map_info, s_goal)
    canvas.setFill('red')
    ptr = path.next
    while(ptr.next != None):
    	ptr = ptr.next

    while (ptr != None):
        xcoor = ptr.x
        ycoor = ptr.y
        canvas.drawOval(10 + xcoor * 10 + 10*.2, 10 + ycoor * 10+ 10*.2, 10*.6, 10*.6)
        #print("path at [{} {}]".format(xcoor, ycoor))
        ptr = ptr.parent
    '''
    while ptr != None:
        print("path is [{} {}]".format(ptr.x, ptr.y), end = " ")
        ptr = ptr.next
    '''
    end = time.time()
    print("Time:" , end - start)

    for i in range(size):  # Note that i ranges from 0 through 7, inclusive.
        for j in range(size):  # So does j.
            cell = maze[i][j]
            if cell.ifBlocked:
                canvas.setFill('black')
                # draw cell_size * cell_size rectangle at point (offset_x + i * cell_size, offset_y + j * cell_size)
                canvas.drawRect(10 + i * cell_size, 10 + j * 10, 10, 10)
    #draw(maze, path)
    return

def take_action_B(track, maze, map_info, path):
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

if __name__ == "__main__":
    counter = 0
    maze = setup()
    win = GraphicsWindow(size * 10 * 1.2, size * 10 * 1.2)
    canvas = win.canvas()
    cell_size = 10
    main_F()
    print("repeated forward: {}".format(counter))
    win.wait()


    win = GraphicsWindow(size * 10 * 1.2, size * 10 * 1.2)
    canvas = win.canvas()
    main_B()
    print("repeated backward: {}".format(counter))
    win.wait()





