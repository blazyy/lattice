import sys
import time
import pygame as pg

pg.init()

from typing import Dict
from Node import Node
from enums import DrawMode, NodeState
from Lattice import Lattice, LatticeInfo, ScreenDim


EventKeyToDrawModeMapping = Dict[int, DrawMode]
event_key_to_draw_mode_mapping = {
    pg.K_o: DrawMode.SET_ORIGIN,
    pg.K_e: DrawMode.SET_VACANT,
    pg.K_g: DrawMode.SET_GOAL,
}

screen_dim = ScreenDim(500, 500)
lattice_info = LatticeInfo(screen_dim, 20)

clock = pg.time.Clock()
mouse = pg.mouse.set_cursor(pg.cursors.tri_left)
screen = pg.display.set_mode((lattice_info.screen_dim.w, lattice_info.screen_dim.h))

mouse_pressed = False
current_draw_mode = DrawMode.SET_WALL

lattice = Lattice(lattice_info)


def update_screen():
    lattice.draw(screen)
    pg.display.flip()


def display_path_to_origin(node):
    while node.get_predecessor():  # Prints the path from goal to origin
        if node.get_state() not in [
            NodeState.ORIGIN,
            NodeState.GOAL,
        ]:  # Doesn't overrwrite states of the origin and the goal
            node.set_state(NodeState.PATH)
        update_screen()
        node = node.get_predecessor()


def dfs(lattice: Lattice, origin: Node, goal: Node):
    stack = [origin]
    while stack:
        node = stack.pop()
        if node == goal:
            display_path_to_origin(node)
            print('DFS: Path found!')
            return True
        if node.get_state() not in [NodeState.WALL, NodeState.VISITED]:
            if node.get_state() not in [
                NodeState.ORIGIN,
                NodeState.GOAL,
            ]:  # Only set as visited if the node isn't origin/goal. This is because origin/goal nodes are never set to visited.
                node.set_state(NodeState.VISITED)
            update_screen()
            for neighbour in lattice.get_neighbours(node):
                if neighbour.get_state() not in [NodeState.WALL, NodeState.VISITED]:
                    neighbour.set_predecessor(
                        node
                    )  # When adding a neighbour to the stack, mark the predecessor as the current node so that we have a route back to the origin once the goal is found
                    stack.append(neighbour)
    print('DFS: Path not found!')
    return False


def bfs(lattice: Lattice, origin: Node, goal: Node):
    queue = [origin]
    while queue:
        for _ in range(len(queue)):
            node = queue.pop(0)
            if node == goal:
                display_path_to_origin(node)
                print('BFS: Path found!')
                return True
            if node.get_state() not in [NodeState.WALL, NodeState.VISITED]:
                if node.get_state() not in [
                    NodeState.ORIGIN,
                    NodeState.GOAL,
                ]:  # Only set as visited if the node isn't origin/goal. This is because origin/goal nodes are never set to visited.
                    node.set_state(NodeState.VISITED)
                update_screen()
                for neighbour in lattice.get_neighbours(node):
                    if neighbour.get_state() not in [
                        NodeState.WALL,
                        NodeState.VISITED,
                        NodeState.ORIGIN,  # As far as I can tell, the last state (NodeState.ORIGIN) is only in this list for BFS because a predecessor was being set on the origin node, which isn't supposed to happen.
                    ]:
                        neighbour.set_predecessor(node)
                        queue.append(neighbour)
    print('BFS: Path not found!')
    return False


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                lattice.clear()
            elif event.key == pg.K_d and lattice.get_goal() and lattice.get_origin():
                dfs(lattice, lattice.get_origin(), lattice.get_goal())
            elif event.key == pg.K_b and lattice.get_goal() and lattice.get_origin():
                bfs(lattice, lattice.get_origin(), lattice.get_goal())
            else:
                lattice.set_draw_mode(
                    event_key_to_draw_mode_mapping.get(
                        event.key, DrawMode.SET_WALL
                    )  # If an invalid key is pressed, the draw mode will be set to DrawMode.SET_WALL
                )

        if event.type == pg.KEYUP:
            lattice.set_draw_mode(DrawMode.SET_WALL)

        if mouse_pressed:
            x, y = pg.mouse.get_pos()
            r = x // lattice_info.node_size
            c = y // lattice_info.node_size
            lattice.change_node_state(r, c)

    lattice.draw(screen)
    clock.tick(60)
    pg.display.flip()
