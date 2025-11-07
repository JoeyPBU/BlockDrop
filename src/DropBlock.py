import pygame
import sys
from game import Game
from colours import Colours
from controls import Controls

pygame.init()

# --- Fonts and UI setup ---
game_font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 60)

score_surface = game_font.render("Score", True, Colours.text_white)
score_rect = pygame.Rect(320, 55, 170, 60)
level_surface = game_font.render("Level", True, Colours.text_white)
level_rect = pygame.Rect(320, 175, 170, 60)
lines_surface = game_font.render("Lines", True, Colours.text_white)
lines_rect = pygame.Rect(320, 295, 170, 60)
next_rect = pygame.Rect(320, 415, 170, 180)
game_over_surface = game_over_font.render("Game Over!", True, Colours.text_black)

# --- Window setup ---
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Drop Block!")
clock = pygame.time.Clock()

# --- Game setup ---
controls = Controls()
game = Game()

# --- Setup game drop timer ---
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed()) 

while True:
    events = pygame.event.get()

    actions = controls.get_actions(events)

    if actions["quit"]:
        pygame.quit()
        sys.exit()

    # Handle pause / reset
    if actions["pause_toggle"]:
        game.paused = not game.paused
    if actions["reset"]:
        game.reset()
        pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())

    # Only move blocks if not paused or game over
    if not game.paused and not game.game_over:
        if actions["move_left"]:
            game.move_left()
        if actions["move_right"]:
            game.move_right()
        if actions["move_down"]:
            game.move_down()
        if actions["rotate"]:
            game.rotate()

    for event in events:
        if event.type == GAME_UPDATE and not game.paused and not game.game_over:
            game.move_down()
            pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())
    
    # --- Drawing ---
    screen.fill(Colours.board_colour)

    # Score
    pygame.draw.rect(screen, Colours.board_colour_light, score_rect, 0, 10)
    screen.blit(score_surface, (365, 20))
    score_value_surface = game_font.render(str(game.score), True, Colours.text_white)
    screen.blit(score_value_surface, score_value_surface.get_rect(center=score_rect.center))

    # Level
    pygame.draw.rect(screen, Colours.board_colour_light, level_rect, 0, 10)
    screen.blit(level_surface, (365, 140))
    level_value_surface = game_font.render(str(game.level), True, Colours.text_white)
    screen.blit(level_value_surface, level_value_surface.get_rect(center=level_rect.center))

    # Lines
    pygame.draw.rect(screen, Colours.board_colour_light, lines_rect, 0, 10)
    screen.blit(lines_surface, (365, 260))
    lines_value_surface = game_font.render(str(game.total_lines_cleared), True, Colours.text_white)
    screen.blit(lines_value_surface, lines_value_surface.get_rect(center=lines_rect.center))

    # Next
    pygame.draw.rect(screen, Colours.board_colour_light, next_rect, 0, 10)

    # Game board
    game.draw(screen)

    # --- Game over overlay ---
    if game.game_over:
        screen.blit(game_over_surface, (40, 277))

    pygame.display.update()
    clock.tick(30)
