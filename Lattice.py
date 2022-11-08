import random
import pygame as pg
from typing import Dict
from collections import namedtuple

from enums import DrawMode, NodeState
from Node import Node, node_colors

ScreenDim = namedtuple('ScreenDim', ['w', 'h'])
LatticeDim = namedtuple('LatticeDim', ['nrows', 'ncols'])
LatticeInfo = namedtuple('LatticeInfo', ['screen_dim', 'node_size'])

DrawModeToNodeStateMapping = Dict[DrawMode, NodeState]
draw_mode_to_node_state_mapping: DrawModeToNodeStateMapping = {
    DrawMode.SET_WALL: NodeState.WALL,
    DrawMode.SET_ORIGIN: NodeState.ORIGIN,
    DrawMode.SET_VACANT: NodeState.VACANT,
}


class Lattice:
    '''
    2D array, where each singular value is of the class Node.
    '''

    def __init__(
        self, lattice_info: LatticeInfo = LatticeInfo(ScreenDim(500, 500), 20)
    ) -> None:
        '''
        Initializes the lattice with nodes that have the value NodeState.VACANT.
        '''

        self.values = []
        self.info = lattice_info
        self.draw_mode = DrawMode.SET_WALL
        self.ncols = lattice_info.screen_dim.w // lattice_info.node_size
        self.nrows = lattice_info.screen_dim.h // lattice_info.node_size

        for _ in range(self.nrows):
            row = []
            for _ in range(self.ncols):
                row.append(Node())
            self.values.append(row)

    def get_info(self) -> LatticeInfo:
        '''
        Returns a namedtuple LatticeInfo containing three different pieces of information: The screen dimensions, and the node size.
        '''

        return self.info

    def get_dim(self) -> LatticeDim:
        '''
        Returns a namedtuple LatticeDim containing the number of rows and number of columns in the lattice.
        This value is determined by both the window dimensions and the node size.
        '''

        return LatticeDim(self.nrows, self.ncols)

    def get_node(self, r: int, c: int) -> Node:
        '''
        Given the row and column index, returns the specific node from the 2D array of values.
        '''

        return self.values[r][c]

    def get_draw_mode(self) -> DrawMode:
        '''
        Returns the current draw_mode.
        Depending on draw_mode, the state that a particular Node gets set to when change_node_state() is called will change.
        '''

        return self.draw_mode

    def set_draw_mode(self, new_draw_mode: DrawMode) -> None:
        '''
        Sets draw_mode to a newly provided draw mode.
        '''

        self.draw_mode = new_draw_mode

    def randomize(self) -> None:
        '''
        Resets all nodes in current lattice to the state NodeState.VACANT, and randomly initializes each node to either be NodeState.VACANT or NodeState.WALL.
        Nodes are set to NodeState.VACANT and not entirely replaced to keep the original object intact. Sounds like a good thing to do.
        '''

        self.clear()
        for _ in range(self.nrows):
            row = []
            for _ in range(self.ncols):
                row.append(
                    Node(
                        random.choice(
                            [state for state in [NodeState.WALL, NodeState.VACANT]]
                        )
                    )
                )
            self.values.append(row)

    def change_node_state(self, r: int, c: int) -> None:
        '''
        Given the row and column number, sets the node to a new state depending on draw_mode.
        '''

        new_state = draw_mode_to_node_state_mapping[self.draw_mode]
        self.values[r][c].set_state(new_state)

    def draw(self, screen: pg.Overlay) -> None:
        '''
        Given pygame's Overlay object, i.e. the screen, draws the current lattice configuration.
        The colour of the nodes is dependent on the node_colors dictionary.
        '''

        for r in range(0, self.info.screen_dim.w, self.info.node_size):
            for c in range(0, self.info.screen_dim.h, self.info.node_size):
                node = self.values[r // self.info.node_size][c // self.info.node_size]
                node_colour = node_colors[node.get_state()]
                pg.draw.rect(
                    screen,
                    node_colour,
                    pg.Rect(r, c, self.info.node_size, self.info.node_size),
                )

    def clear(self) -> None:
        '''
        Sets all nodes in the lattice to the state NodeState.VACANT.
        '''

        for r in range(self.nrows):
            for c in range(self.ncols):
                self.values[r][c].set_state(NodeState.VACANT)
