from enums import DrawMode, NodeState


node_colors = {
    NodeState.WALL: 'black',
    NodeState.VACANT: 'white',
    NodeState.ORIGIN: 'green',
}


class Node:
    '''
    Representation of a single node in the entire lattice.
    '''

    def __init__(self, state: NodeState = NodeState.VACANT) -> None:
        self.state = state

    def get_state(self) -> NodeState:
        return self.state

    def set_state(self, new_state: NodeState) -> None:
        self.state = new_state
