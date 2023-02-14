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
"""Converting images into pandas dataframes and CSV files."""

# Loading filepaths into Python in bulk
from glob import glob

# Converting images into pandas dataframes
from pd2img import Pd2Img

# Concatenating dataframes
from pandas import concat


# Loading the images
paths = [
    glob("images/input_clockwise/*.png"),
    glob("images/input_anticlockwise/*.png"),
    glob("images/input_nothing/*.png"),
]

# Output of function
dataframes = []


def im2df():
    """Take all images from given paths and return
    a dataframe for each path in a list."""

    for path in paths:
        # First run to add headers
        dframe = Pd2Img(path[0]).df

        # The remaining images
        for i in range(1, len(path)):
            dfi = Pd2Img(path[i]).df

            # Concatenating the dataframes
            dframe = concat([dframe, dfi])

        dataframes.append(dframe)
    return dataframes
