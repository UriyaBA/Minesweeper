import random
from drawable import Drawable
from pygame import mixer
from tile import *


class Minefield(Drawable):

    WINDOW_SIZE = 800
    FIELD_LENGTH = 16
    TOTAL_MINES = 40
    TILE_SIZE = WINDOW_SIZE // FIELD_LENGTH

    def __init__(self, screen):
        self.screen = screen
        self.tiles = []
        self.coords = []
        self.remaining_flags = Minefield.TOTAL_MINES
        self.first_left_click = True
        self.game_end = False

    def compute_valid_neighbors(self, t):
        if(t.row-1 >= 0):
            t.valid_neighbors.append(self.tiles[t.row-1][t.col])
            if(t.col-1 >= 0):
                t.valid_neighbors.append(self.tiles[t.row-1][t.col-1])
            if(t.col+1 < Minefield.FIELD_LENGTH):
                t.valid_neighbors.append(self.tiles[t.row-1][t.col+1])

        if(t.row+1 < Minefield.FIELD_LENGTH):
            t.valid_neighbors.append(self.tiles[t.row+1][t.col])
            if(t.col-1 >= 0):
                t.valid_neighbors.append(self.tiles[t.row+1][t.col-1])
            if(t.col+1 < Minefield.FIELD_LENGTH):
                t.valid_neighbors.append(self.tiles[t.row+1][t.col+1])

        if(t.col-1 >= 0):
            t.valid_neighbors.append(self.tiles[t.row][t.col-1])
        if(t.col+1 < Minefield.FIELD_LENGTH):
            t.valid_neighbors.append(self.tiles[t.row][t.col+1])

    def init_field(self):

        # Preparing empty tile field and empty coords list
        for i in range(Minefield.FIELD_LENGTH):
            row = []
            for j in range(Minefield.FIELD_LENGTH):
                self.coords.append((i, j))
                row.append(Tile(0, i, j, self, self.screen))
            self.tiles.append(row)

        # Generating a valid neighbor list for each tile
        for i in range(Minefield.FIELD_LENGTH):
            for j in range(Minefield.FIELD_LENGTH):
                self.compute_valid_neighbors(self.tiles[i][j])

    def prep_field(self, clicked_tile):

        # Remove clicked tile and all adjacent tiles are mine eligable
        self.coords.remove((clicked_tile.row, clicked_tile.col))

        for t in clicked_tile.valid_neighbors:
            self.coords.remove((t.row, t.col))

        # Placing mines randomly
        for i in range(Minefield.TOTAL_MINES):
            k = random.randint(0, len(self.coords)-1)
            row, col = self.coords.pop(k)
            self.tiles[row][col].surrounding_mines_num = Tile.MINE_DANGER

        # Assigning 'surrounding_mines_num' levels
        for i in range(0, Minefield.FIELD_LENGTH):
            for j in range(0, Minefield.FIELD_LENGTH):
                currentTile = self.tiles[i][j]
                if(currentTile.surrounding_mines_num != Tile.MINE_DANGER):
                    for t in currentTile.valid_neighbors:
                        if(t.surrounding_mines_num == Tile.MINE_DANGER):
                            currentTile.surrounding_mines_num += 1
        clicked_tile.surrounding_mines_num = 0

    # Called whenever we're out of flags to save computing power
    def check_win(self):
        for i in range(Minefield.FIELD_LENGTH):
            for j in range(Minefield.FIELD_LENGTH):
                t = self.tiles[i][j]
                if(t.surrounding_mines_num == Tile.MINE_DANGER and not t.flagged):
                    return False
        return True

    def reveal_all_mines(self):
        for i in range(0, Minefield.FIELD_LENGTH):
            for j in range(0, Minefield.FIELD_LENGTH):
                t = self.tiles[i][j]
                if(t.surrounding_mines_num == Tile.MINE_DANGER):
                    t.revealed = True

    def reveal_cascade(self, centralTile):

        # Return if current tile is a revealed tile, mine tile, or a flagged tile
        if(centralTile.revealed or centralTile.flagged or centralTile.surrounding_mines_num == Tile.MINE_DANGER):
            return

        # If current tile is an unrevealed non lethal tile, reveal it
        if(centralTile.surrounding_mines_num > 0 and centralTile.surrounding_mines_num <= 8):
            centralTile.revealed = True
            return

        # If current tile is an unrevealed empty tile, reveal it and check other neighbors
        if(centralTile.surrounding_mines_num == 0):
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
        if(clicked_tile.surrounding_mines_num == Tile.MINE_DANGER):
            mixer.music.load('sfx/lose.wav')
            mixer.music.play()
            self.reveal_all_mines()
            self.game_end = True

        # If player clicked on an unrevealed dangerous tile
        elif(clicked_tile.surrounding_mines_num > 0 and clicked_tile.surrounding_mines_num <= 8):
            clicked_tile.revealed = True

        # If player clicked on an unrevealed empty tile
        elif(clicked_tile.surrounding_mines_num == 0):
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
        for i in range(0, Minefield.FIELD_LENGTH):
            yline = self.tiles[0][0].w * i
            for j in range(0, Minefield.FIELD_LENGTH):
                self.tiles[i][j].draw()
                xline = self.tiles[0][0].w * j
                pygame.draw.line(self.screen, (0, 0, 0), (xline, 0),
                                 (xline, Minefield.WINDOW_SIZE))

            pygame.draw.line(self.screen, (0, 0, 0), (0, yline),
                             (Minefield.WINDOW_SIZE, yline))
