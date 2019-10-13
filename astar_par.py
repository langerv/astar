'''
class ParStar, parrallel pathfinding using the mutiprocessing package
Created on 2010-10-17
@author: Artsimboldo
'''

import sys
import multiprocessing, Queue
from node import Node
from priorityqueue import PriorityQueue
#from sortedlist import SortedList
 
#-----------------------------------------------------------------------------
class Task(object):
    def __init__(self, name, start, goal, obstacles):
        self.name = name
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
            
    def __str__(self):
        return 'task %s calculating path from %s to %s.' % (self.name, self.start, self.goal)

#-----------------------------------------------------------------------------
class AStarPar(multiprocessing.Process):
    '''
    classdocs
    '''
    
    #----------------------------------------------------------------------
    def __init__(self, world, (tasks, results)):
        '''
        Constructor
        '''
        multiprocessing.Process.__init__(self)
        self.tasks = tasks
        self.results = results
        self.world = world
        self.size = (len(world), len(world[0]))
        self.open = PriorityQueue()
        self.openValue = 1
        self.closedValue = 2

    #----------------------------------------------------------------------
    def run(self):
        proc = multiprocessing.current_process()
        while True:
            try:
                task = self.tasks.get()
                if task is None:
                    # Poison pill to shutdown
                    self.tasks.task_done()
                    print '%s: Exiting' % proc.name
                    sys.stdout.flush()
                    break
                print '%s (pid %s): %s' % (proc.name, proc.pid, task)
                self.results[task.name] = self.findPath(self.getNode(task.start), self.getNode(task.goal), task.obstacles)
                self.tasks.task_done()
                sys.stdout.flush()
            except Queue.Empty:
                pass

    #----------------------------------------------------------------------
    def findPath(self, start, goal, obstacles):
        ''' first, check we can achieve the goal'''
        if goal.type in obstacles:
            return None

        ''' clear open list and setup new open/close value state to avoid the clearing of a closed list'''
        self.open.clear()
        self.openValue += 2
        self.closedValue += 2
        
        ''' then init search variables'''
        start.cost = 0
        self.addToOpen(start)
        goal.parent = None
        
        while not self.openIsEmpty():
            current = self.popFromOpen()
            if current == goal:
                break
            self.removeFromOpen(current)
            self.addToClosed(current)
            
            ''' look at the 8 neighbours around the current node from open'''
            for (di, dj) in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                neighbour = self.getNode((current.i + di, current.j + dj))
                if (not neighbour) or (neighbour.type in obstacles):
                    continue
                
                '''the cost to get to this node is the current cost plus the movement
                cost to reach this node. Note that the heuristic value is only used
                in the open list'''
                nextStepCost = current.cost + self.getNeighbourCost(current, neighbour)
                
                '''if the new cost we've determined for this node is lower than 
                it has been previously makes sure the node has not been
                determined that there might have been a better path to get to
                this node, so it needs to be re-evaluated'''
                
                if nextStepCost < neighbour.cost and (self.inOpenList(neighbour) or self.inClosedList(neighbour)):
                    self.invalidateState(neighbour)
                        
                '''if the node hasn't already been processed and discarded then
                step (i.e. to the open list)'''
                if (not self.inOpenList(neighbour)) and (not self.inClosedList(neighbour)):
                    neighbour.cost = nextStepCost
                    neighbour.heuristic = self.getHeuristicCost(neighbour, goal)
                    neighbour.parent = current
                    self.addToOpen(neighbour)

        '''since we'e've run out of search there was no path. Just return None'''
        if goal.parent is None:
            return None
        
        '''At this point we've definitely found a path so we can uses the parent
        references of the nodes to find out way from the target location back
        to the start recording the nodes on the way.'''
        path = []
        while goal is not start:
            path.insert(0, (goal.i, goal.j))
            goal = goal.parent
        
        ''' done, exit with path'''
        return path

    #-----------------------------------------------------------------------------
    def getNode(self, (i, j)):
        if i >=0 and i < self.size[0] and j >= 0 and j < self.size[1]:
            return self.world[i][j]
        else:
            return None

    #----------------------------------------------------------------------
    def getNeighbourCost(self, n1, n2):
        return (abs(n2.i - n1.i) + abs(n2.j - n1.j))
    
    #----------------------------------------------------------------------
    def getHeuristicCost(self, n1, n2):
        return (abs(n2.i - n1.i) + abs(n2.j - n1.j))
    
    #----------------------------------------------------------------------
    def invalidateState(self, node):
        node.state = 0

    #----------------------------------------------------------------------
    def popFromOpen(self):
        return self.open.pop()

    #----------------------------------------------------------------------
    def addToOpen(self, node):
        self.open.insert(node)
        node.state = self.openValue
        
    #----------------------------------------------------------------------
    def inOpenList(self, node):
        return node.state is self.openValue
   
    #----------------------------------------------------------------------
    def removeFromOpen(self, node):
        self.open.remove(node)
        node.state = 0

    #----------------------------------------------------------------------
    def openIsEmpty(self):
        return self.open.isEmpty()
        
    #----------------------------------------------------------------------
    def addToClosed(self, node):
        node.state = self.closedValue
        
    #----------------------------------------------------------------------
    def inClosedList(self, node):
        return node.state is self.closedValue

#-----------------------------------------------------------------------------
import uuid
from itertools import product
import random as rnd
import unittest

class TestAstarPar(unittest.TestCase):
    def test(self):
        # Create a world of Nodes to test
        width, height = 20, 10
        obstacle = 'X'
        world = [[Node(i, j, '.') for j in range(height)] for i in range(width)]

        # put obstacles randomly inside the word
        for n in range(50):
            world[rnd.randint(1, width - 2)][rnd.randint(1, height - 2)].type = obstacle

        # Create a queue for tasks
        # Create a dict manager for results
        tasks = multiprocessing.JoinableQueue()
        mgr = multiprocessing.Manager()
        results = mgr.dict()

        # Start astar worker process and start 
        AStarPar(world, (tasks, results)).start()

        # load with 100 tasks
        free = [(i,j) for i,j in product(range(width), range(height)) if not world[i][j].type == obstacle]
        max = len(free) - 1
        for n in range(100):
            tasks.put(Task(n, free[rnd.randint(0, max)], free[rnd.randint(0, max)], [obstacle]))

        # last task to sync and output result
        path = None
        n += 1
        start = (0, 0)
        goal = (width - 1, height - 1)
        tasks.put(Task(n, start, goal, [obstacle]))
        while True:
            try:
                path = results[n]  
                del results[n]
                break
            except KeyError:
                pass

        # kill worker
        tasks.put(None)
        tasks.join()

        # Display found path and world as strings
        self.assertNotEqual(path, None)
        for (i, j) in path:
            self.assertNotEqual(world[i][j].type, obstacle)
            world[i][j] = '*'

        world[start[0]][start[1]] = 'S'
        world[goal[0]][goal[1]] = 'G'

        world_str = ''
        for j in range(height):
            world_str += ''.join(str(world[i][j]) for i in range(width)) + '\n'
        print world_str

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()