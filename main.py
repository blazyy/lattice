import sys
import pygame as pg

pg.init()

from typing import Dict
from enums import DrawMode, PathfindingOption
from Node import Pos
from Lattice import Lattice, LatticeInfo, ScreenDim


EventKeyToDrawModeMapping = Dict[int, DrawMode]
event_key_to_draw_mode_mapping = {
    pg.K_o: DrawMode.SET_ORIGIN,
    pg.K_e: DrawMode.SET_VACANT,
    pg.K_g: DrawMode.SET_GOAL,
}

NODE_SIZE = 15
SCREEN_SIDE_LEN = 1500

screen_dim = ScreenDim(SCREEN_SIDE_LEN, SCREEN_SIDE_LEN)
lattice_info = LatticeInfo(screen_dim, NODE_SIZE)

clock = pg.time.Clock()
mouse = pg.mouse.set_cursor(pg.cursors.tri_left)
screen = pg.display.set_mode(
    (lattice_info.screen_dim.w, lattice_info.screen_dim.h), pg.DOUBLEBUF
)

mouse_pressed = False

lattice = Lattice(screen, lattice_info)
lattice.draw()

'''
Event mapping:

C - Clear Lattice
M - Generate maze (using randomized DFS)
E - Erases wall nodes (Have to hold down key when clicking mouse)
O - Sets origin node (Have to hold down key when clicking mouse, can only set 1 origin)
G - Sets goal node (Have to hold down key when clicking mouse, can only set 1 goal)
R - Generate random walls
L - Begin Game of Life simulation
D - Begin DFS visualization (only starts if Origin and Goal are both set)
B - Begin BFS visualization (only starts if Origin and Goal are both set)
K - Begin Dijkstra's Pathfinding visualization
A - Begin A* Search Visualization
'''

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                lattice.clear()
            if event.key == pg.K_m:
                lattice.generate_maze()
            if event.key == pg.K_r:
                lattice.randomize(0.25)
            elif event.key == pg.K_d:
                lattice.visualize(PathfindingOption.DFS)
            elif event.key == pg.K_b:
                lattice.visualize(PathfindingOption.BFS)
            elif event.key == pg.K_k:
                lattice.visualize(PathfindingOption.DIJKSTRA)
            elif event.key == pg.K_a:
                lattice.visualize(PathfindingOption.A_STAR)
            elif event.key == pg.K_l:
                lattice.game_of_life()
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
            pos = Pos(r, c)
            lattice.change_node_state_on_user_input(pos)

    # clock.tick(60)
