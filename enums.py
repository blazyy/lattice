from enum import Enum


class DrawMode(Enum):
    SET_WALL = 0
    SET_ORIGIN = 1
    SET_VACANT = 2


class NodeState(Enum):
    VACANT = 0
    WALL = 1
    ORIGIN = 2