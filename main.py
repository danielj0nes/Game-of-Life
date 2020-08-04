"""Daniel Jones - Game of Life, Python 3.x implementation - RIP John Conway 11.04.2020"""
import pygame
import random

CELL_SIZE = 20
MARGIN_SIZE = 20
WINDOW_HEIGHT = 1000 + MARGIN_SIZE
WINDOW_WIDTH = 1000 + MARGIN_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), pygame.RESIZABLE)
pygame.display.set_caption("Game of Life")


class Grid:
    def __init__(self, surface):
        self.surface = surface
        self.columns = (WINDOW_HEIGHT // CELL_SIZE)
        self.rows = (WINDOW_WIDTH // CELL_SIZE)
        self.cell_size = CELL_SIZE
        self.current_grid = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.font = pygame.font.SysFont('times new roman', 12, False)
        self.generation = 0

    def draw_grid(self):
        """Create grid using lines and numbers for rows/columns"""
        for row in range(self.rows):
            if row < 10:
                indent = " "
            else:
                indent = ""
            text = self.font.render(indent + str(row), 1, (0, 0, 0))
            row_coord = MARGIN_SIZE + row * CELL_SIZE
            self.surface.blit(text, (0, row_coord))
            pygame.draw.line(self.surface, BLACK, (MARGIN_SIZE, row_coord), (self.surface.get_width(), row_coord))
        for co in range(self.columns):
            if co < 10:
                indent = "  "
            else:
                indent = " "
            text = self.font.render(indent + str(co), 1, (0, 0, 0))
            col_coord = MARGIN_SIZE + co * CELL_SIZE
            self.surface.blit(text, (col_coord, 1))
            pygame.draw.line(self.surface, BLACK, (col_coord, MARGIN_SIZE), (col_coord, self.surface.get_height()))

    def __draw_cell(self, x, y):
        pygame.draw.rect(self.surface, RED, pygame.Rect(y + MARGIN_SIZE, x + MARGIN_SIZE, CELL_SIZE + 1, CELL_SIZE + 1))
        pygame.draw.rect(self.surface, BLACK,
                         pygame.Rect(y + MARGIN_SIZE, x + MARGIN_SIZE, CELL_SIZE + 1, CELL_SIZE + 1), 1)

    def __delete_cell(self, x, y):
        pygame.draw.rect(self.surface, WHITE,
                         pygame.Rect(y + MARGIN_SIZE, x + MARGIN_SIZE, CELL_SIZE + 1, CELL_SIZE + 1))
        pygame.draw.rect(self.surface, BLACK,
                         pygame.Rect(y + MARGIN_SIZE, x + MARGIN_SIZE, CELL_SIZE + 1, CELL_SIZE + 1), 1)

    def random_seed(self):
        for x in range(self.rows):
            for y in range(self.columns):
                self.current_grid[x][y] = random.getrandbits(1)

    def get_active_neighbours(self, x, y):
        active_neighbours = 0
        for a in range(-1, 2):
            for b in range(-1, 2):
                x_edge = (x + a + self.rows) % self.rows
                y_edge = (y + b + self.columns) % self.columns
                active_neighbours += self.current_grid[x_edge][y_edge]
        active_neighbours -= self.current_grid[x][y]
        return active_neighbours

    def parse(self):
        next_gen = [[0 for i in range(self.columns)] for j in range(self.rows)]
        for x in range(self.columns):
            for y in range(self.rows):
                neighbours = self.get_active_neighbours(x, y)
                if self.current_grid[x][y]:
                    self.__draw_cell(x * CELL_SIZE, y * CELL_SIZE)
                    if neighbours < 2 or neighbours > 3:  # Rules 1 and 3, handling under/overpopulation
                        next_gen[x][y] = 0
                    else:
                        next_gen[x][y] = 1  # Rule 2, handling cells living on to the next generation
                else:
                    self.__delete_cell(x * CELL_SIZE, y * CELL_SIZE)
                    if neighbours == 3:
                        next_gen[x][y] = 1  # Rule 4, reproducing cells
        self.current_grid = next_gen
        pygame.display.update()


pygame.init()
grid = Grid(surface=SCREEN)
SCREEN.fill(WHITE)  # Background colour
grid.draw_grid()
grid.random_seed()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    grid.parse()
