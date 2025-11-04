from colours import Colours
import pygame
from position import Position

class Block:
    """
    Represents a single Piece wth a specific shape and rotation state.
    Handles movement, rotation, and drawing of the block on the grid.
    """
    def __init__(self, id):
        """
        Initialise a piece with a unique ID and its rotation states.
        
        Args:
            id (int): The piece's unique identifier, ie its shape and colour.
        """
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colours = Colours.get_cell_colours()

    def move(self, rows, columns):
        """
        Move the piece by a specified number of rows and columns.

        Args:
            rows(int): Number of rows to move vertically (positive moves down).
            columns (int): Number of columns to move horizontally (positives moves right).
        """
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_position(self):
        """
        Get the absolute grid positions of the piece's cells based on its rotation and offset.
        
        Returns:
            list[Position]: A list of Position objects representing the piece's occupied grid cells.
        """
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        """
        Rotate the piece to the next rotation state.
        Wraps around when the final rotation state is reached.
        """
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotate(self):
        """
        Revert the piece's rotation to its previous state.
        Used when a rotation would result in an invalid position.
        """
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1
    
    def draw(self, screen, offset_x, offset_y):
        """
        Draw the piece on the given Pygame surface at the specified screen offset.
        
        Args:
            screen (pygame.Surface): The Pygame surface to draw the piece on.
            offset_x (int): horizontal offset in pixels for drawing.
            offset_y (int): vertical offset in pixels for drawing.
        """
        tiles = self.get_cell_position()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x+ tile.column * self.cell_size, offset_y + tile.row * self.cell_size,
                                    self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colours[self.id], tile_rect)