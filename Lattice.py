import math
import random
import pygame as pg
from typing import Dict, List, Tuple, Optional
from collections import namedtuple, defaultdict

from enums import DrawMode, NodeState, PathfindingOption
from Node import Node, NUM_COLOURS_IN_TRANSITION, Pos, node_colour_ranges

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

NODE_STATES_WITH_TRANSITION_COLOURS = [
    node_state
    for node_state in node_colour_ranges
    if len(node_colour_ranges[node_state]) > 1
]


class Lattice:
    '''
    2D array, where each singular value is of the class Node.
    '''

    def __init__(self, pg_screen: pg.surface.Surface, lattice_info) -> None:
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
        self.previously_rendered_nodes = (
            {}
        )  # Contains nodes which have been rendered since beginning of the animation. Used to enable gradient animation on nodes as visualization progresses

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

    def get_origin(self) -> Optional[Node]:
        '''
        Returns the origin node.
        '''

        return self.origin

    def get_goal(self) -> Optional[Node]:
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

    def get_node_coords(self, node: Node) -> Tuple[int, int]:
        '''
        Given a node, returns it's x and y coordinates (top left).
        '''

        pos = node.get_pos()
        x, y = pos.r * self.info.node_size, pos.c * self.info.node_size
        return (x, y)

    def get_rect_from_node(self, node: Node) -> pg.rect.Rect:
        '''
        Gets a pygame Rect object from a given node.
        '''

        x, y = self.get_node_coords(node)
        render_number = self.previously_rendered_nodes.get(node, None)
        colour = node.get_colour(render_number)
        rect = pg.draw.rect(
            self.pg_screen,
            colour,
            pg.Rect(x, y, self.info.node_size, self.info.node_size),
        )
        return rect

    def draw(self) -> None:
        '''
        Draws the lattice configuration.
        '''

        new_rects = []
        for r in range(self.nrows):
            for c in range(self.ncols):
                node = self.get_node(r, c)
                new_rect = self.get_rect_from_node(node)
                new_rects.append(new_rect)
        pg.display.update(new_rects)  # type: ignore

    def render_nodes(self, nodes: List[Node]) -> None:
        '''
        Renders the given nodes. Leaves rest of the screen untouched (i.e. same as the last render)
        '''

        node_rects = []
        for node in nodes:
            node_rects.append(self.get_rect_from_node(node))
        pg.display.update(node_rects)

    def handle_node_rendering(self, latest_rendered_node: Optional[Node] = None):
        '''
        Handles rendering a node once it's state has been updated. Also handles the colour transitions for all
        the previously generated nodes. If the latest rendered node is not provided, it means the function doesn't
        handle newer nodes but transitions the colours of already rendered nodes to the last colour so that all node's
        of a particular state change to be the same colour.
        '''

        # Nodes which have already reached the last colour in the transition phase, after which they don't need to be updated, so they can be removed from self.previously_rendered_nodes
        if latest_rendered_node:
            self.previously_rendered_nodes[
                latest_rendered_node
            ] = 0  # Set to 0 here, but will be set to 1 in the for loop below. Every node in this dictionary will be added in this line, one at a time each subsequent render.
        nodes_to_update = []  # Nodes to update using pg.display.update()
        last_state_nodes = []
        # Loops through all nodes that were rendered before current render, and if the number of renders a previously rendered node has been through is less
        # than NUM_COLOURS_IN_TRANSITION, re-render node. If node has been through enough renders, we stop updating it, which is what last_state_nodes contains.
        for node in self.previously_rendered_nodes:
            # Make sure the NodeStates in the list below correspond to NodeStates which have more than one colour in node_colours (in Node.py)
            if node.get_state() in NODE_STATES_WITH_TRANSITION_COLOURS:
                self.previously_rendered_nodes[node] += 1
            else:
                last_state_nodes.append(
                    node
                )  # If a node's state doesn't need a colour transition, it has finished rendering and therefore should not be rendered anymore.
            if self.previously_rendered_nodes[node] == NUM_COLOURS_IN_TRANSITION - 1:
                last_state_nodes.append(node)
            else:
                nodes_to_update.append(node)

        # Separate for loop because we can't delete dictionary keys while iterating through the dictionary
        for node in last_state_nodes:
            self.previously_rendered_nodes.pop(node)

        self.render_nodes(nodes_to_update)

    def update_node_state_and_render(self, node: Node, new_state: NodeState) -> None:
        '''
        Updates a node's state and renders it on the screen.
        '''

        if self.get_origin() == node and new_state != NodeState.ORIGIN:
            self.origin = None
        if self.get_goal() == node and new_state != NodeState.GOAL:
            self.goal = None
        node.set_state(new_state)
        self.handle_node_rendering(node)

    def handle_end_transitions(self) -> None:
        '''
        After a visualization finishes, node's colour transitions need to be completed, i.e. all nodes of a certain
        NodeState should end on the same colour.
        '''

        while len(self.previously_rendered_nodes):
            self.handle_node_rendering()

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
            if self.origin:
                self.update_node_state_and_render(self.origin, NodeState.VACANT)
            self.origin = node
        elif new_state == NodeState.GOAL:
            if self.goal:
                self.update_node_state_and_render(self.goal, NodeState.VACANT)
            self.goal = node

        self.update_node_state_and_render(node, new_state)

    def get_neighbours(self, node: Node) -> List[Node]:
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
                NodeState.GOAL,
            ]:  # Doesn't overrwrite states of the origin and the goal
                path.append(node)
            node = node.get_predecessor()

        path.reverse()
        for node in path:
            self.update_node_state_and_render(node, NodeState.PATH)

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
            if node and node.get_state() not in [
                NodeState.WALL,
                NodeState.VISITED,
            ]:  # The `if node` is just to suppress mypy warnings
                self.update_node_state_and_render(
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
                if node and node.get_state() not in [
                    NodeState.WALL,
                    NodeState.VISITED,
                ]:  # If node isn't visited or isn't a wall, mark as visited, if isn't isn't an origin node. Also, note to self: I was confused as to why we need to check if
                    # a node is visited or not again when we're already checking for that below when adding the neighbours into the queue. The reason is because a particular
                    # node might exist in the queue at a certain point in time more than once. I.e. node c being a neighbour of a, node c being a neighbour of b, and node
                    # b being a neighbour of a. When a is being processed, c will be added. Next, when b is processed, c will also be added. Since the same node can be added
                    # multiple times into the queue, we need to check if it's visited again.
                    self.update_node_state_and_render(
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

    def dijkstra(self) -> bool:
        '''
        Finds a path from origin to goal. Currently, squares on a grid cannot be assigned weights (they can, but it's hard to visualize).
        Because of this, weights between nodes are all by default to 1.

        This implementation, instead of using a priority queue, uses a mapping (defauldict with default distance of infinity) of a node to its distance.
        A Node object's state is internal, so we do not need to check externally whether or node a node has been visited through the use of a typical priority queue.
        We can just check if a node's state has been marked as visited, compared to the typical implementation where we check if it exists in a priority queue.
        '''

        dist = defaultdict(lambda: float('inf'))
        dist[self.origin] = 0
        node = self.origin
        while True:
            if node.get_state() != NodeState.ORIGIN:
                self.update_node_state_and_render(node, NodeState.VISITED)
            neighbours = self.get_neighbours(node)
            unvisited_neighbours = list(
                filter(
                    lambda n: n.get_state()
                    not in [NodeState.VISITED, NodeState.ORIGIN, NodeState.WALL],
                    neighbours,
                )
            )
            for neighbour in unvisited_neighbours:
                if (
                    dist[node] + 1 < dist[neighbour]
                ):  # If current distance to a node is smaller than any previous possible distance, update it. Every node is only 1 node away from other nodes due to the fact that this is a nxn grid with no weights.
                    dist[neighbour] = dist[node] + 1
                    neighbour.set_predecessor(
                        node
                    )  # Whenever we visit a node, mark the predecessor so that when a path is found, we can backtrack back to origin.
                if neighbour == self.goal:
                    self.display_path_to_origin(neighbour)
                    return True
            # "Priority Queue"
            smallest_path_dist, smallest_path_node = float('inf'), None
            for node in dist.keys():
                if dist[node] < smallest_path_dist and node.get_state() not in [
                    NodeState.VISITED,
                    NodeState.ORIGIN,
                    NodeState.WALL,
                ]:
                    smallest_path_dist = dist[node]
                    smallest_path_node = node
            node = smallest_path_node
            if not node:
                break

    def a_star(self) -> bool:
        '''
        Finds a path from origin to goal. Currently, squares on a grid cannot be assigned weights (they can, but it's hard to visualize).
        Because of this, weights between nodes are all by default to 1. Heuristic is euclidean distance, by assuming lattice nodes exist
        in the 4th quadrant of an axis. This is why the y co-ords are negated, although I'm not sure it makes much of a difference.

        The heuristic is only considered when choosing which node to select out of a node's neighbours. We do not add it to the distance
        when updating distance from origin node.
        '''

        dist = defaultdict(lambda: float('inf'))
        dist[self.origin] = 0
        node = self.origin

        # Calculating the initial heuristic values using Euclidean distances
        goal_pos = self.get_goal().get_pos()
        x1, y1 = goal_pos.r, -goal_pos.c
        for r in range(self.nrows):
            for c in range(self.ncols):
                node_pos = self.get_node(r, c).get_pos()
                x2, y2 = node_pos.r, -node_pos.c
                euclid_distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                self.get_node(r, c).set_heuristic(euclid_distance)

        while True:
            if node.get_state() != NodeState.ORIGIN:
                self.update_node_state_and_render(node, NodeState.VISITED)
            neighbours = self.get_neighbours(node)
            unvisited_neighbours = list(
                filter(
                    lambda n: n.get_state()
                    not in [NodeState.VISITED, NodeState.ORIGIN, NodeState.WALL],
                    neighbours,
                )
            )
            for neighbour in unvisited_neighbours:
                if (
                    dist[node] + 1 < dist[neighbour]
                ):  # If current distance to a node is smaller than any previous possible distance, update it. Every node is only 1 node away from other nodes due to the fact that this is a nxn grid with no weights.
                    dist[neighbour] = dist[node] + 1
                    neighbour.set_predecessor(
                        node
                    )  # Whenever we visit a node, mark the predecessor so that when a path is found, we can backtrack back to origin.
                if neighbour == self.goal:
                    self.display_path_to_origin(neighbour)
                    return True
            # "Priority Queue"
            smallest_path_dist, smallest_path_node = float('inf'), None
            for node in dist.keys():
                if dist[
                    node
                ] + node.get_heuristic() < smallest_path_dist and node.get_state() not in [
                    NodeState.VISITED,
                    NodeState.ORIGIN,
                    NodeState.WALL,
                ]:
                    smallest_path_dist = dist[node] + node.get_heuristic()
                    smallest_path_node = node
            node = smallest_path_node
            if not node:
                break

    def randomize(self, density: float) -> None:
        '''
        Randomly sets a node to a wall, depending on the density amount specified. Think of
        this as the probability of a certain node being set to a wall.
        '''

        self.clear()
        new_rects = []
        for r in range(self.nrows):
            for c in range(self.ncols):
                if random.uniform(0, 1) < density:
                    node = self.get_node(r, c)
                    node.set_state(NodeState.WALL)
                    new_rect = self.get_rect_from_node(node)
                    new_rects.append(new_rect)
        pg.display.update(new_rects)  # type: ignore

    def fill(self) -> None:
        '''
        Fills the entire grid with walls, i.e. sets all nodes to the state NodeState.WALL.
        '''

        self.clear()
        self.origin = None
        self.goal = None
        for r in range(self.nrows):
            for c in range(self.ncols):
                self.values[r][c].set_state(NodeState.WALL)
        self.draw()

    def get_one_off_neighbours(self, node: Node) -> List:
        '''
        Given a node, returns a list of all the neighbouring nodes one node away. Used in maze
        generation to skip a node due to the algorithm working backwards- i.e. making nodes
        vacant from an initially fully filled maze.
        '''

        neighbours = []
        r, c = node.get_pos().r, node.get_pos().c
        if r > 1:
            neighbours.append(self.get_node(r - 2, c))
        if r < self.nrows - 2:
            neighbours.append(self.get_node(r + 2, c))
        if c > 1:
            neighbours.append(self.get_node(r, c - 2))
        if c < self.ncols - 2:
            neighbours.append(self.get_node(r, c + 2))
        return neighbours

    def get_node_between(self, node_a: Node, node_b: Node) -> Node:
        '''
        Given two nodes on the same row/column, returns the node that is in between the two of
        these nodes.
        '''

        node_a_pos = node_a.get_pos()
        node_b_pos = node_b.get_pos()
        if node_a_pos.r == node_b_pos.r:
            r, c = (
                node_a_pos.r,
                min(node_a_pos.c, node_b_pos.c) + 1,
            )  # If both nodes are on the same row, return the node in the middle (i.e. different column)
        elif node_a_pos.c == node_b_pos.c:
            r, c = (
                min(node_a_pos.r, node_b_pos.r) + 1,
                node_a_pos.c,
            )  # If both nodes are on the same row, return the node in the middle (i.e. different row)
        return self.get_node(r, c)

    def generate_maze(self) -> None:
        '''
        Generates a maze using an iterative version of recrusive backtracking (using DFS). Usually, maze generation
        algorithms shown on Wikipedia were algorithms meant for walls with "0" thickness, but since in my implementation
        the walls and nodes are of the same size, I had to write some code to accodomate for this- i.e. self.get_one_off_neighbours()
        which considers only neighbours that are one row or column away, and also self.get_node_between() which gets a node that's
        inbetween two nodes, in order to turn it from a wall state to a vacant state.

        Algorithm (adapted from wikipedia, under the randomized depth-first search - iterative implementation section):

        1) Choose the initial cell (random choice), make it vacant and push it to the stack
        2) While the stack is not empty:
            1) Pop from the stack and make it a current cell
            2) If the current cell has any neighbours which have not been visited
                1) Push the current cell to the stack
                2) Choose one of the unvisited neighbours
                3) Remove the wall between the current cell and the chosen cell (i.e. make it vacant)
                4) Mark the chosen cell as visited and push it to the stack
        '''

        self.fill()
        r, c = random.randint(0, self.nrows - 2), random.randint(
            0, self.ncols - 2
        )  # -2 because the corner nodes are walls and we don't want to choose one of those for our starting path
        node = self.get_node(1, 1)
        stack = [node]
        self.update_node_state_and_render(node, NodeState.VACANT)
        while stack:
            node = stack.pop()
            neighbours = self.get_one_off_neighbours(node)
            unvisited_neighbours = list(
                filter(lambda x: x.get_state() != NodeState.VACANT, neighbours)
            )
            if unvisited_neighbours:
                stack.append(node)
                rand_unvisited_neighbour = random.choice(unvisited_neighbours)
                node_between = self.get_node_between(node, rand_unvisited_neighbour)

                # if rand_unvisited_neighbour.get_pos().r in [1, self.nrows - 1] or rand_unvisited_neighbour.get_pos().c in [1, self.ncols -1 ]:
                #     print('RANDO!!')
                # if node_between.get_pos().r in [1, self.nrows - 1] or node_between.get_pos().c in [1, self.ncols -1 ]:
                #     print('BETWE!!')

                self.update_node_state_and_render(node_between, NodeState.VACANT)
                self.update_node_state_and_render(
                    rand_unvisited_neighbour, NodeState.VACANT
                )
                stack.append(rand_unvisited_neighbour)
        self.draw()

    def get_num_live_neighbours(self, neighbour_indices: List[Tuple[int, int]]) -> int:
        '''
        From all the neighbours of a particular cell, returns the number of cells which have the state NodeState.WALL.
        '''

        num_live_neighbours = 0
        for neighbour_index in neighbour_indices:
            r, c = neighbour_index
            if self.values[r][c].get_state() == NodeState.WALL:
                num_live_neighbours += 1
        return num_live_neighbours

    def clear_certain_state_nodes(self, states_to_clear: List[NodeState]) -> None:
        '''
        Resets nodes with given state(s) to NodeState.VACANT.
        '''

        for r in range(self.nrows):
            for c in range(self.ncols):
                node = self.values[r][c]
                if node.get_state() in states_to_clear:
                    node.set_state(NodeState.VACANT)
        self.draw()

    def game_of_life(self) -> None:
        '''
        Starts an emulation of Conway's Game of Life. NodeState.WALL is considered a live cell, NodeState.VACANT
        is considered a dead cell.

        Rules:
        1) Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        2) Any live cell with two or three live neighbours lives on to the next generation.
        3) Any live cell with more than three live neighbours dies, as if by overpopulation.
        4) Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        '''

        # 2 lines immediately below are in case someone starts a visualization after doing a pathfinding visualization
        self.origin, self.goal = None, None
        self.clear_certain_state_nodes(
            [NodeState.VISITED, NodeState.PATH, NodeState.ORIGIN, NodeState.GOAL]
        )

        # Pre-calculating neighbour indices, so that it isn't done every generation. Sure, uses a lot more storage but that isn't a bottleneck.
        positions = [
            [0, 1],
            [0, -1],
            [1, -1],
            [-1, 1],
            [1, 1],
            [-1, -1],
            [1, 0],
            [-1, 0],
        ]
        all_neighbour_indices = {}
        for r in range(self.nrows):
            for c in range(self.ncols):
                neighbour_indices = []
                for position in positions:
                    new_r = r + position[0]
                    new_c = c + position[1]
                    if (
                        new_r >= 0
                        and new_r < self.nrows
                        and new_c >= 0
                        and new_c < self.ncols
                    ):
                        neighbour_indices.append([new_r, new_c])
                all_neighbour_indices[self.values[r][c]] = neighbour_indices

        prev_nodes_to_update = []  # Checks if evolution has stopped.
        evolution_stopped = False
        while not evolution_stopped:
            batch_update_list = (
                []
            )  # Since each generation is a pure function of the preceding one, we have to update the node states only after going through all of them once.
            # A node's next-generation state shouldn't influence any current-generation node's state.
            for r in range(self.nrows):
                for c in range(self.ncols):
                    node = self.get_node(r, c)
                    neighbour_indices = all_neighbour_indices[node]
                    num_live_neighbours = self.get_num_live_neighbours(
                        neighbour_indices
                    )
                    is_node_alive = node.get_state() == NodeState.WALL
                    if is_node_alive:
                        if num_live_neighbours < 2 or num_live_neighbours > 3:
                            batch_update_list.append([node, NodeState.VACANT])
                    elif not is_node_alive and num_live_neighbours == 3:
                        batch_update_list.append([node, NodeState.WALL])
            nodes_to_update = []
            for item in batch_update_list:
                node, new_state = item
                node.set_state(new_state)
                nodes_to_update.append(node)

            # Takes care of termination state. I wrote this in a jiffy and I don't know how it works and I'm too lazy to try understanding. But hey, it works. So I'm not touching it.
            for item in prev_nodes_to_update:
                if nodes_to_update == item:
                    evolution_stopped = True
            if len(prev_nodes_to_update) == 1:
                prev_nodes_to_update.pop(0)
            prev_nodes_to_update.append(nodes_to_update)

            self.render_nodes(nodes_to_update)

    def clear(self) -> None:
        '''
        Sets all nodes in the lattice to the state NodeState.VACANT, and also resets the origin
        and goal nodes to None.
        '''

        self.origin, self.goal = None, None
        self.previously_rendered_nodes = {}
        for r in range(self.nrows):
            for c in range(self.ncols):
                self.values[r][c].reset()
        self.draw()

    def visualize(self, option: PathfindingOption):
        if self.get_goal() and self.get_origin():
            path_found = None
            self.previously_rendered_nodes = {}
            self.clear_certain_state_nodes([NodeState.VISITED, NodeState.PATH])
            if option == PathfindingOption.DFS:
                path_found = self.dfs()
            elif option == PathfindingOption.BFS:
                path_found = self.bfs()
            elif option == PathfindingOption.DIJKSTRA:
                path_found = self.dijkstra()
            elif option == PathfindingOption.A_STAR:
                path_found = self.a_star()
            # I decided to not transition the colours in the end because of two reasons: 1)
            # You can't give input to the game even after the path has been found and while
            # the animations are still happening. This is bad use experience. And 2) It can
            # be useful to see the path convergence history through colour gradients.
            # If you want to enable, just uncomment the line below.
            # self.handle_end_transitions()
            print('Path found') if path_found else print('Path not found!')
        else:
            print('Origin and goal not set!')
