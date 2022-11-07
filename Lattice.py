import random
import pygame as pg
from collections import namedtuple

from enums import DrawMode, NodeState
from Node import Node, node_colors


LatticeInfo = namedtuple('LatticeInfo', ['screen_width', 'screen_height', 'node_size'])


class Lattice:
    '''
    2D matrix, where each singular value is a node.
    '''

    def __init__(self, lattice_info: LatticeInfo):
        '''
        Initializes the lattice with nodes that are OFF.
        '''

        self.values = []
        self.info = lattice_info
        self.draw_mode = DrawMode.WALL
        self.node_size = self.info.node_size
        self.screen_width = self.info.screen_width
        self.screen_height = self.info.screen_height
        self.ncols = self.screen_width // self.node_size
        self.nrows = self.screen_height // self.node_size

        for _ in range(self.nrows):
            row = []
            for _ in range(self.ncols):
                row.append(Node())
            self.values.append(row)

    def clear_lattice(self):
        self.values = []

    def get_current_draw_mode(self):
        return self.draw_mode

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
        for r in range(0, self.info.screen_width, self.node_size):
            for c in range(0, self.screen_height, self.node_size):
                node = self.values[r // self.node_size][c // self.node_size]
                node_colour = node_colors[node.get_state()]
                pg.draw.rect(
                    screen, node_colour, pg.Rect(r, c, self.node_size, self.node_size)
                )
