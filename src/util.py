from PIL import Image
import os


def create_page(width, height):
    return Image.new("RGB", (width, height), "white")


def save_page(page, name, output_dir):
    page.save(os.path.join(output_dir, name + ".pdf"), size=(2550, 3300))
