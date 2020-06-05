import pygame

black = (0, 0, 0)
white = (255, 255, 255)
center = 37
radius = 30

def board(screen):
    light_brown = (214, 177, 139)
    brown = (165, 122, 96)

    square_size = 75
    # 8x8 game board
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                color = light_brown
            else:
                color = brown
            pygame.draw.rect(screen, color, (row * square_size, column * square_size, square_size, square_size))
    pygame.display.update()


def tiles(screen, board):
    for row in range(8):
        for column in range(8):
            if board[row][column] == '':
                continue
            elif board[row][column] == 'X':
                color = white
            elif board[row][column] == 'O':
                color = black

            pygame.draw.circle(screen, color, (row * 75 + center, column * 75 + center), radius)
    pygame.display.update()


def tile(screen, move, symbol):
    row = move[1]
    column = move[0]
    color = white if symbol == 'X' else black
    pygame.draw.circle(screen, color, (row * 75 + center, column * 75 + center), radius)
    pygame.display.update()
