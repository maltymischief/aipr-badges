from PIL import Image, ImageDraw, ImageFont

"""CONFIGURATION PARAMETERS"""
FIRST_NAME_Y = 350
LAST_NAME_Y = 470
COMPANY_Y = 600
THEME_Y = 140
THEME_X = 680
FONT_NAME = "fonts/StagSans-Medium.otf"
FONT_NAME = "fonts/roboto/Roboto-Black.ttf"
FONT_COMPANY = "fonts/StagSans-Light.otf"
FONT_COMPANY = "fonts/roboto/Roboto-Medium.ttf"
FONT_THEME = "fonts/roboto/Roboto-MediumItalic.ttf"
FONT_MAXSIZE_NAME = 26
FONT_MAXSIZE_COMPANY = 16
FONT_MAXSIZE_THEME = 12
FONT_COLOR_NAME = "#00629b"
FONT_COLOR_COMPANY = "#000000"
FONT_COLOR_THEME = "#FFFFFF"
FOLD_COLOR = "#000000"


class BadgeImage(object):
    """This class represents a badge object with methods to render the badge text."""

    def __init__(self, filename: str):
        """Initialize class

        Args:
            filename (str): path to badge template
        """
        self.img = Image.open(filename)
        self.draw = ImageDraw.Draw(self.img)
        self.width = int(self.img.size[0] * 0.9)

    def drawAlignedText(
        self, pos: tuple, text: str, font: str, color: str, xtransform, ytransform
    ):
        """Render aligned text on badge

        Args:
            pos (tuple): (x,y) position of text
            text (str): the text to print
            font (str): font to use
            color (str): color hex code
            xtransform (_type_): _description_
            ytransform (_type_): _description_
        """

        width, height = font.getsize(text)
        xpos = xtransform(pos[0], width)
        ypos = ytransform(pos[1], height)
        self.draw.text((xpos, ypos), text, fill=color, font=font)

    def drawCenteredText(self, pos: tuple, text: str, font: str, color: str):
        """Render centered text on badge

        Args:
            pos (tuple):  (x,y) position of text
            text (str): the text to print
            font (str): font to use
            color (str): color hex code
        """
        self.drawAlignedText(
            pos, text, font, color, lambda x, w: x - w / 2, lambda y, h: y - h / 2
        )

    def getFitSize(self, startsize: int, text: str):
        """Find the max font size that fits

        Args:
            startsize (int): size of font/text to try
            text (str): the text to print

        Returns:
            (int): the max font size
        """

        size = startsize
        font = ImageFont.truetype(FONT_NAME, size * 300 // 72)
        textwidth, textheight = font.getsize(text)
        while textwidth > self.width:
            size -= 1
            font = ImageFont.truetype(FONT_NAME, size * 300 // 72)
            textwidth, textheight = font.getsize(text)
        return size

    def drawPerson(self, name: str):
        """Render attendees name

        Args:
            name (str): person's name
        """
        linepos = (self.img.size[0] // 2, 500)
        line1pos = (self.img.size[0] // 2, FIRST_NAME_Y)
        line2pos = (self.img.size[0] // 2, LAST_NAME_Y)
        if name.find(" ") >= 0:
            firstname, rest = name.split(" ", 1)
        else:
            firstname, rest = (name, "")
        if rest != "":
            personFont = ImageFont.truetype(
                FONT_NAME, self.getFitSize(FONT_MAXSIZE_NAME, firstname) * 300 // 72
            )
            self.drawCenteredText(line1pos, firstname, personFont, FONT_COLOR_NAME)
            personFont = ImageFont.truetype(
                FONT_NAME, self.getFitSize(FONT_MAXSIZE_NAME, rest) * 300 // 72
            )
            self.drawCenteredText(line2pos, rest, personFont, FONT_COLOR_NAME)
        else:
            personFont = ImageFont.truetype(
                FONT_NAME, self.getFitSize(FONT_MAXSIZE_NAME, name) * 300 // 72
            )
            self.drawCenteredText(linepos, name, personFont, FONT_COLOR_NAME)

    def drawCompany(self, name: str):
        """Render the name of the attendees Company

        Args:
            name (str): the company name
        """
        pos = (self.img.size[0] / 2, COMPANY_Y)
        font = ImageFont.truetype(
            FONT_COMPANY, self.getFitSize(FONT_MAXSIZE_COMPANY, name) * 300 // 72
        )
        self.drawCenteredText(pos, name, font, FONT_COLOR_COMPANY)

    def drawTheme(self, theme: str):
        """render the workshop theme

        Args:
            theme (str): the theme
        """
        pos = (THEME_X, THEME_Y)
        font = ImageFont.truetype(
            FONT_THEME, self.getFitSize(FONT_MAXSIZE_THEME, theme) * 300 // 72
        )
        self.drawCenteredText(pos, theme, font, FONT_COLOR_THEME)

    def save(self, filename: str, doubleSided: bool = False):
        """save the badge as a png image

        Args:
            filename (str): name of the saved file
            doubleSided (bool, optional): Defaults to False.
        """

        if not doubleSided:
            self.img.save(filename)
            return

        newimg = Image.new(
            "RGB", (self.img.size[0] * 2 + 20, self.img.size[1]), FOLD_COLOR
        )
        newimg.paste(self.img, (0, 0))
        newimg.paste(self.img, (self.img.size[0] + 20, 0))
        newimg.save(filename)
