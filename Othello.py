import sys
import draw
import random
import pygame

pygame.init()

width = 600
height = 600
screen = pygame.display.set_mode((width, height))


class Game:
    def __init__(self, board):
        self.board = board
        self.turn = 0
        self.player_one = Player('X')  # White
        self.player_two = Player('O')  # Black

    def main_loop(self, screen):
        self.set_up_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.turn % 2 == 0:
                current_player = 'X'
                move = self.player_one.get_move()
            else:
                current_player = 'O'
                move = self.player_two.get_move()

            if self.board.possible_move(move, current_player):
                draw.tile(screen, move, current_player)
                self.turn += 1
            else:
                continue

    def set_up_board(self):
        self.board.grid[3][3] = self.board.grid[4][4] = self.player_one.symbol
        self.board.grid[3][4] = self.board.grid[4][3] = self.player_two.symbol
        draw.board(screen)
        draw.tiles(screen, self.board.grid)


class Player:
    def __init__(self, symbol):
        self.tile_count = 2
        self.symbol = symbol

    def get_move(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Check for left click to select a move
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    board_row = y // 75
                    board_column = x // 75
                    return board_row, board_column

    def update_tile_count(self):
        pass


class Board:
    def __init__(self):
        # 8x8 Grid
        self.grid = [[''] * 8 for row in range(8)]

    def possible_move(self, move: tuple, player: str) -> bool:
        opposite_player = 'X' if player == 'O' else 'O'
        row, column = move
        print(f'{player} playing move {column, row} against {opposite_player}')
        # Can't play a move on a taken space
        if self.grid[row][column] != '':
            return False

        #  Check up down left right and all diagonals
        directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
        for direction in directions:
            print()
            print(direction)
            current_row = row
            current_column = column
            # Number of opponent tiles in between your move and one of your own pieces
            opponent_tiles = 0
            while True:
                # Move along board depending on current direction
                current_row += direction[1]
                current_column += direction[0]

                # Can not go farther than length of board
                if len(self.grid) < current_row < 0 or len(self.grid[0]) < current_column < 0:
                    print('too far')
                    break

                # There can not be a space in the middle of a move
                if self.grid[current_row][current_column] == '':
                    print('space')
                    break
                # Opponents tiles must be in between your two pieces
                elif self.grid[current_row][current_column] == opposite_player:
                    print('found opponent')
                    opponent_tiles += 1
                # There must be one of your own tiles across from your move
                elif self.grid[current_row][current_column] == player:
                    print('found self')
                    # There must be at least one opponent tiles in between your own pieces
                    if opponent_tiles > 0:
                        return True
                    else:
                        print('not enough opponent')
                        break
        return False


game_board = Board()
game = Game(game_board)
game.main_loop(screen)
