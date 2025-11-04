import pygame
import sys
from game import Game
from colours import Colours

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
game = Game()
GAME_UPDATE = pygame.USEREVENT
game_speed = max(100, 350 - (25 * game.level))
pygame.time.set_timer(GAME_UPDATE, game_speed)
paused = False
MOVE_DELAY = 120
last_move_time = {"left": 0, "right": 0, "down": 0}

# --- Main loop ---
while True:
    # --- Fall Speed based on Level ---
    new_speed = max(100, 350 - (25 * game.level))
    if new_speed != game_speed:
        game_speed = new_speed
        pygame.time.set_timer(GAME_UPDATE, game_speed)

    current_time = pygame.time.get_ticks()

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # --- Game over logic ---
        if game.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.reset()
                paused = False
            continue

        # --- Gameplay controls ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                game.reset()
            elif event.key == pygame.K_UP and not paused:
                game.rotate()
        
        # --- Passive Drop Blocks ---
        if event.type == GAME_UPDATE and not paused:
            game.move_down()

    # --- Gameplay controls - Hold Movement ---
    if not paused and not game.game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and current_time - last_move_time["left"] > MOVE_DELAY:
            game.move_left()
            last_move_time["left"] = current_time

        if keys[pygame.K_RIGHT] and current_time - last_move_time["right"] > MOVE_DELAY:
            game.move_right()
            last_move_time["right"] = current_time

        if keys[pygame.K_DOWN] and current_time - last_move_time["down"] > MOVE_DELAY:
            game.move_down()
            last_move_time["down"] = current_time


    # --- Drawing ---
    screen.fill(Colours.board_colour)

    # --- Score box ---
    pygame.draw.rect(screen, Colours.board_colour_light, score_rect, 0, 10)
    screen.blit(score_surface, (365, 20))
    score_value_surface = game_font.render(str(game.score), True, Colours.text_white)
    screen.blit(score_value_surface, score_value_surface.get_rect(center=score_rect.center))

    # --- Level box ---
    pygame.draw.rect(screen, Colours.board_colour_light, level_rect, 0, 10)
    screen.blit(level_surface, (365, 140))
    level_value_surface = game_font.render(str(game.level), True, Colours.text_white)
    screen.blit(level_value_surface, level_value_surface.get_rect(center=level_rect.center))

    # --- Lines box ---
    pygame.draw.rect(screen, Colours.board_colour_light, lines_rect, 0, 10)
    screen.blit(lines_surface, (365, 260))
    lines_value_surface = game_font.render(str(game.total_lines_cleared), True, Colours.text_white)
    screen.blit(lines_value_surface, lines_value_surface.get_rect(center=lines_rect.center))

    # --- Next box ---
    pygame.draw.rect(screen, Colours.board_colour_light, next_rect, 0, 10)

    # --- Game board ---
    game.draw(screen)

    # --- Game over overlay ---
    if game.game_over:
        screen.blit(game_over_surface, (40, 277))

    pygame.display.update()
    clock.tick(30)
