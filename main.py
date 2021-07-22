import pygame
from minefield import *

pygame.init()
mixer.init()

screen = pygame.display.set_mode([Minefield.WINDOW_DIM, Minefield.WINDOW_DIM])
pygame.display.set_icon(Tile.SPR_MINE)

m = Minefield(screen)
m.init_field()

running = True

while running:

    ev = pygame.event.get()

    for event in ev:
        if(event.type == pygame.QUIT):
            running = False

        # Handling mouse presses
        if(event.type == pygame.MOUSEBUTTONUP and not m.game_end):

            x, y = pygame.mouse.get_pos()
            norm_x, norm_y = y//Minefield.R, x//Minefield.R

            clicked_tile = m.tiles[norm_x][norm_y]

            if(event.button == 1):
                m.left_clicked(clicked_tile)
            elif(event.button == 3):
                m.right_clicked(clicked_tile)

    pygame.display.set_caption(
        "Total mines: " + str(m.MINES) + " | Remaining flags: " + str(m.remaining_flags))
    m.draw()
    pygame.display.flip()

pygame.quit()
