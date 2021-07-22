from drawable import Drawable
import json
import pygame


class Tile(Drawable):

    COLOR_UNREVEALED = (193, 192, 193)
    COLOR_REVEALED = (193, 192, 193)
    COLOR_REVEALED_MINE = (255, 192, 193)

    MINE_DANGER = 9

    # Load indicative 'danger level' colors from external json file
    with open('json/colors_danger.json', 'r') as f:
        data = json.load(f)

    COLORS_DANGER = data['colors']
    SPRITE_FLAG = pygame.image.load("sprites/flag.png")
    SPRITE_MINE = pygame.image.load("sprites/mine.png")

    def __init__(self, surrounding_mines_num, row, col, minefield, screen):
        self.surrounding_mines_num = surrounding_mines_num
        self.row = row
        self.col = col
        self.minefield = minefield
        self.screen = screen
        self.valid_neighbors = []
        self.flagged = False
        self.revealed = False

        self.w = minefield.TILE_SIZE
        self.h = minefield.TILE_SIZE

        self.x = self.w * self.col
        self.y = self.h * self.row

    def draw_sprite(self, spr):
        self.screen.blit(spr, (self.x, self.y))

    def draw_danger(self):

        if(self.surrounding_mines_num == Tile.MINE_DANGER):
            return

        pygame.font.init()
        myfont = pygame.font.SysFont('Futura', 57)
        textsurface = myfont.render(
            str(self.surrounding_mines_num), False, Tile.COLORS_DANGER[self.surrounding_mines_num])
        self.screen.blit(textsurface, (self.x + 15, self.y + 7))

    def draw(self):

        # Assign background color
        if(not self.revealed):
            color = Tile.COLOR_UNREVEALED
        elif(self.surrounding_mines_num == 0):
            color = Tile.COLORS_DANGER[0]
        elif(self.surrounding_mines_num != Tile.MINE_DANGER):
            color = Tile.COLOR_REVEALED
        elif(self.flagged):
            color = Tile.COLOR_UNREVEALED
        else:
            color = Tile.COLOR_REVEALED_MINE

        pygame.draw.rect(self.screen, color, pygame.Rect(
            self.x, self.y, self.w, self.h))
        if(self.revealed and self.surrounding_mines_num != 0):
            self.draw_danger()

        if(self.flagged):
            self.draw_sprite(Tile.SPRITE_FLAG)
        elif(self.surrounding_mines_num == Tile.MINE_DANGER and self.revealed):
            self.draw_sprite(Tile.SPRITE_MINE)
