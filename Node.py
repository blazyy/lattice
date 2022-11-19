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
    NodeState.VISITED: '#054a29',
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
        self.already_rendered = False

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

    # def set_rendered(self) -> None:
    #     '''
    #     Sets self.already_rendered to True. Used to aniamted color gradient transitions in node
    #     in the consequent game loops after a node has initially been set to a certain state.
    #     '''

    #     self.already_rendered = True

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
