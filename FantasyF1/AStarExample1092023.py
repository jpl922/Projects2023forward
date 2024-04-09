# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 22:15:15 2023

@author: 17jlo
"""

# Breadth First search

# creating the graph 
from __future__ import annotations
from typing import Protocol, Iterator, Tuple, TypeVar, Optional
T = TypeVar('T')



Location = TypeVar('Location')
class Graph(Protocol):
    def neighbors(self, id: location) -> list[Location]: pass

class SimpleGraph:
    def __init__(self):
        self.edges: dict[Location, list[Location]] = {}
        
    def neighbors(self, id: Location) -> list[Location]:
        return self.edges[id]
    
    
example_graph = SimpleGraph()
example_graph.edges = {
    'A':['B'],
    'B':['C'],
    'C':['B','D','F'],
    'D':['C','E'],
    'E':['F'],
    'F':[],
}

import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
        
    def empty(self) -> bool:
        return not self.elements
        
    def put(self, x: T):
        self.elements.append(x)
        
    def get(self) -> T:
        return self.elements.popleft()

from implementation import *

def breadth_first_search(graph: Graph, start: Location):
    # Start here 