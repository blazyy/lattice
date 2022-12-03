from __future__ import (
    annotations,
)  # Used for type hinting to set type of class method to class itself, i.e. in set_predecessor() function below.
from colour import Color
from collections import namedtuple

from enums import NodeState
from typing import Optional

Pos = namedtuple('Pos', ['r', 'c'])

NUM_COLOURS_IN_TRANSITION = (
    999  # Make sure this is an odd number lol, else program might go kaboom
)

node_colour_ranges = {
    NodeState.WALL: ['#000500'],
    NodeState.VACANT: ['#FAF0CA'],
    NodeState.ORIGIN: ['green'],
    NodeState.GOAL: ['red'],
    # NodeState.VISITED: [
    #     'fbf8cc',
    #     'fde4cf',
    #     'ffcfd2',
    #     'f1c0e8',
    #     'cfbaf0',
    #     'a3c4f3',
    #     '90dbf4',
    #     '8eecf5',
    #     '98f5e1',
    #     'b9fbc0',
    # ],
    NodeState.VISITED: [
        '16DB65',
        '058C42',
        '04471C',
    ],
    NodeState.PATH: ['#ffd100', '#ffee32'],
}

# Code below generates the appropriate number of transition colours depending on the number of colours specified in the range above
node_colours = {}
for node_state, colour_range_colours in node_colour_ranges.items():
    num_colours_in_colour_range = len(colour_range_colours)
    if num_colours_in_colour_range > 1:
        colours = []
        for i in range(num_colours_in_colour_range):
            if i + 1 < num_colours_in_colour_range:
                start_colour = colour_range_colours[i]
                start_colour = f'{"#" if "#" not in start_colour else ""}{start_colour}'  # Handles case if # is not present in specified colour range hex value
                end_colour = colour_range_colours[i + 1]
                end_colour = f'{"#" if "#" not in end_colour else ""}{end_colour}'
                colours.extend(
                    map(
                        lambda color: color.hex_l,
                        Color(start_colour).range_to(
                            Color(end_colour),
                            NUM_COLOURS_IN_TRANSITION
                            // (num_colours_in_colour_range - 1)
                            if num_colours_in_colour_range > 2
                            else NUM_COLOURS_IN_TRANSITION,
                        ),
                    )
                )
        # The 3 lines below are only needed because if there are more than 2 colours in a given NodeState's colour transition,
        # the above code that adds the colour gradient between two colours doesn't exactly sum up to NUM_COLOURS_IN_TRANSITION
        # at the end. This means the last few colours in a given transition will be the same, but it is pretty much
        # unnoticeable if the value of NUM_COLOURS_IN_TRANSITION is high
        num_colours_left = NUM_COLOURS_IN_TRANSITION - len(colours)
        fillers = [colours[len(colours) - 1] for _ in range(num_colours_left)]
        colours.extend(fillers)
        node_colours[node_state] = colours
    else:
        node_colours[node_state] = colour_range_colours


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
        self.heuristic = None
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

    def get_heuristic(self) -> float:
        '''
        Returns the heuristic value for a particular Node.
        In this implementation, it is Euclidean distance.
        '''

        return self.heuristic

    def set_heuristic(self, val) -> None:
        '''
        Sets the heuristic value for a particular node.
        In this implementation, it is Euclidean distance.
        '''

        self.heuristic = val

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

    def get_colour(self, render_number: int) -> str:
        '''
        Given the number which represents it's nth render, returns the appropriate colour.
        render_number exists in the range (1, NUM_COLOURS_IN_TRANSITION - 1).
        '''

        if render_number is None:
            return node_colours[self.state][0]
        return node_colours[self.state][render_number - 1]

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
