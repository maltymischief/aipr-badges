#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import os
import glob
from src import DataFileReader
from src import BadgeImage
from src import util

"""create_badges.py
   This module creates workshop badges from registrant xlsx data.
   Requirements: registry data  (.xlsx)
                 badge template (.png)
   Outputs: individual badges   (.png)
            badge sheets        (.pdf)
"""

"""CONFIGURATION PARAMETERS"""
CARD = (1200, 900)
PADDING = (1, 1)
REGISTRANT_FILE = "sample/AIPR_Sample_Registrants.xlsx"
REGISTRANT_SHEET = "Registrants"
TEMPLATE_FILE = "sample/aipr_badge_template.png"
THEME = "Building Trust in Artificial Intelligence"
OUTPUT_DIR = "output/"

if __name__ == "__main__":

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    count = 0
    for name, company in DataFileReader.DataFileReader(
        REGISTRANT_FILE, REGISTRANT_SHEET
    ).getData():
        print(f"{name}, {company}")
        badge = BadgeImage.BadgeImage(TEMPLATE_FILE)
        badge.drawPerson(str(name))
        badge.drawCompany(str(company))
        badge.drawTheme(str(THEME))
        badge.save(os.path.join(OUTPUT_DIR, "badge_" + str(count) + ".png"))
        count += 1

    print("\n%d badges created" % (count))

    page_index = 0
    card_index = 0
    card_folder = OUTPUT_DIR
    tiled_folder = OUTPUT_DIR

    width, height = int(8.5 * 300), int(11 * 300)  # 300dpi
    page = util.create_page(width, height)
    cols = int(width // CARD[0])
    rows = int(height // CARD[1])

    for card_file in glob.glob(OUTPUT_DIR + "*.png"):
        card = Image.open(card_file)

        if card_index == 0 or card_index == 1:
            x = int(((CARD[0]) * (card_index % cols)) + 50)
            y = int(((CARD[1]) * (card_index // cols)) + 50)
        else:
            x = int(((CARD[0]) * (card_index % cols)) + 50)
            y = int(((CARD[1] + 1) * (card_index // cols)) + 50)

        page.paste(card, (x, y))
        print(f"Page {page_index+1}, Card {card_index+1}")

        # new page
        if card_index == (rows * cols) - 1:
            util.save_page(page, str(page_index))
            print(f"Saved page {page_index}")
            page = util.create_page(width, height)
            page_index += 1
            card_index = 0
        else:
            card_index += 1

    util.save_page(page, str(page_index), output_dir=OUTPUT_DIR)
