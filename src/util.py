from PIL import Image
import os
import glob

"""util.py
   Badge creation helps functions
"""


def create_page(width: int, height: int):
    """create a page to tile badges on

    Args:
        width (int): pixel width of page
        height (int): pixel height of page

    Returns:
        _type_: PIL Image
    """
    return Image.new("RGB", (width, height), "white")


def save_page(page: Image.Image, name: str, output_dir: str):
    """save badge page to pdf file

    Args:
        page (Image.Image): A PIL Image of tiled badges
        name (str): file name
        output_dir (str): where to save the file
    """
    page.save(os.path.join(output_dir, name + ".pdf"), size=(2550, 3300))


def tile_badges(badge_dir: str, badge_size: tuple, output_dir: str):
    """Tile individual badges into a printable pdf

    Args:
        badge_dir (str): dir of badge image files
        badge_size (tuple): pixel dimensions of badge (w x h)
        output_dir (str): where the resulting pdf shall be saved
    """
    page_index = 0
    card_index = 0
    width, height = int(8.5 * 300), int(11 * 300)  # 300dpi
    page = create_page(width, height)
    cols = int(width // badge_size[0])
    rows = int(height // badge_size[1])

    for card_file in glob.glob(badge_dir + "*.png"):
        card = Image.open(card_file)

        if card_index == 0 or card_index == 1:
            x = int(((badge_size[0]) * (card_index % cols)) + 50)
            y = int(((badge_size[1]) * (card_index // cols)) + 50)
        else:
            x = int(((badge_size[0]) * (card_index % cols)) + 50)
            y = int(((badge_size[1] + 1) * (card_index // cols)) + 50)

        page.paste(card, (x, y))
        print(f"Page {page_index+1}, badge_size {card_index+1}")

        # new page
        if card_index == (rows * cols) - 1:
            save_page(page, str(page_index))
            print(f"Saved page {page_index}")
            page = create_page(width, height)
            page_index += 1
            card_index = 0
        else:
            card_index += 1

    save_page(page, str(page_index), output_dir=output_dir)
