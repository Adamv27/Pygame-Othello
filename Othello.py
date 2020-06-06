import sys
import draw
import random
import pygame

pygame.init()


class Game:
    def __init__(self, board):
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.board = board
        self.turn = 0
        self.player_one = Player('X')  # White
        self.player_two = Player('O')  # Black
        self.possible_moves = []
    def main_loop(self):
        self.set_up_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.turn % 2 == 0:
                current_player = 'X'
                self.possible_moves = self.board.get_possible_moves('X', self.screen)
                self.display_possible_moves()
                move = self.player_one.get_move(self.possible_moves)
            else:
                current_player = 'O'
                self.possible_moves = self.board.get_possible_moves('O', self.screen)
                self.display_possible_moves()
                move = self.player_two.get_move(self.possible_moves)

            self.board.grid[move[1]][move[0]] = current_player
            self.reset_possible_moves()
            draw.tile(self.screen, move, current_player)
            self.turn += 1

    def set_up_board(self):
        # Each player starts with two pieces in the middle
        self.board.grid[3][3] = self.board.grid[4][4] = self.player_one.symbol
        self.board.grid[3][4] = self.board.grid[4][3] = self.player_two.symbol
        draw.board(self.screen)
        draw.tiles(self.screen, self.board.grid)

    def display_possible_moves(self):
        # Draws the green circle at a possible move
        for possible_move in self.possible_moves:
            draw.possible_move(self.screen, possible_move[0], possible_move[1])

    def reset_possible_moves(self):
        # Removes the green circles after the turn is over
        for possible_move in self.possible_moves:
            draw.square(self.screen, possible_move[0], possible_move[1])
        self.possible_moves = []


class Player:
    def __init__(self, symbol):
        self.tile_count = 2
        self.symbol = symbol

    def get_move(self, possible_moves):
        print(possible_moves)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Check for left click to select a move
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    board_row = y // 75
                    board_column = x // 75
                    print(board_row, board_column)
                    if (board_row, board_column) in possible_moves:
                        return board_row, board_column

    def update_tile_count(self):
        pass


class Board:
    def __init__(self):
        # 8x8 Grid
        self.grid = [[''] * 8 for row in range(8)]

    def get_possible_moves(self, player: str, screen) -> list:
        possible_moves = []
        # Loop through all spots on the board and check if each one is possible to play
        # for a given player
        for row_index, row in enumerate(self.grid):
            for column_index, column in enumerate(row):
                if self.possible_move((row_index, column_index), player):
                    possible_moves.append((row_index, column_index))
        return possible_moves

    def possible_move(self, move: tuple, player: str) -> bool:
        opposite_player = 'X' if player == 'O' else 'O'
        row, column = move
        # Can't play a move on a taken space
        if self.grid[row][column] != '':
            return False

        #  Check up down left right and all diagonals
        directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
        for direction in directions:
            current_row = row
            current_column = column
            # Number of opponent tiles in between your move and one of your own pieces
            opponent_tiles = 0
            while True:
                # Move along board depending on current direction
                current_row += direction[1]
                current_column += direction[0]

                # Can not go farther than length of board
                if (current_row > 7 or current_row < 0) or (current_column > 7 or current_column < 0):
                    break
                # There can not be a space in the middle of a move
                elif self.grid[current_row][current_column] == '':
                    break
                # Opponents tiles must be in between your two pieces
                elif self.grid[current_row][current_column] == opposite_player:
                    opponent_tiles += 1
                # There must be one of your own tiles across from your move
                elif self.grid[current_row][current_column] == player:
                    # There must be at least one opponent tiles in between your own pieces
                    if opponent_tiles > 0:
                        return True
                    else:
                        break
        return False

    def flip_tiles(self, move):
        pass


game_board = Board()
game = Game(game_board)
game.main_loop()
