#
 #   Copyright 2023 Krzysztof Hoszowski and Chimelie Nzelibe
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
"""
   Performs binary thresholding on an image based on R
   content in RGB image, aiming to extract the human hand
   from it for further processing.
"""

from time import time
import cv2 as cv
from numpy import zeros


def extract_hand(img):
    """Returns binary mask of human body from picture."""

    # Dimension of image (square)
    shape = 256

    # Downscale the image for faster processing
    img = cv.resize(img, (shape, shape))

    # Create a binary mask
    msk = zeros((shape, shape, 1), dtype="u1")

    # Filter variable
    fil = 30

    # Loop over the pixels in the image
    for y in range(fil, img.shape[0] - fil):
        for x in range(fil, img.shape[1] - fil):
            # OpenCV uses BGR representation instead of RGB
            b, g, r = img[y, x]

            # Optimization: convert unsigned int into signed int.
            r = int(r)
            g = int(g)
            b = int(b)

            # Alternative algorithm
            # if r > 80 and g > 30 and b > 20 and r > g and r > b and abs(r-g) > 15:

            # Compare the RGB values
            if r > g + fil and r > b + fil:
                # Keep the pixel
                msk[y, x] = 255
    return msk


# Test the extracting on 8 examples
if __name__ == "__main__":
    for i in range(1, 9):

        # Timing the program
        start_time = time()

        # Load the image
        image = cv.imread("".join([str(i), ".jpeg"]), cv.IMREAD_COLOR)

        mask = extract_hand(image)

        print(f"-- It took {time() - start_time} seconds --")

        # Show the binary image
        cv.imshow("binary mask", mask)
        cv.imwrite("".join([str(i), ".png"]), mask)
        cv.waitKey(0)
        cv.destroyAllWindows()
