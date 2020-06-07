import sys
import draw
import time
import random
import pygame
import minimax
pygame.init()


class Game:
    def __init__(self, board):
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.board = board
        self.turn = 0
        self.player_one = Player('O')  # White
        self.player_two = Player('X')  # Black
        self.possible_moves = []

    def main_loop(self):
        self.set_up_board()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.turn % 2 == 0:
                current_player = 'O'
                self.possible_moves = self.board.get_possible_moves('O', self.screen)
                self.display_possible_moves()
                move = self.player_one.get_move(self.possible_moves)
            else:
                current_player = 'X'
                computer = minimax.Computer(self.board.grid)
                move = computer.get_best_move()
                print(move)
            # Play the current move
            self.board.grid[move[0]][move[1]] = current_player
            # Flip tiles after move has been played
            self.board.flip_tiles(self.screen, move, current_player)

            # Update the tile counts to check for a win
            self.player_one.update_tile_count('X', self.board.grid)
            self.player_two.update_tile_count('O', self.board.grid)

            if self.player_one.tile_count <= 0 or self.player_two.tile_count <= 0:
                self.display_winner()
                time.sleep(2)
                break
            # Redraw board to get rid of possible moves
            self.update_board()
            # Reset possible moves for next turn
            self.possible_moves = []
            self.turn += 1

    def set_up_board(self):
        # Each player starts with two pieces in the middle
        self.board.grid[3][3] = self.board.grid[4][4] = self.player_one.symbol
        self.board.grid[3][4] = self.board.grid[4][3] = self.player_two.symbol
        self.update_board()

    def display_possible_moves(self):
        # Draws the green circle at a possible move
        for possible_move in self.possible_moves:
            draw.possible_move(self.screen, possible_move[1], possible_move[0])

    def update_board(self):
        draw.board(self.screen)
        draw.tiles(self.screen, self.board.grid)

    def display_winner(self):
        winner = 'White' if self.player_one.tile_count > self.player_two.tile_count else 'Black'
        text = f'Game over! {winner} is the winner!'
        font = pygame.font.SysFont(None, 50)
        display_text = font.render(text, True, (255, 0, 0))
        self.screen.blit(display_text, (25, 250))
        pygame.display.update()


class Player:
    def __init__(self, symbol):
        self.tile_count = 2
        self.symbol = symbol

    def get_move(self, possible_moves: list) -> tuple:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Check for left click to select a move
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    board_row = y // 75
                    board_column = x // 75
                    if (board_row, board_column) in possible_moves:
                        return board_row, board_column

    def update_tile_count(self, player, board):
        self.tile_count = 0
        for row in board:
            self.tile_count += row.count(player)


class Board:
    def __init__(self):
        # 8x8 Grid
        self.grid = [[''] * 8 for row in range(8)]
        self.directions_to_flip = []

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
        row, column = move
        # Can't play a move on a taken space
        if self.grid[row][column] in ['X', 'O']:
            return False

        #  Check up down left right and all diagonals
        directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
        for direction in directions:
            # If any direction is possible then the move is playable
            if self.check_direction(move, direction, player):
                return True
        return False

    def check_direction(self, move: tuple, direction: list, player: str) -> bool:
        opposite_player = 'X' if player == 'O' else 'O'
        row, column = move
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

    def flip_tiles(self, screen, move: tuple, player:str):
        opposite_player = 'X' if player == 'O' else 'O'
        row, column = move

        directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
        for direction in directions:
            if self.check_direction(move, direction, player):
                current_row = row
                current_column = column
                while True:
                    current_row += direction[1]
                    current_column += direction[0]

                    if (current_row > 7 or current_row < 0) or (current_column > 7 or current_column < 0):
                        break

                    elif self.grid[current_row][current_column] == player:
                        break
                    elif self.grid[current_row][current_column] == opposite_player:
                        self.grid[current_row][current_column] = player
                        draw.tile(screen, (current_row, current_column), player)


game_board = Board()
game = Game(game_board)
game.main_loop()
