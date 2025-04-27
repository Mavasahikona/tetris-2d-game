import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

SHAPE_COLORS = [CYAN, YELLOW, GREEN, RED, BLUE, ORANGE, MAGENTA]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(SHAPE_COLORS)
        return {'shape': shape, 'color': color, 'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 'y': 0}

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, piece):
        for y in range(len(piece['shape'])):
            for x in range(len(piece['shape'][y])):
                if piece['shape'][y][x]:
                    pygame.draw.rect(self.screen, piece['color'], ((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, WHITE, ((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def valid_move(self, piece, x_offset=0, y_offset=0):
        for y in range(len(piece['shape'])):
            for x in range(len(piece['shape'][y])):
                if piece['shape'][y][x]:
                    new_x = piece['x'] + x + x_offset
                    new_y = piece['y'] + y + y_offset
                    if new_x < 0 or new_x >= len(self.grid[0]) or new_y >= len(self.grid) or (new_y >= 0 and self.grid[new_y][new_x]):
                        return False
        return True

    def lock_piece(self, piece):
        for y in range(len(piece['shape'])):
            for x in range(len(piece['shape'][y])):
                if piece['shape'][y][x]:
                    self.grid[piece['y'] + y][piece['x'] + x] = piece['color']

    def clear_lines(self):
        lines_cleared = 0
        for y in range(len(self.grid)):
            if all(self.grid[y]):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1][:]
                self.grid[0] = [0 for _ in range(len(self.grid[0]))]
        self.score += lines_cleared * 100

    def rotate_piece(self, piece):
        rotated = [[piece['shape'][y][x] for y in range(len(piece['shape']))] for x in range(len(piece['shape'][0]) - 1, -1, -1)]
        if self.valid_move({'shape': rotated, 'x': piece['x'], 'y': piece['y'], 'color': piece['color']}}):
            piece['shape'] = rotated

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.valid_move(self.current_piece, x_offset=-1):
                        self.current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT and self.valid_move(self.current_piece, x_offset=1):
                        self.current_piece['x'] += 1
                    if event.key == pygame.K_DOWN and self.valid_move(self.current_piece, y_offset=1):
                        self.current_piece['y'] += 1
                    if event.key == pygame.K_UP:
                        self.rotate_piece(self.current_piece)
                    if event.key == pygame.K_SPACE:
                        while self.valid_move(self.current_piece, y_offset=1):
                            self.current_piece['y'] += 1

            if self.valid_move(self.current_piece, y_offset=1):
                self.current_piece['y'] += 1
            else:
                self.lock_piece(self.current_piece)
                self.clear_lines()
                self.current_piece = self.new_piece()
                if not self.valid_move(self.current_piece):
                    self.game_over = True

            self.draw_grid()
            self.draw_piece(self.current_piece)
            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()