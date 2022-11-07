from enums import DrawMode, NodeState


node_colors = {NodeState.WALL: 'black', NodeState.VACANT: 'white'}


class Node:
    '''
    Representation of a single node in the entire lattice.
    '''

    def __init__(self, state: NodeState = NodeState.VACANT):
        self.state = state

    def get_state(self):
        return self.state

    def flip_state(self, draw_mode: DrawMode):
        if draw_mode == DrawMode.WALL and self.state == NodeState.VACANT:
            self.state = self.state.opposite()

    def __repr__(self):
        return f'{self.state}'
