from tkinter import FIRST
from PIL import Image
import os
import pandas as pd

import glob

from src import DataFileReader
from src import BadgeImage


#####################################################
######## User Defined Values ########################
#####################################################

REGISTRANT_FILE = 'AIPR_Sample_Registrants.xlsx'
REGISTRANT_SHEET = 'Registrants'
OUTPUT_DIR = "out/"
TEMPLATE_FILE = "aipr_badge_template.png"
CARD = (1200,900)
PADDING = (1, 1)
THEME = "Building Trust in Artificial Intelligence"



def create_paper(width, height):
    return Image.new('RGB', (width, height), 'white')

def save_paper(paper, name):
    #paper = paper.resize((2550,3300), Image.ANTIALIAS)
    paper.save(os.path.join(OUTPUT_DIR, name + '.pdf'), size=(2550,3300))

if __name__ == "__main__":
    
    count = 0
    reader = DataFileReader.DataFileReader(REGISTRANT_FILE, REGISTRANT_SHEET)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for name, company in reader.getData():
        print(name, company)
        badge = BadgeImage.BadgeImage(TEMPLATE_FILE)
        badge.drawPerson(str(name))
        badge.drawCompany(str(company))
        badge.drawTheme(str(THEME))
        badge.save(os.path.join(OUTPUT_DIR, "badge_" + str(count) + ".png"))
        count += 1
        
    print("\n%d badges created" % (count))
    
paper_index = 0
card_index = 0
card_folder = OUTPUT_DIR
tiled_folder = OUTPUT_DIR

width, height = int(8.5 * 300), int(11 * 300) #300dpi
paper = create_paper(width, height)
cols = int(width//CARD[0])
rows = int(height//CARD[1])

for card_file in glob.glob(OUTPUT_DIR + "*.png"):
    card = Image.open(card_file)
   
    if card_index == 0 or card_index == 1:
        x = int(((CARD[0]) * (card_index % cols)) + 50)
        y = int(((CARD[1]) * (card_index // cols)) + 50)
    else:
        x = int(((CARD[0]) * (card_index % cols)) + 50 )
        y = int(((CARD[1]+1) * (card_index // cols)) + 50)
        
    paper.paste(card,(x, y))
    print(f"Paper {paper_index}, Card {card_index}")

    # new page
    if card_index == (rows * cols) - 1: 
        save_paper(paper, str(paper_index))
        print (f"Saved Paper {paper_index}")
        paper = create_paper(width, height)
        paper_index += 1
        card_index = 0
    else:
        card_index += 1

save_paper(paper, str(paper_index))

