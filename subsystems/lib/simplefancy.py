'''This file contains functions related to fancy rendering, but does not import from setting'''

from PIL import Image
import numpy
from subsystems.lib.render import *

def getArrayImageRGBAFromPath(path):
    '''Given a path, opens the image, converts it to RGBA, and returns it as a numpy array.'''
    return numpy.array(Image.open(path).convert("RGBA"))

def getImageRGBAFromPath(path):
    '''Given a path, opens the image, converts it to RGBA, and returns the Image.'''
    return Image.open(path).convert("RGBA")

def getFrameFromGIF(image, frame):
    '''Given a GIF image, opens the GIF's (frame) frame, converts it to RGBA, and returns it.'''
    image.seek(round(frame) % image.n_frames)
    return image.copy().convert("RGBA")

def generateColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color'''
    array = numpy.empty((size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :] = color
    return arrayToImage(array)

def generateBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a bordered box with a transparent inside, with transparent space of (size), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return arrayToImage(array)

def generateInwardsBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a inwards bordered box with a transparent inside, with transparent space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1], size[0], 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return arrayToImage(array)