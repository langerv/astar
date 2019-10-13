'''
class Astar, generator-based pathfinder
Created on 2010-09-10
@author: Artsimboldo
'''

from node import Node
from priorityqueue import PriorityQueue
#from sortedlist import SortedList

#-----------------------------------------------------------------------------
class AStar():
    '''
    Properties:

    public:
    - world: 2D array of Nodes

    internal:
    - size: (width, height) tuple of world
    - open: Nodes queue to evaluate (heap-based priority queue)
    '''

    #----------------------------------------------------------------------
    def __init__(self, world):
        self.world = world
        self.size = (len(world), len(world[0]))
#        self.open = SortedList()
        self.open = PriorityQueue()
        self.openValue = 1
        self.closedValue = 2

    #----------------------------------------------------------------------
    def initSearch(self, start, goal, obstacles):
        ''' first, check we can achieve the goal'''
        if goal.type in obstacles:
            return False

        ''' clear open list and setup new open/close value state to avoid the clearing of a closed list'''
        self.open.clear()
        self.openValue += 2
        self.closedValue += 2
        
        ''' then init search variables'''
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.start.cost = 0
        self.addToOpen(self.start)
        self.goal.parent = None
        return True

    #----------------------------------------------------------------------
    def search(self):
        while not self.openIsEmpty():
            current = self.popFromOpen()
            if current == self.goal:
                break
            self.removeFromOpen(current)
            self.addToClosed(current)

            ''' generator passes : look at the 8 neighbours around the current node from open'''
            for (di, dj) in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                neighbour = self.getNode(current.i + di, current.j + dj)
                if (not neighbour) or (neighbour.type in self.obstacles):
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
                    neighbour.heuristic = self.getHeuristicCost(neighbour, self.goal)
                    neighbour.parent = current
                    self.addToOpen(neighbour)

            ''' exit with None = path not yet found'''
            yield None

        '''since we've run out of search 
        there was no path. Just return'''
        if self.goal.parent is None:
            return
        
        '''At this point we've definitely found a path so we can uses the parent
        references of the nodes to find out way from the target location back
        to the start recording the nodes on the way.'''
        path = []
        goal = self.goal
        while goal is not self.start:
            path.insert(0, (goal.i, goal.j))
            goal = goal.parent
        
        ''' done, exit with path'''
        yield path

    #-----------------------------------------------------------------------------
    def getNode(self, i, j):
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
#        return self.open.first()
        return self.open.pop()

    #----------------------------------------------------------------------
    def addToOpen(self, node):
#        self.open.add(node)
        self.open.insert(node)
        node.state = self.openValue
        
    #----------------------------------------------------------------------
    def inOpenList(self, node):
        return node.state is self.openValue
   
    #----------------------------------------------------------------------
    def removeFromOpen(self, node):
#        self.open.remove(node)
        self.open.remove(node)
        node.state = 0

    #----------------------------------------------------------------------
    def openIsEmpty(self):
#        return not self.open.size()
        return self.open.isEmpty()
        
    #----------------------------------------------------------------------
    def addToClosed(self, node):
        node.state = self.closedValue
        
    #----------------------------------------------------------------------
    def inClosedList(self, node):
        return node.state is self.closedValue

#-----------------------------------------------------------------------------
import random as rnd
import unittest

class TestAstar(unittest.TestCase):
    def test(self):
        # Create a world of Nodes to test
        width, height = 20, 10
        obstacle = 'X'
        world = [[Node(i, j, '.') for j in range(height)] for i in range(width)]

        # put obstacles randomly inside the word
        for n in range(50):
            world[rnd.randint(1, width - 2)][rnd.randint(1, height - 2)].type = obstacle

        # run search iterator from start to goal
        astar = AStar(world)
        start = world[0][0]
        goal = world[width - 1][height - 1]
        self.assertTrue(astar.initSearch(start, goal, [obstacle]))
        path = None
        iterSearch = astar.search()
        while True:
            try:
                path = iterSearch.next()
            except StopIteration:
                break

        # Display found path and world as strings
        self.assertNotEqual(path, None)
        for (i, j) in path:
            self.assertNotEqual(world[i][j].type, obstacle)
            world[i][j] = '*'

        world[start.i][start.j] = 'S'
        world[goal.i][goal.j] = 'G'

        world_str = ''
        for j in range(height):
            world_str += ''.join(str(world[i][j]) for i in range(width)) + '\n'
        print world_str

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()