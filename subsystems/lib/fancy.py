"""This file contains functions related to fancy rendering"""

from typing import Literal
from PIL import Image, ImageDraw
from PIL.ImageFont import FreeTypeFont
from settings import FONT_SMALL, FONT_SMALL_MEDIUM, FONT_MEDIUM, FONT_LARGE
from subsystems.lib.simplefancy import *


def displayText(
    text: str,
    size: Literal["s", "m", "l", "sm"],
    colorBG: tuple[float, float, float, float] = (0, 0, 0, 0),
    colorTXT: tuple[int, int, int, int] = (255, 255, 255, 255),
    bold: bool = False,
) -> Image.Image:
    """Returns a numpy array for text, give the text (str), size (s, m, or l for small, medium, large, respectively), and optional background and text color given as (r,g,b,a)"""
    if size == "s":
        font: FreeTypeFont = FONT_SMALL
    elif size == "m":
        font: FreeTypeFont = FONT_MEDIUM
    elif size == "sm":
        font: FreeTypeFont = FONT_SMALL_MEDIUM
    elif size == "l":
        font: FreeTypeFont = FONT_LARGE

    txtW: int = int(font.getbbox(text=text)[2])
    txtH: float = font.getbbox(text=text)[3]

    img: Image.Image = Image.new(
        mode="RGBA", size=(txtW, round(number=txtH * 1.5)), color=colorBG
    )
    ImageDraw.Draw(im=img).text(
        xy=(0, 0),
        text=str(object=text),
        font=font,
        fill=colorTXT,
        stroke_width=(1 if bold else 0),
    )
    return img
