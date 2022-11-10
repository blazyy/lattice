import random
import pygame as pg
from typing import Dict, List, Tuple
from collections import namedtuple

from enums import DrawMode, NodeState
from Node import Node, node_colours, Pos

ScreenDim = namedtuple('ScreenDim', ['w', 'h'])
LatticeDim = namedtuple('LatticeDim', ['nrows', 'ncols'])
LatticeInfo = namedtuple('LatticeInfo', ['screen_dim', 'node_size'])

DrawModeToNodeStateMapping = Dict[DrawMode, NodeState]
draw_mode_to_node_state_mapping: DrawModeToNodeStateMapping = {
    DrawMode.SET_WALL: NodeState.WALL,
    DrawMode.SET_ORIGIN: NodeState.ORIGIN,
    DrawMode.SET_VACANT: NodeState.VACANT,
    DrawMode.SET_GOAL: NodeState.GOAL,
}


class Lattice:
    '''
    2D array, where each singular value is of the class Node.
    '''

    def __init__(
        self,
        pg_screen: pg.Surface,
        lattice_info: LatticeInfo = LatticeInfo(ScreenDim(500, 500), 20),
    ) -> None:
        '''
        Initializes the lattice with nodes that have the value NodeState.VACANT.
        '''

        self.values = []
        self.info = lattice_info
        self.draw_mode = DrawMode.SET_WALL
        self.ncols = lattice_info.screen_dim.w // lattice_info.node_size
        self.nrows = lattice_info.screen_dim.h // lattice_info.node_size
        self.origin = None
        self.goal = None
        self.pg_screen = pg_screen

        for r in range(self.nrows):
            row = []
            for c in range(self.ncols):
                row.append(Node(Pos(r, c)))
            self.values.append(row)

    def get_info(self) -> LatticeInfo:
        '''
        Returns a namedtuple LatticeInfo containing three different pieces of information: The screen
        dimensions, and the node size.
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

    def get_origin(self) -> Node:
        '''
        Returns the origin node.
        '''

        return self.origin

    def get_goal(self) -> Node:
        '''
        Returns the goal node.
        '''

        return self.goal

    def get_draw_mode(self) -> DrawMode:
        '''
        Returns the current draw_mode. Depending on draw_mode, the state that a particular Node
        gets set to when change_node_state_on_user_input() is called will change.
        '''

        return self.draw_mode

    def set_draw_mode(self, new_draw_mode: DrawMode) -> None:
        '''
        Sets draw_mode to a newly provided draw mode.
        '''

        self.draw_mode = new_draw_mode

    def init_screen(self) -> None:
        '''
        Draws the initial lattice configuration, which is just the entire lattice with
        node states set to NodeState.VACANT.
        '''

        for x in range(0, self.info.screen_dim.w, self.info.node_size):
            for y in range(0, self.info.screen_dim.h, self.info.node_size):
                pg.draw.rect(
                    self.pg_screen,
                    node_colours[NodeState.VACANT],
                    pg.Rect(x, y, self.info.node_size, self.info.node_size),
                )
        pg.display.flip()

    def get_coords_from_pos(self, pos: Pos) -> Tuple[int, int]:
        '''
        Given a Pos tuple containing a node's row and column number, returns the x and y
        coordinate (top left) of that particular node.
        '''

        x, y = pos.r * self.info.node_size, pos.c * self.info.node_size
        return (x, y)

    def render_node(self, node: Node) -> pg.Rect:
        '''
        Renders the given node.
        '''

        pos = node.get_pos()
        x, y = self.get_coords_from_pos(pos)
        new_node_rect = pg.draw.rect(
            self.pg_screen,
            node_colours[node.get_state()],
            pg.Rect(x, y, self.info.node_size, self.info.node_size),
        )
        pg.display.update(new_node_rect)

    def update_node_state(self, node: Node, new_state: NodeState) -> None:
        '''
        Updates a node's state and renders it on the screen.
        '''

        node.set_state(new_state)
        self.render_node(node)

    def change_node_state_on_user_input(self, pos: Pos) -> None:
        '''
        Given the Pos tuple of a node, sets the node to a new state depending on draw_mode.
        This function is used for user-input: drawing walls, setting the goal and origin, etc.
        '''

        node = self.values[pos.r][pos.c]
        new_state = draw_mode_to_node_state_mapping[
            self.draw_mode
        ]  # Get the appropriate NodeState based on draw_mode.

        # Conditions below restrict only one origin node and one goal node to be set.
        if new_state == NodeState.ORIGIN:
            if not self.origin:
                self.origin = node
            else:
                return
        elif node.get_state() == NodeState.ORIGIN and new_state != NodeState.ORIGIN:
            self.origin = None
        elif new_state == NodeState.GOAL:
            if not self.goal:
                self.goal = node
            else:
                return
        elif node.get_state() == NodeState.GOAL and new_state != NodeState.GOAL:
            self.goal = None

        self.update_node_state(node, new_state)

    def get_neighbours(self, node: Node) -> List:
        '''
        Given a node, returns a list of all the neighbouring nodes.
        '''

        neighbours = []
        r, c = node.get_pos().r, node.get_pos().c
        if r > 0:
            neighbours.append(self.values[r - 1][c])
        if r < self.nrows - 1:
            neighbours.append(self.values[r + 1][c])
        if c > 0:
            neighbours.append(self.values[r][c - 1])
        if c < self.ncols - 1:
            neighbours.append(self.values[r][c + 1])
        return neighbours

    def display_path_to_origin(self, node) -> None:
        '''
        After a path is found (this method doesn't check for that!), this method traverses through
        the given node's predecessors until the origin is reached (which won't have a predecessor).
        Since visualization should be done from origin to goal, the results from the previous
        step is added to a list which would be reversed, and then would be visualized.
        '''

        path = []
        while node.get_predecessor():  # Prints the path from goal to origin
            if node.get_state() not in [
                NodeState.ORIGIN,
            ]:  # Doesn't overrwrite states of the origin and the goal
                path.append(node)
            node = node.get_predecessor()

        path.reverse()
        for node in path:
            self.update_node_state(node, NodeState.PATH)

    def dfs(self) -> bool:
        '''
        Does a Depth-first Search from the given origin node to the goal node. The preference of
        the direction the DFS takes is influenced by the get_neighbours() function. Depending on
        the order of the if conditions, this direction might be changed.
        '''

        stack = [self.origin]
        while stack:
            node = stack.pop()
            if node == self.goal:
                self.display_path_to_origin(node)
                return True
            if node.get_state() not in [NodeState.WALL, NodeState.VISITED]:
                self.update_node_state(
                    node, NodeState.VISITED
                ) if node.get_state() != NodeState.ORIGIN else ''
                for neighbour in self.get_neighbours(node):
                    if neighbour.get_state() not in [
                        NodeState.WALL,
                        NodeState.VISITED,
                        NodeState.ORIGIN,
                    ]:
                        neighbour.set_predecessor(
                            node
                        )  # When adding a neighbour to the stack, mark the predecessor as the current node so that we have a route back to the origin once the goal is found
                        stack.append(neighbour)
        return False

    def bfs(self) -> bool:
        '''
        Does a Breadth-first Search from the given origin node to the goal node.
        '''

        queue = [self.origin]
        while queue:
            for _ in range(len(queue)):
                node = queue.pop(0)
                if node == self.goal:
                    self.display_path_to_origin(node)
                    return True
                if node.get_state() not in [
                    NodeState.WALL,
                    NodeState.VISITED,
                ]:  # If node isn't visited or isn't a wall, mark as visited, if isn't isn't an origin node. Also, note to self: I was confused as to why we need to check if
                    # a node is visited or not again when we're already checking for that below when adding the neighbours into the queue. The reason is because a particular
                    # node might exist in the queue at a certain point in time more than once. I.e. node c being a neighbour of a, node c being a neighbour of b, and node
                    # b being a neighbour of a. When a is being processed, c will be added. Next, when b is processed, c will also be added. Since the same node can be added
                    # multiple times into the queue, we need to check if it's visited again.
                    self.update_node_state(
                        node, NodeState.VISITED
                    ) if node.get_state() != NodeState.ORIGIN else ''
                    for neighbour in self.get_neighbours(node):
                        if neighbour.get_state() not in [
                            NodeState.WALL,
                            NodeState.VISITED,
                            NodeState.ORIGIN,  # As far as I can tell, the last state (NodeState.ORIGIN) is only in this list for BFS because a predecessor was being set on the origin node,
                            # which isn't supposed to happen. We don't need to check if state is NodeState.GOAL because algorithm terminates immediately when the goal node is found
                        ]:
                            neighbour.set_predecessor(node)
                            queue.append(neighbour)
        return False

    def clear(self) -> None:
        '''
        Sets all nodes in the lattice to the state NodeState.VACANT, and also resets the origin
        and goal nodes to None.
        '''

        self.origin = None
        self.goal = None
        for r in range(self.nrows):
            for c in range(self.ncols):
                self.values[r][c].reset()
        self.init_screen()
