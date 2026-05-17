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
    
# def breadth_first_search(graph: Graph, start: Location):
#     # print what we find
#     frontier = Queue()
#     frontier.put(start)
#     reached: set[Location]-set()
#     reached.add(start)
    
#     while not frontier.empty():
#         current: Location = frontier.get()
#         for next in graph.neighbors(current):
#             if next not in reached:
#                 frontier.put(next)
#                 reached.add(next)


# print('Reachable from A:')
# breadth_first_search(example_graph,'A')
# print('Reachable from E:')
# breadth_first_search(example_graph,'E')

# def breadth_first_search(graph: Graph, start: Location):
#     # print what we find
#     frontier = Queue()
#     frontier.put(start)
#     came_from: dict[Location, Optional[Location]] = {}
#     came_from[start] = None
    
#     while not frontier.empty():
#         current: Location = frontier.get()
#         for next in graph.neighbors(current):
#             if next not in came_from:
#                 frontier.put(next)
#                 came_from[next] = current
#     return came_from

# early exit variation 
def breadth_first_search(graph: Graph, start: Location, goal: Location):
    # print what we find
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        # early exit variation 
        if current == goal: 
            break 
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    return came_from

# reachable example 
# print('Reachable from A:')
# breadth_first_search(example_graph,'A')
# print('Reachable from E:')
# breadth_first_search(example_graph,'E')
     

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
        neighbors = [(x+1, y), (x-1, y), (x,y-1), (x, y+1)] # E W N S
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
# draw_grid(g)


# start = (8, 7)
# parents = breadth_first_search(g,start)
# draw_grid(g, point_to=parents, start=start)

# early exit 
start = (8,7) 
goal = (17,2) 
parents = breadth_first_search(g, start, goal) 
draw_grid(g, point_to=parents, start=start, goal=goal)


# 1.3 Dijkstra's algorithm
# evaluates cost (weight) of movements 

# how is this working 
class WeightedGraph(Graph): # type?
    def cost(self, from_id: Location, to_id: Location)-> float: pass

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height) # super allows other classes to use more easily 
        self.weights: dict[GridLocation, float] = {}
        
    def cost(self, from_node: GridLocation, to_node: GridLocation)-> float:
        return self.weights.get(to_node, 1) 
    

import heapq

class PriorityQueue: # review this section and heapq 
    def __init__(self):
        self.elements: list[tuple[float, T]] = []
        
    def empty(self)->bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
        
    def get(self) -> T: 
        return heapq.heappop(self.elements)[1]
    
# above is a wrapper, but python has queue.PriorityQueue built in 


def dijkstra_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0) # start/0 pushed to heapq.heappush
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get() # heapq.heappop
        
        if current == goal:  # early exit 
            break 
        
        for next in graph.neighbors(current): 
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next]=new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current 
    return came_from, cost_so_far


def reconstruct_path(came_from: dict[Location, Location], start: Location, goal: Location)-> list[Location]:
    current: Location = goal
    path: list[Location]= []
    if goal not in came_from: # no path found
        return []
    while current != start: 
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional 
    # sometimes more useful to store backwards or add start node
    return path

diagram4 = GridWithWeights(10,10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

start, goal = (1,4), (8,3) 
came_from, cost_so_far = dijkstra_search(diagram4, start, goal)
draw_grid(diagram4, point_to=came_from, start=start, goal=goal)
print()
draw_grid(diagram4, path=reconstruct_path(came_from, start=start, goal=goal))
# copy into sublime text to see bigger
# the @ is the chosen path 
# shown example has a forest in the middle which you avoid with the path

# 1.3.4 no path 



    

    

