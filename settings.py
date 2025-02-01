'''################################################################################################################################'''
'''                                                       DASHBOARD SETTINGS                                                       '''
'''################################################################################################################################'''

# Defines whether the robot is real or not. Determines connection method.
REAL = False

# Changes the method of detection. When set to true, detects sudden mouse teleportation as a click.
TOUCHSCREEN = True 

# Controls communications. Disabling this disables all the dashboard's NetworkTables functions.
COMMS = True

# Sets which modes allow stimulation devices to display. (Note: Stimulation devices affect performance!)
STIMULATION: list[str] = [
    "disconnected",
    # "red",
    # "blue",
    ]





'''################################################################################################################################'''
'''                                                          IVO SETTINGS                                                          '''
'''################################################################################################################################'''

'''Visuals'''
INTERFACE_FPS = 60 # The desired operating FPS
FPS_DAMPENING = 1 # The number of seconds between FPS calculations
TICK_MS = 1 # Extra delay between frames, must be 1 or greater
OCCASIONAL_TICK_MS = 1000 # Should keep above 1 second, as it runs processes that do not need updates every tick

def hexColorToRGBA(hexcolor: str) -> tuple[*tuple[int, ...]]:
    return tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#000000" #Background color
BACKGROUND_COLOR_RGBA: tuple[int, ...] = hexColorToRGBA(hexcolor=BACKGROUND_COLOR)


import os
from PIL import ImageFont
from PIL.Image import Image
from subsystems.lib.simplefancy import *
from subsystems.lib.render import *

# Version
VERSION = "v0.0.0"
SYS_IVOS: list[int] = [-999,-998,-997,-996]


# Fonts
FONTS_ALL: list[str] = ["Orbitron-VariableFont_wght.ttf"]
FONT_PATH: str = os.path.join("resources", "fonts", FONTS_ALL[0])
FONT_LARGE: ImageFont.FreeTypeFont = ImageFont.truetype(font=FONT_PATH, size=35)
FONT_MEDIUM: ImageFont.FreeTypeFont = ImageFont.truetype(font=FONT_PATH, size=15)
FONT_SMALL_MEDIUM: ImageFont.FreeTypeFont = ImageFont.truetype(font=FONT_PATH, size=12)
FONT_SMALL: ImageFont.FreeTypeFont = ImageFont.truetype(font=FONT_PATH, size=10)
def EDITOR_SPACING(x: float) -> float:
    return x*20+15

# Images
TEST_IMAGE: Image.Image = getImageRGBAFromPath(path=os.path.join("resources", "test.png"))
CONNECTED_ALLIANCE_BACKGROUND: Image.Image = getImageRGBAFromPath(path=os.path.join("resources", "bg_connected.png"))
DISCONNECTED_ALLIANCE_BACKGROUND: Image.Image = getImageRGBAFromPath(path=os.path.join("resources", "bg_disconnected.png"))
SUBWAY_GIF: GifImageFile = Image.open(fp=os.path.join("resources", "subway guy.gif")) # type: ignore

# Sections
'''
Region ID : Top Left, Bottom Right, Size, Keep In Relative Top Left, Keep In Relative Top Right
'''
SECTION_DATA: list[tuple[int, int]] = [(   0,   0),(1500, 865),(1500, 865),(   0,   0),(1500, 865)]
SECTION_FRAME_INSTRUCTIONS: list[tuple[Image.Image, tuple[int, int]]] = [(DISCONNECTED_ALLIANCE_BACKGROUND,(0,0)), (CONNECTED_ALLIANCE_BACKGROUND,(0,0))]