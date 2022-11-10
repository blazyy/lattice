import sys
import pygame as pg

pg.init()

from typing import Dict
from enums import DrawMode
from Node import Pos
from Lattice import Lattice, LatticeInfo, ScreenDim


EventKeyToDrawModeMapping = Dict[int, DrawMode]
event_key_to_draw_mode_mapping = {
    pg.K_o: DrawMode.SET_ORIGIN,
    pg.K_e: DrawMode.SET_VACANT,
    pg.K_g: DrawMode.SET_GOAL,
}

screen_dim = ScreenDim(500, 500)
lattice_info = LatticeInfo(screen_dim, 5)

clock = pg.time.Clock()
mouse = pg.mouse.set_cursor(pg.cursors.tri_left)
screen = pg.display.set_mode((lattice_info.screen_dim.w, lattice_info.screen_dim.h))

mouse_pressed = False

lattice = Lattice(screen, lattice_info)
lattice.init_screen()


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
                lattice.dfs()
            elif event.key == pg.K_b and lattice.get_goal() and lattice.get_origin():
                lattice.bfs()
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
