'''
class PriorityQueue
Created on 2010-10-14
@author: http://swinbrain.ict.swin.edu.au/wiki/Python_Samples_-_Priority_Queue
'''

import heapq
 
class PriorityQueue:
    '''
    classdocs
    '''
    #----------------------------------------------------------------------
    def __init__(self):
        self.heap = []

    #----------------------------------------------------------------------
    def clear(self):
        self.heap = []
 
    #----------------------------------------------------------------------
    def insert(self, object):
        heapq.heappush(self.heap, object)
 
    #----------------------------------------------------------------------
    def top(self):
        assert(not self.isEmpty())
        return self.heap[0]
 
    #----------------------------------------------------------------------
    def isEmpty(self):
        return self.heap == []
 
    #----------------------------------------------------------------------
    def size(self):
        return len(self.heap)
 
    #----------------------------------------------------------------------
    def pop(self):
        assert(not self.isEmpty())
        return heapq.heappop(self.heap)
 
    #----------------------------------------------------------------------
    def remove(self, object):
        i = -1
        for j in range(len(self.heap)):
            if self.heap[j] == object:
                i = j
                break
        if i == -1:
            return
        self.heap = self.heap[:i] + self.heap[i+1:]
        heapq.heapify(self.heap)