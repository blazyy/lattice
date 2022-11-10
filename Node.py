from __future__ import (
    annotations,
)  # Used for type hinting to set type of class method to class itself, i.e. in set_predecessor() function below.
from collections import namedtuple

from enums import NodeState
from typing import Optional


node_colours = {
    NodeState.WALL: 'black',
    NodeState.VACANT: 'white',
    NodeState.ORIGIN: 'green',
    NodeState.GOAL: 'red',
    NodeState.VISITED: 'blue',
    NodeState.PATH: 'yellow',
}

Pos = namedtuple('Pos', ['r', 'c'])


class Node:
    '''
    Representation of a single node in the entire lattice.
    '''

    # Type hints
    predecessor: Optional[Node]

    def __init__(self, pos: Pos, state: NodeState = NodeState.VACANT) -> None:
        '''
        Initializes the node with the value NodeState.VACANT.
        '''

        self.state = state
        self.pos = pos
        self.predecessor = None

    def get_state(self) -> NodeState:
        '''
        Returns the node's state, which is of type NodeState.
        '''

        return self.state

    def set_state(self, new_state: NodeState) -> None:
        '''
        Sets the node's state to the new provided NodeState.
        '''

        self.state = new_state

    def get_pos(self) -> Pos:
        '''
        Returns the node's position, which is of type Pos.
        '''

        return self.pos

    def set_predecessor(self, predecessor: Node) -> None:
        '''
        Sets the predecessor, i.e. the node that came before the current node
        for a certain path.
        '''

        self.predecessor = predecessor

    def get_predecessor(self) -> Optional[Node]:
        '''
        Returns the predecessor, i.e. the node that came before the current node
        for a certain path.
        '''

        return self.predecessor

    def reset(self) -> None:
        '''
        Resets the node by setting state to NodeState.VACANT and setting predecessor to None.
        '''

        self.state = NodeState.VACANT
        self.predecessor = None

    def __repr__(self) -> str:
        '''
        Returns the Pos tuple value for the node in a string format. Used for console output.
        '''

        return f'({self.pos.r}, {self.pos.c})'
