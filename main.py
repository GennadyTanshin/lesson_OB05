import pygame
import random

pygame.init()

# Установка параметров окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Инициализация окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Функции для отрисовки блоков и сетки
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_grid():
    for x in range(GRID_WIDTH):
        pygame.draw.line(screen, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(screen, WHITE, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))

# Инициализация игрового поля
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Функция для создания нового блока
def new_block():
    tetrominos = [
        [[1, 1, 1, 1]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [1, 1]],
        [[1, 1, 0], [0, 1, 1]]
    ]
    block = random.choice(tetrominos)
    return block, 0, GRID_WIDTH // 2 - len(block[0]) // 2

block, block_rotation, block_x = new_block()
game_over = False

clock = pygame.time.Clock()

while not game_over:
    screen.fill(BLACK)
    draw_grid()

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x, y, cell)

    # Падение блока
    if not any(cell for row in grid for cell in row):
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    else:
        for y, row in list(enumerate(grid))[::-1]:
            if not any(row):
                break
            if 0 in row:
                continue
            grid.pop(y)
            grid.append([0 for _ in range(GRID_WIDTH)])

    # Движение блока вниз
    new_block_y = len(grid) - len(block) - 1
    if new_block_y <= block_x:
        game_over = True
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                draw_block(block_x + x, block_rotation + y, BLUE)

    block_y = new_block_y
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                draw_block(block_x + x, block_y + y, BLUE)

    # Ввод с клавиатуры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        block_x -= 1
    if keys[pygame.K_RIGHT]:
        block_x += 1
    if keys[pygame.K_DOWN]:
        block_y += 1
    if keys[pygame.K_UP]:
        block_rotation = (block_rotation + 1) % 4

    pygame.display.update()
    clock.tick(5)

pygame.quit()