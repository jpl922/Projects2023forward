# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 17:17:22 2026
A* implementation and visualization sandbox 
Referneces and notes in Project - A star 
https://www.redblobgames.com/pathfinding/a-star/implementation.html
@author: Jason Lord
"""

# Imports
from __future__ import annotations
from typing import Protocol, Iterator, Tuple, TypeVar, Optional
import collections
#%% Breadth First Search 

T = TypeVar('T')
Location = TypeVar('Location')

class Graph(Protocol):
    def neighbors(self, id: Location)-> list[Location]: pass

class SimpleGraph:
    def __init__(self):
        self.edges: dict[Location, list[Location]] = {}
    
    def neighbors(self, id: Location)->list[Location]:
        return self.edges[id]

example_graph = SimpleGraph()
example_graph.edges = {'A':['B'], 
                       'B':['C'], 
                       'C':['B','D','F'], 
                       'D':['C','E'], 
                       'E':['F'], 
                       'F':[],
}

class Queue: # wrapper on deque can just deque directly
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self)->bool:
        return not self.elements
    
    def put(self, x: T):
        self.elements.append(x)
    
    def get(self)->T:
        return self.elements.popleft()
    
def breadth_first_search(graph: Graph, start: Location):
    # print what we find
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: Location = frontier.get()
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    return came_from

print('Reachable from A:')
breadth_first_search(example_graph,'A')
print('Reachable from E:')
breadth_first_search(example_graph,'E')
     

GridLocation = Tuple[int, int]

class SquareGrid: 
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation]=[]
        
    def in_bounds(self, id: GridLocation)->bool: 
        (x,y) = id
        return 0 <= x < self.width and 0<= y< self.height
    
    def passable(self, id: GridLocation)->bool: 
        return id not in self.walls
    
    def neighbors(self, id: GridLocation)->Iterator[GridLocation]:
        (x,y)=id
        neighbors = [(x+1, y), (x-1, y), (x,y-1), (x+y+1)] # E W N S
        # "Ugly Paths" section explains on site:
        if (x+y)% 2 == 0: neighbors.reverse() # S N W E 
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results 


# utility functions for dealing with square grids (copied only) 
def from_id_width(id, width):
    return (id % width, id // width)

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    if 'goal' in style and id == style['goal']:   r = " Z "
    if id in graph.walls: r = "###"
    return r

def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)

# data from main article
DIAGRAM1_WALLS = [from_id_width(id, width=30) for id in [21,22,51,52,81,82,93,94,111,112,123,124,133,134,141,142,153,154,163,164,171,172,173,174,175,183,184,193,194,201,202,203,204,205,213,214,223,224,243,244,253,254,273,274,283,284,303,304,313,314,333,334,343,344,373,374,403,404,433,434]]


g = SquareGrid(30,15)
g.walls = DIAGRAM1_WALLS # coords of walls 

start = (8, 7)
parents = breadth_first_search(g, start)
draw_grid(g, point_to=parents, start=start)
## NEED DEBUG 



    

