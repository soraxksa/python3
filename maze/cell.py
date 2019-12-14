# cell.py


class Cell:

    def __init__(self, row, col, value=' '):
        self.row = row
        self.col = col
        self.value = value

    def setValue(self, value):
        self.value = value
    
    def __repr__(self):
        return self.value

