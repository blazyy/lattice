from Lattice import Lattice, LatticeInfo
import sys
import pygame as pg
pg.init()


lattice_info = LatticeInfo(500, 500, 20)

screen = pg.display.set_mode(
    (lattice_info.screen_width, lattice_info.screen_height))

lattice = Lattice(lattice_info)
lattice.randomize()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            r, c = pg.mouse.get_pos()
            lattice.flip_node_state(
                r // lattice_info.node_size, c // lattice_info.node_size)
    screen.fill('black')
    lattice.draw(screen)
    # Makes sure everything that we've drawn on the screen becomes visible.
    pg.display.flip()
