from enum import Enum


class NodeState(Enum):
    OFF = 0
    ON = 1

    def opposite(self):
        if self is NodeState.OFF:
            return NodeState.ON
        elif self is NodeState.ON:
            return NodeState.OFF


node_colors = {
    NodeState.OFF: 'black',
    NodeState.ON: 'white'
}


class Node:
    '''
    Representation of a single node in the entire lattice.
    '''

    def __init__(self, state: NodeState = NodeState.OFF):
        self.state = state

    def get_state(self):
        return self.state

    def flip_state(self):
        self.state = self.state.opposite()

    def __repr__(self):
        return f'{self.state}'
