import pygame
from pygame import mixer
from minefield import Minefield
from tile import Tile

pygame.init()
mixer.init()

screen = pygame.display.set_mode([Minefield.WINDOW_SIZE, Minefield.WINDOW_SIZE])
pygame.display.set_icon(Tile.SPRITE_MINE)

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
            norm_x, norm_y = y//Minefield.TILE_SIZE, x//Minefield.TILE_SIZE

            clicked_tile = m.tiles[norm_x][norm_y]

            if(event.button == 1):
                m.left_clicked(clicked_tile)
            elif(event.button == 3):
                m.right_clicked(clicked_tile)

    pygame.display.set_caption(
        f"Total mines: {str(m.TOTAL_MINES)} | Remaining flags: {str(m.remaining_flags)}")
    m.draw()
    pygame.display.flip()

pygame.quit()
