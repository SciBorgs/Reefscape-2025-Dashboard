'''This file contains functions for rendering related purposes'''

from typing import Any, Union
from PIL import Image, ImageEnhance
import numpy, math

from numpy.typing import NDArray

# Convert

def imageToArray(img: Image.Image) -> numpy.ndarray[Any,numpy.dtype[numpy.uint8]]:
    '''Converts an Image into a numpy array'''
    return numpy.array(object=img)

def arrayToImage(array: numpy.ndarray[Any,numpy.dtype[numpy.uint8]]) -> Image.Image:
    '''Converts a numpy array to an Image'''
    return Image.fromarray(obj=array.astype(dtype="uint8"), mode="RGBA")

def saveImage(array: numpy.ndarray[Any,numpy.dtype[numpy.uint8]], output_path: str) -> None:
    img: Image.Image = Image.fromarray(obj=array)
    img.save(fp=output_path)


# Image

def clip(img: Union[Image.Image, numpy.ndarray[Any,numpy.dtype[numpy.uint8]]], cliplen: int, direction: str) -> numpy.ndarray[Any,numpy.dtype[numpy.uint8]]:
    '''Returns an image with clipped cliplen from a given direction'''
    img = numpy.array(object=img)
    cliplen = round(number=cliplen)
    if direction == "N":
        return img[cliplen:, :, :]
    elif direction == "S":
        return img[:-cliplen, :, :]
    elif direction == "E":
        return img[:, cliplen:, :]
    elif direction == "W":
        return img[:, :-cliplen, :]
    else:
        return img

def addBlank(img: Union[Image.Image, numpy.ndarray[Any,numpy.dtype[numpy.uint8]]], add: int, direction: str, color: tuple[int, int, int, int] = (0, 0, 0, 0), thirdaxis: bool = True) -> numpy.ndarray[Any,numpy.dtype[numpy.uint8]]:
    '''Returns the image with added add "empty" pixels in a given direction'''
    img = numpy.array(object=img)
    y : float = img.shape[:2][0]
    x : float = img.shape[:2][1]
    if direction == 'N': 
        temp: numpy.ndarray[Any, numpy.dtype[numpy.uint8]] = numpy.zeros(shape=(add, int(x), 4) if thirdaxis else (add, int(x)), dtype=img.dtype)
        temp[:, :] = color
        return numpy.vstack(tup=(temp, img))
    elif direction == 'S': 
        temp: numpy.ndarray[Any, numpy.dtype[numpy.uint8]] = numpy.zeros(shape=(add, int(x), 4) if thirdaxis else (add, int(x)), dtype=img.dtype)
        temp[:, :] = color
        return numpy.vstack(tup=(img, temp))
    elif direction == 'E': 
        temp: numpy.ndarray[Any, numpy.dtype[numpy.uint8]] = numpy.zeros(shape=(add, int(y), 4) if thirdaxis else (add, int(y)), dtype=img.dtype)
        temp[:, :] = color
        return numpy.hstack(tup=(img, temp))
    elif direction == 'W': 
        temp: numpy.ndarray[Any, numpy.dtype[numpy.uint8]] = numpy.zeros(shape=(add, int(y), 4) if thirdaxis else (add, int(y)), dtype=img.dtype)
        temp[:, :] = color
        return numpy.hstack(tup=(temp, img))
    else:
        return img

def getRegion(
    img: Union[Image.Image, numpy.ndarray[Any,numpy.dtype[numpy.uint8]]],
    cornerA: Union[tuple[int, int], list[int]],
    cornerB: Union[tuple[int, int], list[int]],
    exact: int = 2,
    color: tuple[int, int, int, int] = (0, 0, 0, 0),
    thirdaxis: bool = True
) -> numpy.ndarray[Any,numpy.dtype[numpy.uint8]]:
    '''Returns a region of an image, given two coordinates relative to (0,0) of the image'''
    imgC = numpy.array(object=img)
    if thirdaxis:
        y : float = imgC.shape[0]
        x : float = imgC.shape[1]
        _: float = imgC.shape[2]
    else:
        y : float = imgC.shape[:2][0]
        x : float = imgC.shape[:2][1]
    pointA: list[int] = [round(number=min(cornerA[0], cornerB[0])), round(number=min(cornerA[1], cornerB[1]))]
    pointB: list[int] = [round(number=max(cornerA[0], cornerB[0])), round(number=max(cornerA[1], cornerB[1]))]
    if exact > 0:
        if pointA[0] < 0:
            add: int = abs(pointA[0])
            imgC: numpy.ndarray[Any, numpy.dtype[numpy.uint8]] = addBlank(img=imgC, add=add, direction="W", color=color, thirdaxis=thirdaxis)
            pointA[0] += add 
            pointB[0] += add
        if pointA[1] < 0:
            add = abs(pointA[1])
            imgC = addBlank(img=imgC, add=add, direction="N", color=color, thirdaxis=thirdaxis)
            pointA[1] += add 
            pointB[1] += add
        if exact > 1:
            if x < pointB[0]:
                add = abs(pointB[0] - int(x))
                imgC = addBlank(img=imgC, add=add, direction="E", color=color, thirdaxis=thirdaxis)
                pointB[0] += add
            if y < pointB[1]:
                add = abs(pointB[1] - int(y))
                imgC = addBlank(img=imgC, add=add, direction="S", color=color, thirdaxis=thirdaxis)
                pointB[1] += add
    area: numpy.ndarray[Any, numpy.dtype[numpy.uint8]] = imgC[round(number=pointA[1]):round(number=pointB[1] + 1), round(number=pointA[0]):round(number=pointB[0] + 1)]
    return area

def merge(img1: Union[Image.Image, numpy.ndarray[Any,numpy.dtype[numpy.uint8]]], img2: Union[Image.Image, numpy.ndarray[Any,numpy.dtype[numpy.uint8]]]) -> NDArray[numpy.signedinteger[Any]]:
    '''Returns an array of the average of the values of two given images/numpy arrays as a numpy array'''
    img1 = numpy.array(object=img1)
    img2 = numpy.array(object=img2)
    return img1 // 2 + img2 // 2

def arrayPlaceOver(
    img1: numpy.ndarray[Any,numpy.dtype[numpy.uint8]],
    img2: numpy.ndarray[Any,numpy.dtype[numpy.uint8]],
    position: Union[list[int], tuple[int, int]],
    center: bool = False
) -> bool:
    '''Modifies image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as numpy arrays'''
    if center:
        position = (round(number=position[0] - img2.shape[1] * 0.5), round(number=position[1] - img2.shape[0] * 0.5))
    
    img1H : float = img1.shape[:2][0]
    img1W : float = img1.shape[:2][1]

    img2H : float = img2.shape[:2][0]
    img2W : float = img2.shape[:2][1]

    if position[1] > img1H or -position[1] > img2H:
        return False
    if position[0] > img1W or -position[0] > img2W:
        return False

    startX: int = math.floor(max(position[0], 0))
    startY: int = math.floor(max(position[1], 0))
    endX: float = math.floor(min(position[0] + img2W, img1W))
    endY: float = math.floor(min(position[1] + img2H, img1H))

    img2 = img2[round(number=max(-position[1], 0)):round(number=(max(-position[1], 0) + (endY - startY))), round(number=max(-position[0], 0)):round(number=(max(-position[0], 0) + (endX - startX)))]

    alpha_overlay = img2[:, :, 3] / 255.0
    overlayRGB: numpy.ndarray[Any,numpy.dtype[numpy.uint8]] = img2[:, :, :3]
    backgroundRGB: numpy.ndarray[Any,numpy.dtype[numpy.uint8]] = img1[startY:endY, startX:endX, :3]
    alpha_background = img1[startY:endY, startX:endX, 3] / 255.0

    if numpy.any(img2[:, :, 3] < 0):
        alpha_background: NDArray[numpy.float64] = img1[startY:endY, startX:endX, 3].astype(dtype=numpy.float64)
        alpha_background += img2[:, :, 3].astype(dtype=numpy.float64)
        alpha_background[alpha_background < 0] = 0
        alpha_background[alpha_background > 255] = 255
        img1[startY:endY, startX:endX, 3] = alpha_background.astype(dtype=numpy.uint8)
    else:
        combined_alpha = alpha_overlay + alpha_background * (1 - alpha_overlay)
        blendedRGB: NDArray[numpy.uint8] = (overlayRGB * alpha_overlay[:, :, None] + backgroundRGB * (1 - alpha_overlay[:, :, None])).astype(dtype=numpy.uint8)
        img1[startY:endY, startX:endX, :3] = blendedRGB
        img1[startY:endY, startX:endX, 3] = (combined_alpha * 255).astype(dtype=numpy.uint8)

    return True

def dArrayPlaceOver(img1: numpy.ndarray[Any,numpy.dtype[numpy.uint8]], img2: numpy.ndarray[Any,numpy.dtype[numpy.uint8]], position: Union[list[int], tuple[int, int]]) -> numpy.ndarray[Any,numpy.dtype[numpy.uint8]]:
    '''Dangerously returns an overlayed version of image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as numpy arrays, by directly adding it'''
    if img1.shape == img2.shape:
        img1 += img2
    else:
        try:
            img2 = numpy.hstack(tup=[numpy.zeros(shape=(img2.shape[0], position[0], 4), dtype=numpy.uint8), img2])
            img2 = numpy.hstack(tup=[img2, numpy.zeros(shape=(img2.shape[0], img1.shape[1] - img2.shape[1], 4), dtype=numpy.uint8)])
            img2 = numpy.vstack(tup=[numpy.zeros(shape=(position[1], img2.shape[1], 4), dtype=numpy.uint8), img2])
            img2 = numpy.vstack(tup=[img2, numpy.zeros(shape=(img1.shape[0] - img2.shape[0], img2.shape[1], 4), dtype=numpy.uint8)])
            img1 += img2
        except Exception as e:
            print(f"Error: {e}")
            pass
    return img1

def placeOver(img1: Image.Image, img2: Image.Image, position: Union[list[int], tuple[int, int]], center: bool = False) -> bool:
    '''Modifies image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as PIL images'''
    if center:
        x: int = (position[0] - round(number=img2.width / 2), position[1] - round(number=img2.height / 2))[0]
        y: int = (position[0] - round(number=img2.width / 2), position[1] - round(number=img2.height / 2))[1]
    else:
        x = position[0]
        y = position[1]

    if (x < img1.width) and (y < img1.height) and (x + img2.width > 0) and (y + img2.height > 0):
        if (x < 0) or (y < 0) or (x + img2.width > img1.width) or (y + img2.height > img1.height):
            sx: int = math.floor(max(x, 0))
            sy: int = math.floor(max(y, 0))
            crop: Image.Image = img2.crop(box=(
                max(-x, 0),
                max(-y, 0),
                max(-x, 0) + (math.floor(min(x + img2.width, img1.width)) - sx),
                max(-y, 0) + (math.floor(min(y + img2.height, img1.height)) - sy)
            ))
            img1.paste(im=crop, box=(sx, sy), mask=crop)
        else:
            img1.paste(im=img2, box=(round(number=x), round(number=y)), mask=img2)
    return True

def rotateDeg(img: Image.Image, degrees:float) -> Image.Image:
    '''Returns a copy of the Image as a rotated version of the given Image by (degrees) degrees, using the 0 up CCW rotation system'''
    return img.rotate(angle=degrees,expand=True)

def rotateDegHundred(img: Image.Image, cent:float) -> Image.Image:
    '''Returns a copy of the given Image as a rotated version of the given Image by (cent) cents, using the 0 up CCW rotation system. 100 cents = 360 degrees, 1 cent = 3.6 degrees'''
    return img.rotate(angle=cent*3.6,expand=True)

def setSize(img: Image.Image, size:float) -> Image.Image:
    '''Returns a copy of the given Image scaled by size, given the size change (given with 100 as normal, >100 scale up, <100 scale down)'''
    x: int = img.width
    y: int = img.height
    return img.resize(size=(max(1, (round(number=x*(size/100)))),max(1, round(y*(size/100)))),resample=Image.Resampling.NEAREST)

def setSizeSize(img: Image.Image, size:tuple[int,int]) -> Image.Image:
    '''Returns a copy of the given image with set size size, given the exact target sizes'''
    return img.resize(size=(max(1,size[0]), max(1,size[1])), resample=Image.Resampling.NEAREST)

def setSizeSizeBlur(img: Image.Image, size:tuple[int,int]) -> Image.Image:
    '''Returns a copy of the given image with set size size, given the exact target sizes, resampling is hamming!'''
    return img.resize(size=(size[0], size[1]), resample=Image.Resampling.HAMMING)

def setColorEffect(img: Image.Image, colorEffect:float) -> Image.Image:
    '''Returns a copy of the given Image with a color shift, given the shift value (given 0-100)'''
    imgc: NDArray[numpy.uint8] = imageToArray(img=img)
    imgc[:, :, 0:2] += numpy.uint8(colorEffect/100*255)
    return arrayToImage(array=imgc)

def setTransparency(img: Image.Image, transparency:float) -> Image.Image:
    '''Returns a copy of the given Image with transparency multiplied, given the transparency value (given 0-100, 0 = clear, 100 = normal)'''
    if transparency == 100: return img
    imgc: NDArray[numpy.uint8] = imageToArray(img=img)
    imgMask = imgc[:, :, 3] * (transparency/100)
    imgc[:, :, 3] = imgMask
    return arrayToImage(array=imgc)

def setBrightnessEffect(img: Image.Image, brightness:float) -> Image.Image:
    '''Returns a copy of the given Image with brightness changed, given the brightness value (<0 = darker, 0 = normal, >0 = brighter)'''
    return ImageEnhance.Brightness(image=img).enhance(factor=(brightness+100)/100)

def setBlur(img: Image.Image, pixelation:float) -> Image.Image:
    '''Returns a copy of the given Image blured, given the blur value (given 0-100, 0 = normal, 100 = very pixelated)'''
    if pixelation <= 1: return img
    x: int = img.width
    y: int = img.height
    imgc: Image.Image = img.resize(size=(max(1, (round(number=x/pixelation*(x/100)))),max(1, round(number=y/pixelation*(y/100)))))
    return imgc.resize(size=(round(number=x),round(number=y)))

def setLimitedSize(img: Image.Image, size:int) -> Image.Image:
    '''Returns a copy of the given Image scaled to fix inside a (size x size) shape'''
    x: int = img.width
    y: int = img.height
    scaleFactor: float = size/x if x>y else size/y
    return img.resize(size=(max(1, (round(number=x*scaleFactor))),max(1, round(number=y*scaleFactor))))

def setLimitedSizeSize(img: Image.Image, size:tuple[int,int]) -> Image.Image:
    '''Returns a copy of the given Image scaled to fix inside a size shape'''
    x: int = img.width
    y: int = img.height
    scaleFactor: float = size[0]/x
    if size[1]/y < scaleFactor: scaleFactor = size[1]/y
    return img.resize(size=(max(1, (round(number=x*scaleFactor))),max(1, round(number=y*scaleFactor))), resample=Image.Resampling.NEAREST)

def resizeImage(img: Image.Image, size:tuple[int,int]) -> Image.Image:
    '''Returns a copy of the given Image scaled to shape size'''
    return img.resize(size=size, resample=Image.Resampling.NEAREST)