'''This file contains functions related to fancy rendering'''

from typing import Any, Literal
from PIL import Image, ImageDraw
from PIL.ImageFont import FreeTypeFont
from settings import FONT_SMALL, FONT_SMALL_MEDIUM, FONT_MEDIUM, FONT_LARGE
from subsystems.lib.simplefancy import *

def displayText(text: str, size : Literal["s","m","sm","ms"], colorBG:tuple[float,float,float,float]|list[float] = (0,0,0,0), colorTXT:tuple[float,float,float,float]|list[float] = (255,255,255,255), bold : bool = False) -> Image.Image:
    '''Returns a numpy array for text, give the text (str), size (s, m, or l for small, medium, large, respectively), and optional background and text color given as (r,g,b,a)'''
    if size == "s":
        font: FreeTypeFont = FONT_SMALL
    elif size == "m":
        font: FreeTypeFont = FONT_MEDIUM
    elif size == "sm" or size == "ms":
        font: FreeTypeFont = FONT_SMALL_MEDIUM
    else: 
        font: FreeTypeFont = FONT_LARGE
   
    fsize: Any = font.font.getsize(text) # type: ignore
    assert type(fsize) == tuple[tuple[int, int], tuple[int, int]]
    
    txtW: int = fsize[0][0]-fsize[1][0] | 0
    txtH: int = fsize[0][1]

    img: Image.Image = Image.new(mode='RGBA', size=(txtW, round(number=txtH*1.5)), color=colorBG)
    ImageDraw.Draw(img).text(xy=(0, 0), text=str(object=text), font=font, fill=colorTXT, stroke_width=(1 if bold else 0))
    return img
