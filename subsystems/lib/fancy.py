'''This file contains functions related to fancy rendering'''

from PIL import Image, ImageDraw
from settings import FONT_SMALL, FONT_SMALL_MEDIUM, FONT_MEDIUM, FONT_LARGE, FONT_MEDIUM_LARGE, FONT_MEDIUM_MEDIUM_LARGE
from subsystems.lib.simplefancy import *

def displayText(text: str, size, colorBG:tuple|list = (0,0,0,0), colorTXT:tuple|list = (255,255,255,255), bold = False):
    '''Returns a numpy array for text, give the text (str), size (s, m, or l for small, medium, large, respectively), and optional background and text color given as (r,g,b,a)'''
    if size == "s":
        font = FONT_SMALL
    elif size == "m":
        font = FONT_MEDIUM
    elif size == "sm" or size == "ms":
        font = FONT_SMALL_MEDIUM
    elif size == "ml":
        font = FONT_MEDIUM_LARGE
    elif size == "mml":
        font = FONT_MEDIUM_MEDIUM_LARGE
    else: 
        font = FONT_LARGE
    fsize = font.font.getsize(str(text))
    txtW = fsize[0][0]-fsize[1][0]
    txtH = fsize[0][1] #-fsize[1][1]
    img = Image.new('RGBA', (txtW, round(txtH*1.5)), colorBG)
    ImageDraw.Draw(img).text((0, 0), str(text), font=font, fill=colorTXT, stroke_width=(1 if bold else 0))
    return img
