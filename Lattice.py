import random
import pygame as pg
from typing import Dict
from collections import namedtuple

from enums import DrawMode, NodeState
from Node import Node, node_colors

LatticeDim = namedtuple('LatticeDim', ['nrows', 'ncols'])
ScreenDim = namedtuple('ScreenDim', ['w', 'h'])
LatticeInfo = namedtuple('LatticeInfo', ['screen_dim', 'node_size'])

DrawModeToNodeStateMapping = Dict[DrawMode, NodeState]

draw_mode_to_node_state_mapping: DrawModeToNodeStateMapping = {
    DrawMode.SET_WALL: NodeState.WALL,
    DrawMode.SET_ORIGIN: NodeState.ORIGIN,
    DrawMode.SET_VACANT: NodeState.VACANT,
}


class Lattice:
    '''
    2D matrix, where each singular value is a node.
    '''

    def __init__(
        self, lattice_info: LatticeInfo = LatticeInfo(ScreenDim(500, 500), 20)
    ) -> None:
        '''
        Initializes the lattice with nodes that are OFF.
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
        return self.info

    def get_dim(self) -> LatticeDim:
        return LatticeDim(self.nrows, self.ncols)

    def get_draw_mode(self) -> DrawMode:
        return self.draw_mode

    def set_draw_mode(self, new_draw_mode: DrawMode) -> None:
        self.draw_mode = new_draw_mode

    def randomize(self) -> None:
        '''
        Resets current lattice state and randomly initializes each node to either be NodeState.ON or NodeState.OFF.
        '''

        self.clear_lattice()
        for _ in range(self.nrows):
            row = []
            for _ in range(self.ncols):
                row.append(Node(random.choice([state for state in [NodeState.WALL, NodeState.VACANT]])))
            self.values.append(row)

    def get_node(self, r: int, c: int) -> Node:
        '''
        Given the row and column index, returns the specific node from the entire lattice.
        '''

        return self.values[r][c]

    def change_node_state(self, r: int, c: int) -> None:
        new_state = draw_mode_to_node_state_mapping[self.draw_mode]
        self.values[r][c].set_state(new_state)

    def draw(self, screen: pg.Overlay) -> None:
        for r in range(0, self.info.screen_dim.w, self.info.node_size):
            for c in range(0, self.info.screen_dim.h, self.info.node_size):
                node = self.values[r // self.info.node_size][c // self.info.node_size]
                node_colour = node_colors[node.get_state()]
                pg.draw.rect(
                    screen,
                    node_colour,
                    pg.Rect(r, c, self.info.node_size, self.info.node_size),
                )

    def clear_lattice(self) -> None:
        self.values = []
