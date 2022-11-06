import sys
import random
import pygame as pg
pg.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_UNIT_SIZE = 20
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Creates a new Surface object that represents the actual displayed graphics. Any drawing you do to this Surface will become visible on the monitor
black = 0, 0, 0

def get_empty_grid():
    grid = []
    for _ in range(SCREEN_HEIGHT // GRID_UNIT_SIZE):
        grid.append([0] * (SCREEN_WIDTH // GRID_UNIT_SIZE))
    return grid

def draw_grid(pg, screen, grid):
    for r in range(0, SCREEN_WIDTH, GRID_UNIT_SIZE):
        for c in range(0, SCREEN_HEIGHT, GRID_UNIT_SIZE):
            pg.draw.rect(screen, 'white', pg.Rect(r, c, GRID_UNIT_SIZE, GRID_UNIT_SIZE), 1)


grid = get_empty_grid()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
    screen.fill(black)
    # pg.draw.rect(screen, 'white', pg.Rect(30, 30, 60, 60))
    draw_grid(pg, screen, grid)
    pg.display.flip() # Makes sure everything that we've drawn on the screen becomes visible.