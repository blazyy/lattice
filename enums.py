from enum import Enum


class DrawMode(Enum):
    SET_WALL = 0
    SET_ORIGIN = 1
    SET_VACANT = 2
    SET_GOAL = 3


class NodeState(Enum):
    VACANT = 0
    WALL = 1
    ORIGIN = 2
    GOAL = 3
    VISITED = 4
    PATH = 5


class PathfindingOption(Enum):
    BFS = 1
    DFS = 2
    DIJKSTRA = 3
    A_STAR = 4