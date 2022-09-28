#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

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
CARD_SIZE = (1200, 900)
PADDING = (1, 1)
REG_FILE = "sample/AIPR_Sample_Registrants.xlsx"
REG_SHEET = "Registrants"
TEMPLATE_FILE = "sample/aipr_badge_template.png"
THEME = "Building Trust in Artificial Intelligence"
OUTPUT_DIR = "output/"

if __name__ == "__main__":

    # if output doesn't exist, make it
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # iterate over registration entries and create a badge for each participant
    count = 0
    for name, company in DataFileReader.DataFileReader(REG_FILE, REG_SHEET).getData():
        print(f"{name}, {company}")
        badge = BadgeImage.BadgeImage(TEMPLATE_FILE)
        badge.drawPerson(str(name))
        badge.drawCompany(str(company))
        badge.drawTheme(str(THEME))
        badge.save(os.path.join(OUTPUT_DIR, "badge_" + str(count) + ".png"))
        count += 1

    print("\n%d badges created" % (count))

    util.tile_badges(badge_dir=OUTPUT_DIR,
                     badge_size=CARD_SIZE, 
                     output_dir=OUTPUT_DIR
                     )
