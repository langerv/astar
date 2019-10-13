# python astar
*"oh baby baby, it's a tile world..."*
###astar: Tile-based A* basics
#####astar.py: pathfinding as a generator
######Optimizations
- Manhattan distance used as the heuristics.
- Heap-based priority queue instead of sorted list giving worst case O(log N) to Insert and removeMax operations.
- Open and Closed values to remove the Closed list and Conatin operations on the Open list.
- Increased memory footprint (Node array) holding local search results into tiles (see Node class).
- To avoid clearing nodes at each new search, open and closed values are increased by 2.
 
Note: storing intermediary states has the important consequence to constrain concurrency among a set of agents acting in the same world. Below is the study of various patterns working around that constraint.

######Blocking search pattern 
The basic usage of A* is to do a blocking search of a solution (path) in a frame. This is exactly what we do here:
```
iterSearch = astar.search()
while True:
    try:
        path = iterSearch.next()
    except StopIteration:
        break
```
It is often the case that a search operation takes time, and then impact significantly the framerate. Below is a diagram showing how that approach sucks - assuming search time is constant and pathing is O(1). In reality it is even worst since search time is variable and then that approach doesn't guarantee a constant framerate.
```
    +     + + + +     + + + +     + + + + 
A0: S S S P P P G . . . . . . . . . . . S 
A1: . . . . . . S S S P P P G . . . . . .
A2: . . . . . . . . . . . . S S S P P P G
```
(Legend: '+': frame; 'Ax': agent x; 'S': search operation; 'P': pathing operation; 'G': goal found; '.': stalling)
######Interlaced pattern 
It is not true we need to execute search at every frame. To simulate human-like behaviours it is reasonnable to accept a latency that emulates the thinking process. However the motions of an agent shouldn't be blocked by the search operations of other agents. 
The generator approach allows us not to wait a search is completed to execute behaviours of other agents. Granularity of the search operation is reduced to neighborhood examination which is exactly 8 fast operations in a tile-based world. However since results are stored in the shared world object, searches cannot be concurrent and must be synchronised. 
Below is an example with a very simple state machine:
```
def move(self):
    if self.state == 0 and not Busy:
        Busy = True
        goal = self.world.getSomeLocation()
        self.astar.initSearch(self.location, goal, [obstacles])
        self.state = 1
    elif self.state == 1:
        self.path = self.astar.search()
        if self.path:
            Busy = False
            self.state = 2
    elif self.state == 2:
        self.location = self.path.pop(0)
        if not self.path:
            self.state = 0
```
Note: Busy is a global variable showing example of search synchronization.

Below is another example of diagram showing reduced latencies and constant framerate thanks to generators:
```
    + + + + + + + + + + + + + + + +
A0: S S S P P P G . . S S S P P G .
A1: . . . S S S P P P G . . S S S P
A2: . . . . . . S S S P P P G . . S
```
(Legend: '+': frame; 'Ax': agent x; 'S': search operation; 'P': pathing operation; 'G': goal found; '.': stalling)

Ballpark benchmark: 16 ms / search.
#####astar_par.py: parallel pathfinding using multiprocessing
This version uses Python's [multiprocessing](https://docs.python.org/2/library/multiprocessing.html) package to offload the sequential processing of searches to other cores. A producer - consumer pattern is used. Seach are represented by Tasks enqueued in a ```JoinableQueue```. Hence, the main process doesn't need to wait anytime before to do something else. Results are stored in a synchronized dictionary where keys are related to tasks. 
Again, the world object is shared and no concurrency is possible during a search operation. However, dynamic operations on the world object may require to acquire a lock on that resource to prevent inconsistencies between the world update and search operations. 
```
def move(self):
    if self.state == 0:
        goal = self.world.getSomeLocation()
        Tasks.put(astar.Task(self.name, self.location, goal, [obstacles])
        self.state = 1
    elif self.state == 1:
        try:
            self.path = Results[self.name]
            del Results[self.name]
            self.state = 2
        except KeyError:
            pass
    elif self.state == 2:
        self.location = self.path.pop(0)
        if not self.path:
            self.state = 0
```

Ballpark benchmark: 100 tasks in 250 ms, 2.5 ms / search.
#####TODO: Concurrent pathfinding using a worker pool
Concurrent search operations require to get back the closed list to store intermediary results locally. 
