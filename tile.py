import json
import pygame


class Tile:

    COLOR_UNREVEALED = (193, 192, 193)
    COLOR_REVEALED = (193, 192, 193)
    COLOR_REVEALED_MINE = (255, 192, 193)

    MINE_DANGER = 9

    # Load danger colors from external json file
    with open('json/colors_danger.json', 'r') as f:
        data = json.load(f)

    COLORS_DANGER = data['colors']
    SPR_FLAG = pygame.image.load("sprites/flag.png")
    SPR_MINE = pygame.image.load("sprites/mine.png")

    def __init__(self, danger, r, c, m, s):
        self.danger = danger
        self.r = r
        self.c = c
        self.m = m
        self.s = s
        self.valid_neighbors = []
        self.flagged = False
        self.revealed = False

        self.w = m.R
        self.h = m.R

        self.x = self.w * self.c
        self.y = self.h * self.r

    def draw_sprite(self, spr):
        self.s.blit(spr, (self.x, self.y))

    def draw_danger(self):

        if(self.danger == Tile.MINE_DANGER):
            return

        pygame.font.init()
        myfont = pygame.font.SysFont('Futura', 57)
        textsurface = myfont.render(
            str(self.danger), False, Tile.COLORS_DANGER[self.danger])
        self.s.blit(textsurface, (self.x + 15, self.y + 7))

    def draw(self):

        # Assign background color
        if(not self.revealed):
            color = Tile.COLOR_UNREVEALED
        elif(self.danger == 0):
            color = Tile.COLORS_DANGER[0]
        elif(self.danger != Tile.MINE_DANGER):
            color = Tile.COLOR_REVEALED
        elif(self.flagged):
            color = Tile.COLOR_UNREVEALED
        else:
            color = Tile.COLOR_REVEALED_MINE

        pygame.draw.rect(self.s, color, pygame.Rect(
            self.x, self.y, self.w, self.h))
        if(self.revealed and self.danger != 0):
            self.draw_danger()

        if(self.flagged):
            self.draw_sprite(Tile.SPR_FLAG)
        elif(self.danger == Tile.MINE_DANGER and self.revealed):
            self.draw_sprite(Tile.SPR_MINE)
