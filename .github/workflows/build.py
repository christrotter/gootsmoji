import os
from PIL import Image

# copilot generated basically all of this code

image_source_path = '../goots'

# Get a list of all image files in the image
image_files = [f for f in os.listdir(image_source_path) if f.endswith(('.png'))]

print(image_files)

# Generate HTML to display the thumbnails
html = '# preview \n <html><body> \n'
for image_file in image_files:
    print(image_file)
    image_path = os.path.join(image_source_path, image_file)
    print("image path: ", image_path)
    html += f'<img src="{image_path}" alt="{image_file}"> \n'
html += '</body></html>'

# Open readme.md in read mode and read the content
with open('README.md', 'r') as f:
    content = f.read()

# Find the index of the "# preview" text
index = content.find("# preview")

# Remove everything after the "# preview" text
new_content = content[:index]

# Open readme.md in write mode and write the updated content
with open('README.md', 'w') as f:
    f.write(new_content)

# Open readme.md in append mode and write the html content
with open('README.md', 'a') as f:
    f.write(html)