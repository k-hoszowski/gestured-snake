#
 #   Copyright 2023 Krzysztof Hoszowski
 #
 #   This file is part of Gestured Snake.
 #
 #   Gestured Snake is free software: you can redistribute it and/or
 #   modify it under the terms of the GNU General Public License as published by
 #   the Free Software Foundation, either version 3 of the License, or
 #   (at your option) any later version.
 #
 #   Gestured Snake is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
 #   Public License for more details.
 #
 #   You should have received a copy of the GNU General Public License along
 #   with Gestured Snake. If not, see <https://www.gnu.org/licenses/>.
 #
#
"""Simple Snake terminal game."""

import sys
from time import sleep
from random import randrange
import pygame

## Function definitions
def show_score(score, color, font, size):
    """Displaying score obtained so far in the game."""

    # Creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # Create the display surface Score_surface
    score_surface = score_font.render("Score: " + str(score), True, color)

    # Create a rectangular object for the text surface object
    score_rect = score_surface.get_rect()

    # Displaying text
    game_window.blit(score_surface, score_rect)


def game_over(score):
    """\"Game over\" message with final score."""

    # Creating font object my_font
    my_font = pygame.font.SysFont("calibri", 60)

    # Creating a text surface on which text will be drawn
    game_over_surface = my_font.render("Final score: " + str(score), True, RED)

    # Create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()

    # Setting position of the text
    game_over_rect.midtop = (WINDOW_X / 2, WINDOW_Y / 4)

    # Draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # Quit the game after 3 seconds
    sleep(3)

    # Quitting
    pygame.quit()
    sys.exit(0)


### Initializing the game ###
# Constant snake speed / FPS
SNAKE_SPEED = 15

# Window size
WINDOW_X = 720
WINDOW_Y = 480

# Defining colors
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)

# Initializing pygame
pygame.init()

# Initialize game window
pygame.display.set_caption("Snake")
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Defining snake default position
snake_position = [140, 70]

# Defining initial 4 blocks of snake body
snake_body = [[130, 70], [120, 70], [110, 70], [100, 70]]

# Fruit position
fruit_position = [
    randrange(1, (WINDOW_X // 10)) * 10,
    randrange(1, (WINDOW_Y // 10)) * 10,
]

# Whether to spawn more fruit
fruit_spawn = True

# Setting default snake direction towards right
directions = ("UP", "RIGHT", "DOWN", "LEFT")
dir_index = 1

# Initial score
score = 0


### Main Program Loop ###
if __name__ == "__main__":
    while True:
        # Handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dir_index += 1
                    dir_index %= 4
                if event.key == pygame.K_DOWN:
                    dir_index -= 1
                    dir_index %= 4

        # Moving the snake
        if directions[dir_index] == "UP":
            snake_position[1] -= 10
        if directions[dir_index] == "DOWN":
            snake_position[1] += 10
        if directions[dir_index] == "LEFT":
            snake_position[0] -= 10
        if directions[dir_index] == "RIGHT":
            snake_position[0] += 10

        # Snake body growing mechanism
        # If fruit and snake collide then scores will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if (
            snake_position[0] == fruit_position[0]
            and snake_position[1] == fruit_position[1]
        ):
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [
                randrange(1, (WINDOW_X // 10)) * 10,
                randrange(1, (WINDOW_Y // 10)) * 10,
            ]

        fruit_spawn = True
        game_window.fill(BLACK)

        for pos in snake_body:
            pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(
            game_window,
            WHITE,
            pygame.Rect(fruit_position[0], fruit_position[1], 10, 10),
        )

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > WINDOW_X - 10:
            game_over(score)
        if snake_position[1] < 0 or snake_position[1] > WINDOW_Y - 10:
            game_over(score)

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over(score)

        # Displaying score
        show_score(score, WHITE, "calibri", 20)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(SNAKE_SPEED)
