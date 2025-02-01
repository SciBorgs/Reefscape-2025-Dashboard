'''This file contains functions related to fancy rendering, but does not import from setting'''

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
import numpy
from numpy._typing._array_like import NDArray
from subsystems.lib.render import *

def getArrayImageRGBAFromPath(path: str) -> NDArray[Any]:
    '''Given a path, opens the image, converts it to RGBA, and returns it as a numpy array.'''
    return numpy.array(object=Image.open(fp=path).convert(mode="RGBA"))

def getImageRGBAFromPath(path: str) -> Image.Image:
    '''Given a path, opens the image, converts it to RGBA, and returns the Image.'''
    return Image.open(fp=path).convert(mode="RGBA")

def getFrameFromGIF(image : GifImageFile, frame : int) -> Image.Image:
    '''Given a GIF image, opens the GIF's (frame) frame, converts it to RGBA, and returns it.'''
    image.seek(frame=frame % image.n_frames)
    return image.copy().convert(mode="RGBA")

def generateColorBox(size:tuple[int,int] = (25,25),color: tuple[int,int,int,int] = (255,255,255,255)) -> Image.Image:
    '''Generates a box of (size) size of (color) color'''
    array: NDArray[numpy.uint8] = numpy.empty(shape=(size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :] = color
    return arrayToImage(array=array)

def generateBorderBox(size: tuple[int,int] = (25,25), outlineW:int = 1, color: tuple[int,int,int,int] = (255,255,255,255)) -> Image.Image:
    '''Generates a bordered box with a transparent inside, with transparent space of (size), and an (outlineW) px thick outline of (color) color surrounding it'''
    array: NDArray[numpy.uint8] = numpy.zeros(shape=(size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return arrayToImage(array=array)

def generateInwardsBorderBox(size:tuple[int,int] = (25,25), outlineW:int = 1, color:tuple[int,int,int,int] = (255,255,255,255)) -> Image.Image:
    '''Generates a inwards bordered box with a transparent inside, with transparent space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array: NDArray[numpy.uint8] = numpy.zeros(shape=(size[1], size[0], 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return arrayToImage(array=array)