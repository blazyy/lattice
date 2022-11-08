from collections import namedtuple

from enums import NodeState


node_colors = {
    NodeState.WALL: 'black',
    NodeState.VACANT: 'white',
    NodeState.ORIGIN: 'green',
    NodeState.GOAL: 'red',
    NodeState.VISITED: 'blue',
}

Pos = namedtuple('pos', ['r', 'c'])

class Node:
    '''
    Representation of a single node in the entire lattice.
    '''

    def __init__(self, pos: Pos, state: NodeState = NodeState.VACANT) -> None:
        '''
        Initializes the node with the value NodeState.VACANT.
        '''

        self.state = state
        self.pos = pos

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