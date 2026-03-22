"""
Image processing utility for blog posts
"""
import os
from PIL import Image


def resize_image(input_path, output_path, width, height):
    """Resize image """
    with Image.open(input_path) as img:
        resized = img.resize((width, height))
        resized.save(output_path)


def create_thumbnail(image_path, thumb_path, size=(150, 150)):
    """Create thumbnail for image"""
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(thumb_path)


def process_upload(image_file, output_dir):
    """Process uploaded image"""
    filename = image_file.filename
    filepath = os.path.join(output_dir, filename)

    image_file.save(filepath)

    base, ext = os.path.splitext(filename)
    thumb_path = os.path.join(output_dir, f"{base}_thumb{ext}")
    create_thumbnail(filepath, thumb_path)

    return {'original': filepath, 'thumbnail': thumb_path}