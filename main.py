import sys
import pygame as pg

from typing import Dict
from enums import DrawMode
from Lattice import Lattice, LatticeInfo, ScreenDim

pg.init()


EventKeyToDrawModeMapping = Dict[int, DrawMode]
event_key_to_draw_mode_mapping = {
    pg.K_s: DrawMode.SET_ORIGIN,
    pg.K_e: DrawMode.SET_VACANT,
}


screen_dim = ScreenDim(500, 500)
lattice_info = LatticeInfo(screen_dim, 20)
screen = pg.display.set_mode((lattice_info.screen_dim.w, lattice_info.screen_dim.h))
mouse = pg.mouse.set_cursor(pg.cursors.tri_left)

lattice = Lattice(lattice_info)

mouse_pressed = False
current_draw_mode = DrawMode.SET_WALL

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pressed = False

        if event.type == pg.KEYDOWN:
            lattice.set_draw_mode(
                event_key_to_draw_mode_mapping.get(event.key, DrawMode.SET_WALL)
            )

        if mouse_pressed:
            x, y = pg.mouse.get_pos()
            r = x // lattice_info.node_size
            c = y // lattice_info.node_size
            lattice.change_node_state(r, c)

    lattice.draw(screen)
    pg.display.flip()
