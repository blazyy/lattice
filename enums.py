from enum import Enum


class DrawMode(Enum):
    WALL = 1


class NodeState(Enum):
    VACANT = 0
    WALL = 1

    def opposite(self):
        if self is NodeState.VACANT:
            return NodeState.WALL
        elif self is NodeState.WALL:
            return NodeState.VACANT
