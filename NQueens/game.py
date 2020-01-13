# game.py
import pygame
from pygame.locals import *
import time
#Trying Out push
#Hello
class board:

    window_size = 720
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    

    def __init__(self, numRows, numCols):
        pygame.init()
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.cell_size = int(self.window_size / numRows) 
        self.rows = numRows
        self.cols = numCols
        self.board = [[False for _ in range(numCols)] for __ in range(numRows)]
        self.queens = []
        self.queen_image = pygame.transform.scale(pygame.image.load('queen.png').convert_alpha(), (self.cell_size, self.cell_size)).convert_alpha()

    def size(self):
        return self.rows

    def numQueens(self):
        return len(self.queens)

    def setQueen(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise NameError('Error:row or col')
        self.board[row][col] = True
        self.queens.append(row)

    def removeQueen(self, row, col):
        self.board[row][col] = False
        del self.queens[col]

    def is_unguard(self, row, col):
        positions = self.positions(row, col)
        for row, col in positions:
            if self.board[row][col] == True:
                return False
        return True

    def positions(self, pos_row, pos_col):
        left = []
        for i in range(pos_col-1, -1, -1):
            left.append((pos_row, i))

        top_left = []
        for row, col in zip(range(pos_row-1, -1, -1), range(pos_col-1, -1, -1)):
            top_left.append((row, col))
        down_left = []

        for row, col in zip(range(pos_row+1, self.rows), range(pos_col-1, -1, -1)):
            down_left.append((row, col))
        return left + top_left + down_left

    def draw(self):
        for row_index, row in enumerate(self.board):
            for col_index, item in enumerate(row):
                cell = pygame.Rect((col_index * self.cell_size), (row_index * self.cell_size), self.cell_size, self.cell_size)
                if item == True:
                    self.window.blit(self.queen_image, ((col_index * self.cell_size), (row_index * self.cell_size)))
                    #pygame.draw.rect(self.window, (255, 0, 0), cell)
                else:
                    pygame.draw.rect(self.window, self.getColor(row_index, col_index), cell)
        pygame.display.update()

    def getColor(self, row, col):
        if row % 2 == 0:
            if col % 2 == 0:
                return self.BLACK
            return self.WHITE
        else:
            if col % 2 == 0:
                return self.WHITE
            return self.BLACK

    def __repr__(self):
        board = []
        for row in self.board:
            new_row = []
            for item in row:
                if item == False:
                    new_row.append('#')
                else:
                    new_row.append('Q')
            board.append(new_row)
        return '\n'.join([''.join(item for item in board[row]) for row in range(len(board))])

        
def solveQueen(board, col):
    game.draw()
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            quit()

    if board.size() == board.numQueens():
        return True
    else:

        for row in range(board.rows):
            if board.is_unguard(row, col):
                board.setQueen(row, col)
                board.draw()
                time.sleep(0.1) 
                if solveQueen(board, col+1):
                    return True
                else:
                    board.removeQueen(row, col)
        return False

def solve_all_queen(board, col):

    if board.numQueens() == board.size():
        board.count += 1
        return True
    else:
        for row in range(board.rows):
            if board.is_unguard(row, col):
                board.setQueen(row, col)
                solveQueen2(board, col+1)
                board.removeQueen(row, col)

fps = pygame.time.Clock()
game = board(8, 8)
solving = True
running = True
game.draw()
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            print('end')
            pygame.quit()
            quit()
            running = False
    keys = pygame.key.get_pressed()
    solveQueen(game, 0)
    '''
    if keys[pygame.K_s] and solving:
        solving = False
        print('solveing')
        solveQueen(game, 0)
        game.draw()
    '''
    


