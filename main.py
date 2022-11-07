import sys
import pygame as pg

from enums import DrawMode
from Lattice import Lattice, LatticeInfo, ScreenDim

pg.init()


screen_dim = ScreenDim(500, 500)
lattice_info = LatticeInfo(screen_dim, 20)

screen = pg.display.set_mode((lattice_info.screen_dim.w, lattice_info.screen_dim.h))

lattice = Lattice(lattice_info)
# lattice.randomize()

dragging = False

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True

        if event.type == pg.MOUSEBUTTONUP:
            dragging = False

        if dragging:
            r, c = pg.mouse.get_pos()
            lattice.flip_node_state(
                r // lattice_info.node_size,
                c // lattice_info.node_size,
                lattice.get_draw_mode(),
            )

    # screen.fill('white')
    lattice.draw(screen)
    # Makes sure everything that we've drawn on the screen becomes visible.
    pg.display.flip()
