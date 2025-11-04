import pygame
from colours import Colours

class Grid:
    """
    Represents the game board for Drop Block.
    Manages the grid state, cell values, collision detection, row clearing, and row rendering.
    """
    def __init__(self):
        """
        Initialise the grid with specified dimensions and empty cells.
        Sets up colour mapping for different block IDs.
        """
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colours = Colours.get_cell_colours()

    def print_grid(self):
        """
        Print the current grid state to the console for debugging
        """
        for row in range(self.num_rows):
            for column in range (self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):
        """
        Check if a given cell position is within grid boundaries.
        Args:
            row (int): The row index.
            column (int): The column index.
        
        Returns:
            bool: True if inside the grid, else False.
        """
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False
    
    def is_empty(self, row, column):
        """
        Check if a given cell is empty (is value 0)
        
        Args:
            row (int): The row index.
            column (int): The column index.
        
        Returns:
            bool: True if cell is empty, else False.
        """
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_full(self, row):
        """
        Check if specified row is completed(All non 0 values)
        
        Args:
            row (int): The row index to check.
        
        Returns:
            bool: True if the row is full, else False
        """
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    def clear_row(self, row):
        """
        Clear all cells in a specified row, setting them to 0
        
        Args:
            row (int): The row index to clear.
        """
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        """
        Move a given row down by a specified number of rows.
        Used when rows have been cleared and need to drop blocks in board.
        
        Args:
            row (int): The row index to move.
            num_rows (int): The amount of rows to move down.
        """
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        """
        Clear all fully filled rows in the grid.
        Move rows above downward to fill empty space.
        
        Returns:
            int: The number of rows cleared.
        """
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        """
        Reset the entire grid to 0s
        """
        for row in range(self.num_rows):
            for column in range (self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        """
        Draw the grid and all occupied cells on the screen.
        
        Args:
            screen (pygame.Surface): The surface on which to render the grid.
        """
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11,
                                        self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colours[cell_value], cell_rect)