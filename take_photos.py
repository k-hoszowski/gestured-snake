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
"""Taking a number of photos (for AI training)."""

# Getting images from webcam
from cv2 import VideoCapture, imwrite

# Processing images
from extract_hand import extract_hand


# Preparing webcam
WEBCAM_PORT = 0
webcam = VideoCapture(WEBCAM_PORT)


for i in range(20):
    # Reading input using the camera
    result, image = webcam.read()

    if result:
        # Extracting the hand
        mask = extract_hand(image)

        # Save mask
        imwrite("mask.png", mask)  # Checking the images
        imwrite("".join([str(i), ".png"]), mask)  # Actual save
