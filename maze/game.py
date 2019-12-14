# game.py
import pygame
from pygame.locals import *
from cell import Cell

class board:

    maze_file = 'mazeFile.txt'
    cell_size = 32
    NOTHING = (255, 255, 255)
    WALL = (0, 0, 0)
    PATH = (0, 0, 155)
    TRIED = (155, 0, 0)
    START = (0, 155, 0)
    END = (255, 0, 255)

    def __init__(self):
        self.mazeCells = self.buildMaze(self.maze_file)
        self.initMaze()
        pygame.init()
        self.window_surface = pygame.display.set_mode((self.numCols * self.cell_size, self.numRows * self.cell_size))

    def buildMaze(self, file_name):
        with open(file_name) as maze_file:
            self.numRows, self.numCols = self.read_value_pair(maze_file)
            maze = [[Cell(row * self.cell_size, col * self.cell_size, '.') for col in range(self.numCols)] for row in range(self.numRows)]

            start_row, start_col = self.read_value_pair(maze_file)
            maze[start_row][start_col].setValue('s')
            self.startCell = Cell(start_row, start_col)

            end_row, end_col = self.read_value_pair(maze_file)
            maze[end_row][end_col].setValue('e')
            self.endCell = Cell(end_row, end_col)

            for row_index, row in enumerate(maze):
                line = maze_file.readline()
                for col_index, char in enumerate(line):
                    if char == '#':
                        maze[row_index][col_index].setValue('#')
            return maze

    def read_value_pair(self, input_file):
        value1, value2 = input_file.readline().split()
        return int(value1), int(value2)
    
    def initMaze(self):
        self.row_pos = self.startCell.row
        self.col_pos = self.startCell.col
        self.stack = []
        self.stop_searching = True

    def draw(self):
        for row in self.mazeCells:
            for cell in row:
                cell_rect = pygame.Rect(cell.col, cell.row, self.cell_size, self.cell_size)
                pygame.draw.rect(self.window_surface, self.cell_type(cell), cell_rect)
        
        pygame.display.update()
    
    def cell_type(self, cell):
        if cell.value == '.':
            return self.NOTHING
        elif cell.value == '#':
            return self.WALL
        elif cell.value == 'x':
            return self.PATH
        elif cell.value == 'o':
            return self.TRIED
        elif cell.value == 's':
            return self.START
        elif cell.value == 'e':
            return self.END
        else:
            return (255, 255, 0)

    def __repr__(self):
        return '\n'.join([' '.join(str(cell) for cell in self.mazeCells[row]) for row in range(self.numRows)])

    def surrounding_pos(self, row, col):
        return [(row-1, col), (row+1, col), (row, col+1), (row, col-1)]

    def vaildMove(self, row, col):
        return row >= 0 and row < self.numRows and col >= 0 and col < self.numCols and (self.mazeCells[row][col].value == '.' \
                                                                                   or   self.mazeCells[row][col].value == 'e' )

    def exitFound(self, row, col):
        return row == self.endCell.row and col == self.endCell.col

    def reset(self):
        self.mazeCells = self.buildMaze(self.maze_file)
        self.initMaze()

    def findPath(self):
        
        
        found_a_way = False
        for row, col in self.surrounding_pos(self.row_pos, self.col_pos):
            if self.vaildMove(row, col):
                self.stack.append((self.row_pos, self.col_pos))
                self.mazeCells[row][col].setValue('x')
                self.row_pos = row
                self.col_pos = col
                found_a_way = True
                break

        if not found_a_way:
            self.mazeCells[self.row_pos][self.col_pos].setValue('o')
            self.row_pos, self.col_pos = self.stack.pop()

        if (self.row_pos == self.startCell.row and self.col_pos == self.startCell.col) or self.exitFound(self.row_pos, self.col_pos):
            self.stop_searching = True
LEFT_BUTTON = 1
RIGHT_BUTTON = 3

fps = pygame.time.Clock()
maze = board()
running = True

while running:
    maze.draw()
    if not maze.stop_searching:
        maze.findPath()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            running = False
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            x = x // maze.cell_size
            y = y // maze.cell_size
            if event.button == LEFT_BUTTON:
                maze.mazeCells[y][x].setValue('.')
            elif event.button == RIGHT_BUTTON:
                maze.mazeCells[y][x].setValue('#')
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        maze.reset()
    if keys[pygame.K_s]:
        maze.stop_searching = False

    fps.tick(20)


