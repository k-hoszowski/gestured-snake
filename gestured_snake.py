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
"""Snake terminal game controlled using hand gestures."""

# Calculating results of AI model
from statistics import mode

# Loading AI model
from joblib import load

# Getting images from webcam
from cv2 import VideoCapture, imwrite

# Obtaining dataframes from images
from pd2img import Pd2Img

# Preprocessing images
from extract_hand import extract_hand

# Basic variables and functions
from snake import *


# Preparing webcam
WEBCAM_PORT = 0
webcam = VideoCapture(WEBCAM_PORT)

# Adjusting game speed to gesture controls
SNAKE_SPEED = 5

# Loading AI classifier
clf = load("model.pkl")

# Controls variable
prediction = -1

# Limiting controls speed
counter = 0


### Main Program Loop ###
while True:
    counter += 1

    if counter == 2:
        # Resetting the timer
        counter = 0

        # Reading input using the camera
        result, image = webcam.read()

        if result:
            # Extracting the hand
            mask = extract_hand(image)
            imwrite("mask.png", mask)

            # Convert mask to dataframe
            df = Pd2Img("mask.png")

            # Recognizing the gesture
            predictions = clf.predict(df.df.iloc[:, 0:3])
            prediction = mode(predictions)

            print(prediction)

            if prediction == 1:
                dir_index += 1
                dir_index %= 4
            elif prediction == 2:
                dir_index -= 1
                dir_index %= 4
        else:
            print("No image detected. Please check your camera or settings.")

    # Alternative to webcam: Handling key events
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
    # If fruit and snake collide then score will be incremented by 10
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
        game_window, WHITE, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10)
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

    # Frame Per Second / Refresh Rate
    fps.tick(SNAKE_SPEED)
