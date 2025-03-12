'''This file contains classes all about the visual objects the user sees'''

import math, time
from subsystems.lib.render import placeOver
from subsystems.lib.fancy import *
from settings import *

'''Point Stuff'''
def addP(coord1: tuple|list, coord2: tuple|list):
    '''Adds the x and y coordinates of 2 points given in (x,y) format'''
    return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def subtractP(coord1: tuple|list, coord2: tuple|list):
    '''Subtracts (x1,y1) by (x2,y2) given in (x,y) format'''
    return (coord1[0]-coord2[0],coord1[1]-coord2[1])


'''Hitboxes'''

class RectangularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific bounding box'''
    def __init__(self, bbox:tuple|list = (10,10), ix = 0, iy = 0):
        '''Bounding box will NOT be centered!'''
        self.bbox, self.ix, self.iy = bbox, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the bounding box of interaction'''
        return (self.ix < rmx) and (rmx < (self.ix+self.bbox[0])) and (self.iy < rmy) and (rmy < (self.iy+self.bbox[1]))
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getBBOX(self): return self.bbox
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setBBOX(self, nbbox): self.bbox = nbbox

'''Visual Objects'''

class VisualObject:
    '''Basic template for Visual Objects'''
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)
    def keyAction(self, keys):
        pass
    
class DummyVisualObject(VisualObject):
    '''I sit around doing nothing and can store data.'''
    def __init__(self, name, pos:tuple|list, data = None):
        self.type = "dummy"
        self.name = name
        self.lastInteraction = time.time()
        self.positionO = RectangularPositionalBox((0,0), pos[0], pos[1])
        self.data = data
    def tick(self, img, visualactive, actives):
        pass
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pass
    def getInteractable(self,rmx,rmy):
        return False
    
class BranchButtonVisualObject(VisualObject):
    '''A custom button for branches.'''
    def __init__(self, name, pos:tuple|list, branch):
        self.type = "branch button"
        self.name = name
        self.lastInteraction = time.time()
        self.enabled = True
        self.activeTime = 0

        overlayText = displayText(str(branch), "l", bold = True)

        self.imgDisconnected = generateBorderBox((94,94), 3, (0,0,0,0), (0,0,0,100))
        placeOver(self.imgDisconnected, overlayText, (50, 50), True)

        self.imgRed = generateBorderBox((94,94), 3, (0,0,0,0), (100,0,0,100))
        placeOver(self.imgRed, overlayText, (50,50), True)

        self.imgBlue = generateBorderBox((94,94), 3, (0,0,0,0), (0,0,100,100))
        placeOver(self.imgBlue, overlayText, (50,50), True)

        self.frameDisabled = generateBorderBox((94,94), 3, (150,150,150,255), (0,0,0,0))

        self.frameActive = generateBorderBox((94,94), 3, (254,221,16,255), (0,0,0,0))

        self.img = self.imgDisconnected
        self.positionO = RectangularPositionalBox((self.frameActive.width,self.frameActive.height), pos[0] - 50, pos[1] - 50)
    def tick(self, img):
        placeOver(img, self.img, self.positionO.getPosition(), False)
        placeOver(img, self.frameActive if self.enabled else self.frameDisabled, self.positionO.getPosition(), False)
    def setAlliance(self, alliance):
        if alliance == "blue": self.img = self.imgBlue
        elif alliance == "red": self.img = self.imgRed
        else: self.img = self.imgDisconnected
    def updatePos(self, rmx, rmy):
        pass


class LevelButtonVisualObject(VisualObject):
    '''A custom button for levels.'''
    def __init__(self, name, pos:tuple|list, level):
        self.type = "level button"
        self.name = name
        self.lastInteraction = time.time()

        overlayText = displayText(str(level), "l", bold = True)

        self.imgDisconnected = generateBorderBox((94,94), 3, (50,50,50,255), (0,0,0,100))
        placeOver(self.imgDisconnected, overlayText, (50, 50), True)

        self.imgRed = generateBorderBox((94,94), 3, (255,0,0,255), (100,0,0,100))
        placeOver(self.imgRed, overlayText, (50, 50), True)

        self.imgBlue = generateBorderBox((94,94), 3, (0,0,255,255), (0,0,100,100))
        placeOver(self.imgBlue, overlayText, (50, 50), True)
        
        self.imgActive = generateBorderBox((94,94), 3, (254,221,16,255), (100,50,0,100))
        placeOver(self.imgActive, overlayText, (50, 50), True)
        
        self.img = self.imgDisconnected
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0] - 50, pos[1] - 50)
    def tick(self, img, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.imgActive if active else self.img, self.positionO.getPosition(), False)
    def setAlliance(self, alliance):
        if alliance == "blue": self.img = self.imgBlue
        elif alliance == "red": self.img = self.imgRed
        else: self.img = self.imgDisconnected
    def updatePos(self, rmx, rmy):
        pass

class VerticalSliderVisualObject(VisualObject):
    '''A slider!!! No way!!! (vertical) modified'''
    def __init__(self, name, pos:tuple|list=(random.randrange(0,20), random.randrange(0,20)), limitY = [0,100]):
        self.type = "slider"
        self.name = name
        self.lastInteraction = time.time()
        self.origPos = (pos[0], limitY[0])
        self.positionO = RectangularPositionalBox((100,100), subtractP(self.origPos, (25,25)))
        self.positionO.setPosition(self.origPos)
        self.limitY = limitY

        barColor = (150,150,150,255)
        self.bar = generateColorBox((56,abs(limitY[1]-limitY[0])+58), (0,0,0,0))
        spacer = generateColorBox((56,4), barColor)
        placeOver(self.bar, spacer, (0,0))
        placeOver(self.bar, spacer, (0,abs(limitY[1]-limitY[0])-6+58))
        placeOver(self.bar,generateColorBox((4,abs(limitY[1]-limitY[0])+56), barColor), (26,0))

        overlayText = displayText(self.name, "sm", colorTXT = (254,221,16,255), bold = 1)
        self.imgIdle = generateBorderBox((50,50), 3, (150,150,150,255), (100,50,0,100))
        placeOver(self.imgIdle, overlayText, (25,25), True)
        self.imgActive = generateBorderBox((50,50), 3, (254,221,16,255), (100,50,0,100))
        placeOver(self.imgActive, overlayText, (25,25), True)

    def tick(self, img, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.bar, self.origPos)
        placeOver(img, self.imgActive if active else self.imgIdle, self.positionO.getPosition())
    def updatePos(self, rmx, rmy):
        self.positionO.setY(max(self.limitY[0], min(rmy, self.limitY[1])))
    def setPercent(self, percent):
        self.positionO.setY(max(self.limitY[0], min(self.limitY[0]+(1-percent)*(self.limitY[1]-self.limitY[0]), self.limitY[1])))
    def getPercent(self):
        return 1-((self.positionO.getY() - self.limitY[0])/(abs(self.limitY[1]-self.limitY[0])))
    

class CameraVisualObject(VisualObject):
    '''A custom button for enabling, disabling, and showing the estimates state of cameras.'''
    def __init__(self, name, pos:tuple|list):
        self.type = "camera button"
        self.name = name
        self.lastInteraction = time.time()
        self.enabled = True
        self.activeTime = 0

        overlayText = displayText(str(name), "l", bold = True)

        self.backRed = generateBorderBox((94,94), 3, (0,0,0,0), (150,0,0,200))
        placeOver(self.backRed, overlayText, (50,50), True)

        self.backGreen = generateBorderBox((94,94), 3, (0,0,0,0), (0,150,0,200))
        placeOver(self.backGreen, overlayText, (50,50), True)

        self.frameDisabled = generateBorderBox((94,94), 3, (150,150,150,255), (0,0,0,0))
        placeOver(self.frameDisabled, overlayText, (50,50), True)

        self.frameActive = generateBorderBox((94,94), 3, (254,221,16,255), (0,0,0,0))
        placeOver(self.frameActive, overlayText, (50,50), True)
        
        self.positionO = RectangularPositionalBox((self.frameActive.width,self.frameActive.height), pos[0] - 50, pos[1] - 50)
    def tick(self, img, active, estimates = False, enabled = False):
        if active: 
            self.lastInteraction = time.time()
            self.activeTime += 1
        else: self.activeTime = 0
        if self.activeTime == 1:
            self.enabled = not(self.enabled)
        placeOver(img, self.backGreen if estimates else self.backRed, self.positionO.getPosition(), False)
        placeOver(img, self.frameActive if self.enabled or enabled else self.frameDisabled, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass

class BeambreakVisualObject(VisualObject):
    '''A custom button for inverted and showing the state of beambreaks. Ideally not used except for worst case.'''
    def __init__(self, name, pos:tuple|list, invert = False):
        self.type = "beambreak button"
        self.name = name
        self.lastInteraction = time.time()
        self.inverted = invert
        self.activeTime = 0

        overlayText = displayText(str(name), "ml", bold = True)

        self.overlayBroken = displayText("BKN", "m", bold = False)
        self.overlayNotBroken = displayText("N/BKN", "m", bold = False)

        self.frameInverted = generateBorderBox((94,94), 3, (255,0,0,255), (0,0,0,0))
        placeOver(self.frameInverted, overlayText, (50,50), True)

        self.frameNormal = generateBorderBox((94,94), 3, (0,255,0,255), (0,0,0,0))
        placeOver(self.frameNormal, overlayText, (50,50), True)
        
        self.positionO = RectangularPositionalBox((self.frameNormal.width,self.frameNormal.height), pos[0] - 50, pos[1] - 50)
    def tick(self, img, active, broken = False):
        if active: 
            self.lastInteraction = time.time()
            self.activeTime += 1
        else: self.activeTime = 0
        if self.activeTime == 1:
            self.inverted = not(self.inverted)
        placeOver(img, self.overlayBroken if (not(broken) if self.inverted else broken) else self.overlayNotBroken, addP(self.positionO.getPosition(), (50, 80)), True)
        placeOver(img, self.frameInverted if self.inverted else self.frameNormal, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass