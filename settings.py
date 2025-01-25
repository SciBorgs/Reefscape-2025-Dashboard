
'''DASHBOARD SETTINGS'''
REAL = False











'''################################################################################################################################'''
'''                                                          IVO SETTINGS                                                          '''
'''################################################################################################################################'''

'''Visuals'''
INTERFACE_FPS = 60 # The desired operating FPS
FPS_DAMPENING = 1 # The number of seconds between FPS calculations
TICK_MS = 1 # Extra delay between frames, must be 1 or greater
OCCASIONAL_TICK_MS = 5000 # Should keep above 1 second, as it runs processes that do not need updates every tick

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#333247" #Background color
FRAME_COLOR      = "#524f6b" #Borders and Frame color
SELECTED_COLOR   = "#bebcd5" #Selected Element color
VOID_COLOR       = "#84829b" #Void color

BACKGROUND_COLOR_RGBA = hexColorToRGBA(BACKGROUND_COLOR)
FRAME_COLOR_RGBA      = hexColorToRGBA(FRAME_COLOR     )
SELECTED_COLOR_RGBA   = hexColorToRGBA(SELECTED_COLOR  )
VOID_COLOR_RGBA       = hexColorToRGBA(VOID_COLOR      )


'''Saving'''
import os, time
PATH_SAVE_DEFAULT = os.path.join("saves")

FORMAT_TIME = lambda x: time.strftime("%I:%M:%S %p %m/%d/%Y", time.localtime(x))

from PIL import ImageFont
from subsystems.lib.simplefancy import *
from subsystems.lib.render import *

# Version
VERSION = "v0.0.0"
SYS_IVOS = [-999,-998,-997,-996]

# Sections
'''
- Example A Area: `(  22,  22) to ( 671, 675)` : size `( 650, 654)`
- Example B Area: `( 694,  22) to (1343, 675)` : size `( 650, 654)`

Region ID : Top Left, Bottom Right, Size, Keep In Relative Top Left, Keep In Relative Top Right
'''
SECTIONS_DATA = {
    " ": [(   0,   0),(   0,   0),(   0,   0),(   0,   0),(   0,   0)],
    "a": [(  22,  22),( 671, 675),( 650, 654),(   0,   0),( 650, 654)],
    "b": [( 694,  22),(1343, 675),( 650, 654),(   0,   0),( 650, 654)],
}
SECTIONS_FRAME_INSTRUCTIONS = {
    " ": [],
    "a": genereateThemedBorderRectangleInstructions(( 650, 654),hexColorToRGBA(FRAME_COLOR)),
    "b": genereateThemedBorderRectangleInstructions(( 650, 654),hexColorToRGBA(FRAME_COLOR)),
}
SECTIONS = list(SECTIONS_DATA.keys())

# Fonts
FONTS_ALL = ["Orbitron-VariableFont_wght.ttf"]
FONT_PATH = os.path.join("resources", "fonts", FONTS_ALL[0])
FONT_LARGE = ImageFont.truetype(FONT_PATH, 24)
FONT_MEDIUM = ImageFont.truetype(FONT_PATH, 15)
FONT_SMALL_MEDIUM = ImageFont.truetype(FONT_PATH, 12)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 10)
EDITOR_SPACING = lambda x: x*20+15

# Images
TEST_IMAGE = getImageRGBAFromPath(os.path.join("resources", "test.png"))