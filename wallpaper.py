#!/usr/bin/env python
"""
Create a custom Goots wallpaper!

usage: ./wallpaper.py
"""

import os
import random

from PIL import Image, ImageFont, ImageDraw


# IMAGE_SOURCE_DIR is the directory to list Goots images from.
IMAGE_SOURCE_DIR = "./goots/"

# OUTPUT_FILENAME is the filename to save the wallpaper to.
OUTPUT_FILENAME = "wallpaper.webp"

# OUTPUT_FORMAT is the Pillow format string to specify the file format.
OUTPUT_FORMAT = "WebP"

# OUTPUT_QUALITY is the quality to retain when saving the file.
OUTPUT_QUALITY = 60

# WALLPAPER_WIDTH and WALLPAPER_HEIGHT are the dimensions of the wallpaper to generate.
WALLPAPER_WIDTH = 1920
WALLPAPER_HEIGHT = 1080

# THUMBNAIL_WIDTH and THUMBNAIL_HEIGHT are the dimensions to resize the goots in the wallpaper.
THUMBNAIL_WIDTH = 128
THUMBNAIL_HEIGHT = 128

# TILE_AMOUNT is the number of times to randomly add goots to the wallpaper. If there's a bunch of
# empty space, just double this value until it's covered. It just takes longer with bigger values.
TILE_AMOUNT = 2048

# TEXT is the text to display on the wallpaper.
TEXT = "Duck, Duck, GOOTS!"

# FONT_TTF_FILE is the path to a TrueType font to use.
FONT_TTF_FILE = "/System/Library/Fonts/MarkerFelt.ttc"

# FONT_SIZE is the size to render the text.
FONT_SIZE = 200

# FONT_COLOR_* are the three stacked font colors to display (top to bottom) (RGB).
FONT_COLOR_1 = (0, 0, 0)
FONT_COLOR_2 = (255, 255, 255)
FONT_COLOR_3 = (0, 0, 0)

# FONT_SPREAD is the spacing between the layers of the font stack.
FONT_SPREAD = 4


def main():
    """Generate the wallpaper."""
    images = [
        Image.open(os.path.join(IMAGE_SOURCE_DIR, filename)).convert("RGBA")
        for filename in os.listdir(IMAGE_SOURCE_DIR)
        if filename.endswith(".png")
    ]

    wallpaper = Image.new("RGB", (WALLPAPER_WIDTH, WALLPAPER_HEIGHT))
    for _ in range(TILE_AMOUNT):
        image = random.choice(images)
        image.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
        image = image.rotate(random.random() * 360, resample=Image.BICUBIC, expand=True)
        image_x = random.randint(-THUMBNAIL_WIDTH, WALLPAPER_WIDTH)
        image_y = random.randint(-THUMBNAIL_HEIGHT, WALLPAPER_HEIGHT)
        wallpaper.paste(image, (image_x, image_y), mask=image)

    draw = ImageDraw.Draw(wallpaper)
    font = ImageFont.truetype(FONT_TTF_FILE, FONT_SIZE)
    left, top, right, bottom = font.getbbox(TEXT)
    text_x = (WALLPAPER_WIDTH - (right - left)) // 2
    text_y = (WALLPAPER_HEIGHT - (bottom - top)) // 2
    draw.text((text_x + FONT_SPREAD, text_y + FONT_SPREAD), TEXT, fill=FONT_COLOR_3, font=font)
    draw.text((text_x, text_y), TEXT, fill=FONT_COLOR_2, font=font)
    draw.text((text_x - FONT_SPREAD, text_y - FONT_SPREAD), TEXT, fill=FONT_COLOR_1, font=font)

    wallpaper.save(OUTPUT_FILENAME, OUTPUT_FORMAT, quality=OUTPUT_QUALITY)


if __name__ == "__main__":
    main()
