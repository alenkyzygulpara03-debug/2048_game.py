
import pygame
import random
import sys

pygame.init()

# Терезе баптаулары
WIDTH = 420
HEIGHT = 500
CELL = 100
GAP = 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

font = pygame.font.SysFont("Arial", 32, bold=True)
small_font = pygame.font.SysFont("Arial", 24)

WHITE = (250, 248, 239)
BG = (187, 173, 160)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

board = [[0] * 4 for _ in range(4)]


def add_tile():
    empty = [
        (r, c)
        for r in range(4)
        for c in range(4)
        if board[r][c] == 0
    ]

    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2 if random.random() < 0.9 else 4


def draw():
    screen.fill(BG)

    title = font.render("2048", True, WHITE)
    screen.blit(title, (15, 10))

    help_text = small_font.render("Arrow keys to move", True, WHITE)
    screen.blit(help_text, (150, 20))

    for r in range(4):
        for c in range(4):
            value = board[r][c]
            x = GAP + c * (CELL + GAP)
            y = 70 + GAP + r * (CELL + GAP)

            color = COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(
                screen,
                color,
                (x, y, CELL, CELL),
                border_radius=6
            )

            if value:
                text_color = (60, 58, 50) if value <= 4 else WHITE
                text = font.render(str(value), True, text_color)
                rect = text.get_rect(center=(x + CELL // 2, y + CELL // 2))
                screen.blit(text, rect)

    pygame.display.flip()


def move_left(row):
    values = [v for v in row if v != 0]
    result = []
    i = 0

    while i < len(values):
        if i + 1 < len(values) and values[i] == values[i + 1]:
            result.append(values[i] * 2)
            i += 2
        else:
            result.append(values[i])
            i += 1

    return result + [0] * (4 - len(result))


def move(direction):
    global board
    old_board = [row[:] for row in board]

    if direction == "left":
        board = [move_left(row) for row in board]

    elif direction == "right":
        board = [move_left(row[::-1])[::-1] for row in board]

    elif direction == "up":
        board = [
            list(col)
            for col in zip(*board)
        ]
        board = [move_left(row) for row in board]
        board = [list(col) for col in zip(*board)]

    elif direction == "down":
        board = [list(col) for col in zip(*board)]
        board = [move_left(row[::-1])[::-1] for row in board]
        board = [list(col) for col in zip(*board)]

    if board != old_board:
        add_tile()


add_tile()
add_tile()

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move("left")
            elif event.key == pygame.K_RIGHT:
                move("right")
            elif event.key == pygame.K_UP:
                move("up")
            elif event.key == pygame.K_DOWN:
                move("down")

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()
