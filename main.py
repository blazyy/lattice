import sys
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

path_found = False
def dfs(lattice: Lattice, origin: Node, goal: Node):
    visited = set()
    stack = [origin]
    while stack:
        pg.time.wait(1000)
        node = stack.pop()
        if node == goal:
            print('Path found!')
            return True
        if node not in visited and node.state != NodeState.WALL:
            visited.add(node)
            node.set_state(NodeState.VISITED)
            for neighbor in lattice.get_neighbours(node):
                stack.append(neighbor)
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
            lattice.set_draw_mode(
                event_key_to_draw_mode_mapping.get(event.key, DrawMode.SET_WALL) # If an invalid key is pressed, the draw mode will be set to DrawMode.SET_WALL
            )

        if lattice.get_goal() and lattice.get_origin() and not path_found:
            path_found = dfs(lattice, lattice.get_origin(), lattice.get_goal())

        if event.type == pg.KEYUP:
            lattice.set_draw_mode(DrawMode.SET_WALL)

        if mouse_pressed:
            x, y = pg.mouse.get_pos()
            r = x // lattice_info.node_size
            c = y // lattice_info.node_size
            lattice.change_node_state(r, c)

    lattice.draw(screen)
    pg.display.flip()
