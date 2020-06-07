from sys import maxsize

HUMAN = -1  # O
COMP = 1  # X

class Computer:
    def __init__(self, board):
        self.board = self.get_board_copy(board)

    def get_board_copy(self, board):
        new_board = [[''] * 8 for row in range(8)]
        for i in range(8):
            for j in range(8):
                new_board[i][j] = board[i][j]
        return new_board

    def get_best_move(self):
        best_move = None
        best_score = -maxsize
        for move in get_possible_moves('X', self.board):
            row, column = move
            temp_board = self.get_board_copy(self.board)
            self.board[row][column] = 'X'
            self.board = flip_tiles(move, 'X', self.board)
            score = self.minimax(self.board, 5, True, 1)
            self.board = temp_board
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, depth, maximizing_player, player):
        if depth == 0 or (0 in game_over(board)):
            if player == COMP:
                return get_score(board)[1]
            else:
                return get_score(board)[0]

        if maximizing_player:
            max_eval = -maxsize
            for move in get_possible_moves('X', board):
                row, column = move
                temp_board = self.get_board_copy(board)
                board[row][column] = 'X'
                board = flip_tiles(move, 'X', board)
                eval_state = self.minimax(board, depth - 1, False, -player)
                max_eval = max(max_eval, eval_state)
                board = temp_board
            return max_eval
        else:
            min_eval = maxsize
            for move in get_possible_moves('O', board):
                row, column = move
                temp_board = self.get_board_copy(board)
                board[row][column] = 'O'
                board = flip_tiles(move, 'O', board)
                eval_state = self.minimax(board, depth - 1, True, -player)
                min_eval = min(min_eval, eval_state)
                board = temp_board
            return min_eval


def get_possible_moves(player: str, board) -> list:
    possible_moves = []
    # Loop through all spots on the board and check if each one is possible to play
    # for a given player
    for row_index, row in enumerate(board):
        for column_index, column in enumerate(row):
            if possible_move((row_index, column_index), player, board):
                possible_moves.append((row_index, column_index))
    return possible_moves


def possible_move(move: tuple, player: str, board) -> bool:
    row, column = move
    # Can't play a move on a taken space
    if board[row][column] in ['X', 'O']:
        return False

    #  Check up down left right and all diagonals
    directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
    for direction in directions:
        # If any direction is possible then the move is playable
        if check_direction(move, direction, player, board):
            return True
    return False


def check_direction(move: tuple, direction: list, player: str, board) -> bool:
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
        elif board[current_row][current_column] == '':
            break
        # Opponents tiles must be in between your two pieces
        elif board[current_row][current_column] == opposite_player:
            opponent_tiles += 1
        # There must be one of your own tiles across from your move
        elif board[current_row][current_column] == player:
            # There must be at least one opponent tiles in between your own pieces
            if opponent_tiles > 0:
                return True
            else:
                break
    return False


def flip_tiles(move: tuple, player:str, board):
    updated_board = board
    opposite_player = 'X' if player == 'O' else 'O'
    row, column = move

    directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
    for direction in directions:
        if check_direction(move, direction, player, board):
            current_row = row
            current_column = column
            while True:
                current_row += direction[1]
                current_column += direction[0]

                if (current_row > 7 or current_row < 0) or (current_column > 7 or current_column < 0):
                    break

                elif board[current_row][current_column] == player:
                    break
                elif board[current_row][current_column] == opposite_player:
                    updated_board[current_row][current_column] = player

    return updated_board


def game_over(board):
    return len(get_possible_moves('X', board)),  len(get_possible_moves('O', board))


def get_score(board):
    p1_score = 0
    p2_score = 0
    for row in board:
        for tile in row:
            if tile == 'O':
                p1_score += 1
            elif tile == 'X':
                p2_score += 1
    return p1_score, p2_score


def win(board):
    p1, p2 = get_score(board)
    print(p1, p2)
    if p2 > p1:
        return True
    else:
        return False


def loss(board):
    p1, p2 = get_score(board)
    if p2 < p1:
        return True
    else:
        return False
