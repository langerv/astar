'''
class Node, cell world including pathfinding states
Created on 2010-09-09
@author: Artsimboldo
'''

#---------------------------------------------------------------------------------
class Node():
    '''
    classdocs
    '''
    
    #-----------------------------------------------------------------------------
    def __init__(self, i = 0, j = 0, type = 0):
        '''
        Constructor
        '''
        self.i = i
        self.j = j
        self.type = type
        
        # pathfinding variables
        self.cost = 0.
        self.heuristic = 0.
        self.state = 0
        self.parent = None

    #-----------------------------------------------------------------------------
    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.i == other.i and self.j == other.j)
        else:
            return False
        
    #-----------------------------------------------------------------------------
    def __cmp__(self, node):
        return cmp(self.heuristic + self.cost, node.heuristic + node.cost)

    #-----------------------------------------------------------------------------
    def __str__(self):
        return str(self.type)

