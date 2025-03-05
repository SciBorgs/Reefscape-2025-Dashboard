'''################################################################################################################################'''
'''                                                       DASHBOARD SETTINGS                                                       '''
'''################################################################################################################################'''

# Defines whether the robot is real or not. Determines connection method.
REAL = True

# Changes the method of detection. When set to true, detects sudden mouse teleportation as a click.
TOUCHSCREEN = True

# Controls communications. Disabling this disables all the dashboard's NetworkTables functions.
COMMS = True

# Sets which modes allow stimulation devices to display. (Note: Stimulation devices affect performance!)
STIMULATION = [
    # "disconnected",
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

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#000000" #Background color
BACKGROUND_COLOR_RGBA = hexColorToRGBA(BACKGROUND_COLOR)


import os
from PIL import ImageFont
from subsystems.lib.simplefancy import *
from subsystems.lib.render import *

# Version
VERSION = "HVR (2025NYSU)"
SYS_IVOS = [-999,-998,-997,-996]
EXCLUDE_IVOS = [-29]


# Fonts
FONTS_ALL = ["Orbitron-VariableFont_wght.ttf"]
FONT_PATH = os.path.join("resources", "fonts", FONTS_ALL[0])
FONT_LARGE = ImageFont.truetype(FONT_PATH, 35)
FONT_MEDIUM = ImageFont.truetype(FONT_PATH, 15)
FONT_SMALL_MEDIUM = ImageFont.truetype(FONT_PATH, 12)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 10)
EDITOR_SPACING = lambda x: x*20+15

# Images
TEST_IMAGE = getImageRGBAFromPath(os.path.join("resources", "test.png"))
CONNECTED_ALLIANCE_BACKGROUND = getImageRGBAFromPath(os.path.join("resources", "bg_connected.png"))
DISCONNECTED_ALLIANCE_BACKGROUND = getImageRGBAFromPath(os.path.join("resources", "bg_disconnected.png"))
SUBWAY_GIF = Image.open(os.path.join("resources", "subway guy.gif"))

# Sections
'''
Region ID : Top Left, Bottom Right, Size, Keep In Relative Top Left, Keep In Relative Top Right
'''
SECTION_DATA = [(   0,   0),(1920, 865),(1920, 865),(   0,   0),(1920, 865)]
SECTION_FRAME_INSTRUCTIONS = [[DISCONNECTED_ALLIANCE_BACKGROUND,(0,0)], [CONNECTED_ALLIANCE_BACKGROUND,(0,0)]]