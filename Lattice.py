import random
import pygame as pg
from collections import namedtuple

from enums import DrawMode, NodeState
from Node import Node, node_colors


ScreenDim = namedtuple('ScreenDim', ['w', 'h'])
LatticeInfo = namedtuple('LatticeInfo', ['screen_dim', 'node_size'])


class Lattice:
    '''
    2D matrix, where each singular value is a node.
    '''

    def __init__(
        self, lattice_info: LatticeInfo = LatticeInfo(ScreenDim(500, 500), 20)
    ):
        '''
        Initializes the lattice with nodes that are OFF.
        '''

        self.values = []
        self.info = lattice_info
        self.draw_mode = DrawMode.WALL
        self.ncols = lattice_info.screen_dim.w // lattice_info.node_size
        self.nrows = lattice_info.screen_dim.h // lattice_info.node_size

        for _ in range(self.nrows):
            row = []
            for _ in range(self.ncols):
                row.append(Node())
            self.values.append(row)

    def clear_lattice(self):
        self.values = []

    def get_draw_mode(self):
        return self.draw_mode

    def get_info(self):
        return self.info

    def get_dim(self):
        return

    def randomize(self):
        '''
        Resets current lattice state and randomly initializes each node to either be NodeState.ON or NodeState.OFF.
        '''

        self.clear_lattice()
        for _ in range(self.nrows):
            row = []
            for _ in range(self.ncols):
                row.append(Node(random.choice([state for state in NodeState])))
            self.values.append(row)

    def get_node(self, r: int, c: int):
        '''
        Given the row and column index, returns the specific node from the entire lattice.
        '''

        return self.values[r][c]

    def flip_node_state(self, r: int, c: int, draw_mode: DrawMode):
        self.values[r][c].flip_state(draw_mode)

    def draw(self, screen: pg.display):
        for r in range(0, self.info.screen_dim.w, self.info.node_size):
            for c in range(0, self.info.screen_dim.h, self.info.node_size):
                node = self.values[r // self.info.node_size][c // self.info.node_size]
                node_colour = node_colors[node.get_state()]
                pg.draw.rect(
                    screen,
                    node_colour,
                    pg.Rect(r, c, self.info.node_size, self.info.node_size),
                )
