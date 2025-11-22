from grid import Grid
from blocks import *
import random
import pygame
from utils import resource_path

class Game:
    """"
    Main game controller for Drop Block.
    Manages the grid, falling blocks, scoring, levels, sounds, and game state.
    Handles block movement, rotation, collision detection, and rendering.
    """

    def __init__(self):
        """
        Initialise the game with a new grid, blocks, sounds, and state variables.
        Sets up the current and next blocks, score, level, and line tracking.
        """
        self.grid = Grid()
        self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), ZPiece(), TPiece()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.place_block_sound = pygame.mixer.Sound(resource_path("sounds/thump.mp3"))
        self.clear_line_sound = pygame.mixer.Sound(resource_path("sounds/clear.mp3"))
        self.level = 0
        self.total_lines_cleared = 0
        self.paused = False

    def update_score(self, lines_cleared):
        """
        Updates the player's score based on the number of rows cleared.
        
        Args:
            lines_cleared (int): Number of rows cleared in one move. (Max 4)
        """
        match lines_cleared:
            case 1:
                self.score += 40 * (self.level + 1)
            case 2:
                self.score += 100 * (self.level + 1)
            case 3:
                self.score += 300 * (self.level + 1)
            case 4:
                self.score += 1200 * (self.level + 1)

    def get_drop_speed(self):
        """
        Returns the drop interval (milliseconds) based on the current level.
        Higher levels = faster drops.
        """
        MAXIMUM_SPEED = 100
        BASE_SPEED = 350
        SPEED_INCREMENT = 25
        return max(MAXIMUM_SPEED, BASE_SPEED - (SPEED_INCREMENT * self.level))

    def increase_total_lines_cleared(self, lines_cleared):
        """
        Add the number of rows cleared to the total count.
        
        Args:
            lines_cleared (int): Number of rows cleared in the move. (Max 4)
        """
        self.total_lines_cleared += lines_cleared

    def increase_level(self):
        """
        Update the game level based on total rows cleared.
        The level increases every 10 rows cleared.
        """
        new_level = self.total_lines_cleared // 10
        if new_level > self.level:
            self.level = new_level
        
    def get_random_block(self):
        """
        Select a random block from the available pieces and remove it from the pool.
        Replenishes the pool when only four pieces remain.
        
        Returns:
            Block: The randomly selected Tetris block.
        """
        if len(self.blocks) == 4:
            self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), ZPiece(), TPiece()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        """
        Move the current block one column to the left.
        Reverts movement if the block would collide or go out of bounds.
        """
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        """
        Move the current block one column to the right.
        Reverts movement if the block would collide or go out of bounds.
        """
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        """
        Move the current block one row down.
        Locks the block if it reaches the bottom or collides with another block.
        """
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        """
        Lock the current block into the grid when it can no longer move down.
        Clears full rows, updates score and level, and spawns the next block.
        Ends the game if a new block cannot be placed.
        """
        tiles = self.current_block.get_cell_position()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.place_block_sound.play()
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_line_sound.play()
            self.update_score(rows_cleared)
            self.increase_total_lines_cleared(rows_cleared)
            self.increase_level()
        if self.block_fits() == False:
            self.game_over = True
    
    def rotate(self):
        """
        Rotate the current block clockwise.
        Reverts rotation if the block would collide or go out of bounds.
        """
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotate()

    def block_inside(self):
        """
        Check if the current block is fully inside the grid boundaries.

        Returns:
            bool: True if block is inside the grid, else False
        """
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
    def block_fits(self):
        """
        Check if the current block fits within empty grid spaces.

        Returns:
            bool: True if block does not overlap other blocks, else False
        """
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True
    
    def reset(self):
        """
        Reset the game state to the beginning.
        Clears the grid, resets the score and level, and spawns new blocks.
        """
        self.score = 0
        self.level = 0
        self.total_lines_cleared = 0
        self.grid.reset()
        self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), ZPiece(), TPiece()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.paused = False
        self.game_over = False


    def draw(self, screen):
        """
        Render the game state to the screen, including the grid, current bock, and next block.
        
        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 490)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 480)
        else:
            self.next_block.draw(screen, 270, 470)
