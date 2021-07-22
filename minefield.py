import random
from pygame import mixer
from tile import *


class Minefield:

    WINDOW_DIM = 800
    N = 16
    MINES = 40
    R = WINDOW_DIM // N

    def __init__(self, s):
        self.s = s
        self.tiles = []
        self.coords = []
        self.remaining_flags = Minefield.MINES
        self.first_left_click = True
        self.game_end = False

    def compute_valid_neighbors(self, t):
        if(t.r-1 >= 0):
            t.valid_neighbors.append(self.tiles[t.r-1][t.c])
            if(t.c-1 >= 0):
                t.valid_neighbors.append(self.tiles[t.r-1][t.c-1])
            if(t.c+1 < Minefield.N):
                t.valid_neighbors.append(self.tiles[t.r-1][t.c+1])

        if(t.r+1 < Minefield.N):
            t.valid_neighbors.append(self.tiles[t.r+1][t.c])
            if(t.c-1 >= 0):
                t.valid_neighbors.append(self.tiles[t.r+1][t.c-1])
            if(t.c+1 < Minefield.N):
                t.valid_neighbors.append(self.tiles[t.r+1][t.c+1])

        if(t.c-1 >= 0):
            t.valid_neighbors.append(self.tiles[t.r][t.c-1])
        if(t.c+1 < Minefield.N):
            t.valid_neighbors.append(self.tiles[t.r][t.c+1])

    def init_field(self):

        # Preparing empty tile field and empty coords list
        for i in range(Minefield.N):
            row = []
            for j in range(Minefield.N):
                self.coords.append((i, j))
                row.append(Tile(0, i, j, self, self.s))
            self.tiles.append(row)

        # Generating a valid neighbor list for each tile
        for i in range(Minefield.N):
            for j in range(Minefield.N):
                self.compute_valid_neighbors(self.tiles[i][j])

    def prep_field(self, clicked_tile):

        # Remove clicked tile and all adjacent tiles are mine eligable
        self.coords.remove((clicked_tile.r, clicked_tile.c))

        for t in clicked_tile.valid_neighbors:
            self.coords.remove((t.r, t.c))

        # Placing mines randomly
        for i in range(Minefield.MINES):
            k = random.randint(0, len(self.coords)-1)
            r, c = self.coords.pop(k)
            self.tiles[r][c].danger = 9

        # Assigning danger levels
        for i in range(0, Minefield.N):
            for j in range(0, Minefield.N):
                currentTile = self.tiles[i][j]
                if(currentTile.danger != 9):
                    for t in currentTile.valid_neighbors:
                        if(t.danger == 9):
                            currentTile.danger += 1
        clicked_tile.danger = 0

    # Called whenever we're out of flags to save computing power
    def check_win(self):
        for i in range(Minefield.N):
            for j in range(Minefield.N):
                t = self.tiles[i][j]
                if(t.danger == 9 and not t.flagged):
                    return False
        return True

    def reveal_all_mines(self):
        for i in range(0, Minefield.N):
            for j in range(0, Minefield.N):
                t = self.tiles[i][j]
                if(t.danger == 9):
                    t.revealed = True

    def reveal_cascade(self, centralTile):

        # Return if current tile is a revealed tile, mine tile, or a flagged tile
        if(centralTile.revealed or centralTile.flagged or centralTile.danger == 9):
            return

        # If current tile is an unrevealed non lethal tile, reveal it
        if(centralTile.danger > 0 and centralTile.danger <= 8):
            centralTile.revealed = True
            return

        # If current tile is an unrevealed empty tile, reveal it and check other neighbors
        if(centralTile.danger == 0):
            centralTile.revealed = True

            for t in centralTile.valid_neighbors:
                self.reveal_cascade(t)

    def left_clicked(self, clicked_tile):

        # Ensuring clicked_tile is unrevealed and unflagged
        if(clicked_tile.revealed or clicked_tile.flagged):
            return

        # Making sure first click is on an empty tile
        if (self.first_left_click):
            self.prep_field(clicked_tile)
            self.first_left_click = False
            self.reveal_cascade(clicked_tile)
            return

        # If player clicked on an unrevealed mine
        if(clicked_tile.danger == 9):
            mixer.music.load('sfx/lose.wav')
            mixer.music.play()
            self.reveal_all_mines()
            self.game_end = True

        # If player clicked on an unrevealed dangerous tile
        elif(clicked_tile.danger > 0 and clicked_tile.danger <= 8):
            clicked_tile.revealed = True

        # If player clicked on an unrevealed empty tile
        elif(clicked_tile.danger == 0):
            self.reveal_cascade(clicked_tile)

    def right_clicked(self, clicked_tile):

        if(clicked_tile.revealed):
            return

        mixer.music.load('sfx/flag.wav')
        mixer.music.play()

        if(clicked_tile.flagged):
            self.remaining_flags += 1
            clicked_tile.flagged = not clicked_tile.flagged

        elif(self.remaining_flags > 0):
            self.remaining_flags -= 1
            clicked_tile.flagged = not clicked_tile.flagged

            if (self.remaining_flags == 0):
                if (self.check_win()):
                    mixer.music.load('sfx/win.wav')
                    mixer.music.play()
                    self.game_end = True

    def draw(self):
        for i in range(0, Minefield.N):
            yline = self.tiles[0][0].w * i
            for j in range(0, Minefield.N):
                self.tiles[i][j].draw()
                xline = self.tiles[0][0].w * j
                pygame.draw.line(self.s, (0, 0, 0), (xline, 0),
                                 (xline, Minefield.WINDOW_DIM))

            pygame.draw.line(self.s, (0, 0, 0), (0, yline),
                             (Minefield.WINDOW_DIM, yline))
