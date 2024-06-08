#!/usr/bin/env python
"""
Build the README.md Goots grid.

usage: ./build.py
"""

import math
import os
import shutil
import subprocess

from PIL import Image

# IMAGE_SOURCE_DIR is the directory to list Goots images from.
IMAGE_SOURCE_DIR = "./goots/"

# OUTPUT_FILENAME is the filename to save the grid image to.
OUTPUT_FILENAME = "grid_image.png"

# THUMBNAIL_WIDTH and THUMBNAIL_HEIGHT are the dimensions to resize the geets in the grid.
THUMBNAIL_WIDTH = 128
THUMBNAIL_HEIGHT = 128

# MARGIN is the amount of margin to leave around the geets.
MARGIN = 12

# GAP is the space between geets in the grid.
GAP = 12


def main():
    """Generate the grid for the readme."""

    # Get a list of all image files in the image.
    image_files = [f for f in os.listdir(IMAGE_SOURCE_DIR) if f.endswith(".png")]
    image_files.sort()

    # Determine the number of columns and rows for the grid.
    num_columns = math.ceil(math.sqrt(len(image_files)))
    num_rows = (len(image_files) + num_columns - 1) // num_columns

    # Create a new image with the size of the grid.
    grid_width = num_columns * (THUMBNAIL_WIDTH + GAP) + (2 * MARGIN) - GAP
    grid_height = num_rows * (THUMBNAIL_HEIGHT + GAP) + (2 * MARGIN) - GAP
    grid_image = Image.new("RGB", (grid_width, grid_height))

    # Paste each image onto the grid.
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(IMAGE_SOURCE_DIR, image_file)
        with Image.open(image_path) as image:
            image.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
            row = i // num_columns
            col = i % num_columns
            x = col * (THUMBNAIL_WIDTH + GAP) + MARGIN
            y = row * (THUMBNAIL_HEIGHT + GAP) + MARGIN
            grid_image.paste(image, (x, y))

    # Save the grid image.
    grid_image.save(OUTPUT_FILENAME)

    # Compress using optiping if installed.
    if shutil.which("optipng"):
        subprocess.run(["optipng", "-o9", OUTPUT_FILENAME], check=True)

if __name__ == "__main__":
    main()
