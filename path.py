'''
class Step and Path, to store pathfinding paths
Created on 2010-09-11
@author: Artsimboldo
'''

#-----------------------------------------------------------------------------
class Step(object):
    '''
    classdocs
    '''

    #----------------------------------------------------------------------
    def __init__(self, node):
        '''
        Constructor
        '''
        self.i = node.i
        self.j = node.j
        
    #-----------------------------------------------------------------------------
    def __str__(self):
        return "(" + str(self.i) + "," + str(self.j) + ")"
    #----------------------------------------------------------------------
    def __eq__(self, other):
        if isinstance(other, Step):
            return (self.i == other.i and self.j == other.j)
        else:
            return False
        
    #----------------------------------------------------------------------
    def __hash__(self):
        return self.i * self.j
        
#-----------------------------------------------------------------------------
class Path(object):
    '''
    classdocs
    '''

    #----------------------------------------------------------------------
    def __init__(self):
        '''
        Constructor
        '''
        self.steps = []
        
    #-----------------------------------------------------------------------------
    def __str__(self):
        return  '->'.join(step.__str__() for step in self.steps)
    
    #----------------------------------------------------------------------
    def appendStep(self, node):
        self.steps.append(Step(node))
        
    #----------------------------------------------------------------------
    def prependStep(self, node):
        self.steps.insert(0, Step(node))
        
