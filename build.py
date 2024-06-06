import os
from PIL import Image

# copilot generated basically all of this code

image_source_path = './goots'

# Get a list of all image files in the image
image_files = [f for f in os.listdir(image_source_path) if f.endswith(('.png'))]

image_width = 100  # Width of each image in the grid
image_height = 100  # Height of each image in the grid

# Determine the number of columns and rows for the grid
num_columns = 6  # Number of columns in the grid
num_rows = (len(image_files) + num_columns - 1) // num_columns  # Number of rows in the grid
# Create a new image with the size of the grid
grid_width = num_columns * image_width  # Assuming all images have the same width
grid_height = num_rows * image_height  # Assuming all images have the same height
grid_image = Image.new('RGB', (grid_width, grid_height))
# Paste each image onto the grid
for i, image_file in enumerate(image_files):
    image_path = os.path.join(image_source_path, image_file)
    image = Image.open(image_path)
    image.thumbnail((image_width, image_height))  # Resize the image to fit the grid cell
    row = i // num_columns
    col = i % num_columns
    x = col * image_width
    y = row * image_height
    grid_image.paste(image, (x, y))
# Save the grid image
grid_image.save('grid_image.png')