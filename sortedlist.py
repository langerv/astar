'''
class SortedList
Created on 2010-09-12
@author: Artsimboldo
'''
import unittest

#-----------------------------------------------------------------------------
class TestSortedList(unittest.TestCase):
    
    #-----------------------------------------------------------------------------
    class elt():
        #-----------------------------------------------------------------------------
        def __init__(self, value):
            self.value = value
            
        #-----------------------------------------------------------------------------
        def __cmp__(self, other):
            return cmp(self.value, other.value)
    
        #-----------------------------------------------------------------------------
        def __str__(self):
            return str(self.value)

    #-----------------------------------------------------------------------------
    def testSort(self):
        listElt =  [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        listGood = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        sortedList = SortedList()
        for value in listElt:
            sortedList.add(TestSortedList.elt(value))
        for index, value in enumerate(listGood):
            self.assertEqual(value, sortedList.get(index).value)

#-----------------------------------------------------------------------------
class SortedList():
    '''
    classdocs
    '''
    #----------------------------------------------------------------------
    def __init__(self):
        '''
        Constructor
        '''
        self.list = []

    #-----------------------------------------------------------------------------
    def __str__(self):
        return ' '.join(str(elt) for elt in self.list) + '\n'
    
    #----------------------------------------------------------------------
    def first(self):
        return self.list[0];

    #----------------------------------------------------------------------
    def get(self, i):
        return self.list[i]
    
    #----------------------------------------------------------------------
    def clear(self):
        self.list = []
        
    #----------------------------------------------------------------------
    def compare(self, a, b):
        return cmp(a, b)
        
    #----------------------------------------------------------------------
    def add(self, object):
        self.list.append(object)
        self.list.sort(cmp = self.compare)

    #----------------------------------------------------------------------
    def remove(self, object):
        self.list.remove(object)
        
    #----------------------------------------------------------------------
    def size(self):
        return len(self.list)
    
    #----------------------------------------------------------------------
    def contains(self, object):
        if object in self.list:
            return True
        else:
            return False

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()   
