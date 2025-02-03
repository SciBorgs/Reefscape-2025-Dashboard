'''This file is all about managing what the user sees'''

from doctest import debug
from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast
from subsystems.lib.render import *
from subsystems.lib.fancy import *
from subsystems.lib.simplefancy import *
from subsystems.lib.visuals import *
from subsystems.lib.counter import Counter
from subsystems.comms import *

class Interface:
    def __init__(self) -> None:
        self.mx = 0
        self.my = 0
        self.prevmx = 0
        self.prevmy = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.c = Counter()
        self.comms = Comms()
        self.debugMode = True
        '''Interactable Visual Objects'''
        '''
        Code:
            a - entire screen
            b - branch
            l - level
            s - processor
            g - goal
        '''
        self.ivos = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling

            # Example Usage
            -50 : ["g", BranchButtonVisualObject("go", (111, 865/2+55), "GO")],
            -49 : ["s", BranchButtonVisualObject("processor", (111, 865/2-55), "PS")],
        }

        for i in range(12):
            id = "ABCDEFGHIJKL"[i]
            self.ivos[i] = ["b", BranchButtonVisualObject("Branch " + id, (round(math.cos(math.pi * i / 6 - 7 * math.pi /12) * 350) + 1500/2, round(math.sin(math.pi * i / 6 - 7 * math.pi /12) * -350) + 865/2), id)]

        for i in range(1,5):
            self.ivos[i+50] = ["l",BranchButtonVisualObject("Level " + str(i),(1389, (3-i-0.5)*(110)+865/2),"L" + str(i))]


        '''Control'''
        self.interacting = -999
        self.previousInteracting = -999
        self.stringKeyQueue = ""
        self.previousKeyQueue = []
        self.mouseScroll = 0 
        self.consoleAlerts = []
        self.keybindLastUpdate = time.time()
        self.lastTouchScreenPress = 0
        '''Sliders'''
        self.sliders = []
        self.slidersData = []
        '''DASHBOARD STUFF'''
        self.selectedBranch = " "
        self.selectedLevel = 0
        self.processor = False
        self.alliance = ""
        self.needUpdate = True

    def tick(self,mx,my,mPressed,fps) -> None:
        ''' Called periodically to update the program '''

        ''' Entire Screen: `(0,0) to (1499, 864)`: size `(1500, 865)` '''
        self.prevmx = self.mx
        self.prevmy = self.my
        self.mx = mx if (0<=mx and mx<=1499) and (0<=my and my<=864) else self.mx 
        self.my = my if (0<=mx and mx<=1499) and (0<=my and my<=864) else self.my

        if TOUCHSCREEN:
            self.mRising = False
            if (abs(self.prevmx-self.mx)+abs(self.prevmy-self.my) > 0 and (not(self.mPressed))):
                self.lastTouchScreenPress = self.ticks
                self.mPressed = True
                self.mRising = True
            else:
                self.mPressed = False
            if mPressed > 0: 
                self.lastTouchScreenPress = self.ticks
                self.mPressed = True
        else:
            self.mPressed = mPressed > 0
            self.mRising = mPressed==2

        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks

        '''Interacting With...'''
        self.previousInteracting = self.interacting
        if not(self.mPressed):
            self.interacting = -999
        if self.interacting == -999 and self.mPressed and self.mRising:
            processed = False
            for id in self.ivos:
                if self.ivos[id][1].getInteractable(self.mx - SECTION_DATA[0][0], self.my - SECTION_DATA[0][1]):
                    self.interacting = id
                    processed = True
                    break
                if processed: break
        if self.interacting != -999:
            self.ivos[self.interacting][1].updatePos(self.mx - SECTION_DATA[0][0], self.my - SECTION_DATA[0][1])
            self.ivos[self.interacting][1].keepInFrame(SECTION_DATA[3][0],SECTION_DATA[3][1],SECTION_DATA[4][0],SECTION_DATA[4][1])

        '''DASHBOARD THINGS'''
        self.comms.tick()
        if self.mRising or self.interacting != self.previousInteracting:
            self.needUpdate = True
        if self.mRising:
            if 0 <= self.interacting <= 11:
                new = "ABCDEFGHIJKL"[self.interacting]
                if self.selectedBranch != new: self.selectedBranch = new
                else: self.selectedBranch = " "
            elif 51 <= self.interacting <= 54:
                new = self.interacting - 50
                if self.selectedLevel != new: 
                    self.selectedLevel = new
                    if self.selectedBranch == "processor": self.selectedBranch = " "
                else: 
                    self.selectedLevel = 0
            elif self.interacting == -49:
                self.selectedBranch = "processor"
                self.selectedLevel = 0
            elif self.interacting == -50:
                if self.selectedBranch == "processor":
                    self.comms.setProcessor(True)
                    self.selectedBranch = " "
                    self.selectedLevel = 0
                elif self.selectedBranch != " " and self.selectedLevel != 0:
                    self.comms.setProcessor(False)
                    self.comms.setBranch(self.selectedBranch)
                    self.comms.setLevel(self.selectedLevel)
                    self.selectedBranch = " "
                    self.selectedLevel = 0
                else: pass
            else: pass

        alliance = ("blue" if self.comms.getBlueAlliance() else "red") if self.comms.getIsConnected() else "disconnected"
        if self.alliance != alliance:
            for id in self.ivos:
                if self.ivos[id][0] == "b": self.ivos[id][1].setAlliance(alliance)
                elif self.ivos[id][0] == "l": self.ivos[id][1].setAlliance(alliance)
                elif self.ivos[id][0] == "s": self.ivos[id][1].setAlliance(alliance)
                else: pass
            self.alliance = alliance
            self.needUpdate = True
        if alliance in STIMULATION:
            self.needUpdate = True



    def process(self, im) -> Image:
        ''' Called periodically to update the screen '''
        img = im.copy()

        if self.debugMode:
            placeOver(img, displayText(f"FPS: {self.fps}", "m"), (20,20))
            placeOver(img, displayText(f"Interacting With: {self.interacting}", "m"), (20,55))
            placeOver(img, displayText(f"length of IVO: {len(self.ivos)}", "m"), (20,90))
            placeOver(img, displayText(f"Mouse Pos: ({self.mx}, {self.my})", "m"), (200,20))
            placeOver(img, displayText(f"Mouse Press: {self.mPressed}", "m", colorTXT=(100,255,100,255) if self.mPressed else (255,100,100,255)), (200,55))
            placeOver(img, displayText(f"Selected: {self.selectedBranch}{" " if self.selectedLevel==0 else self.selectedLevel}", "m"), (20,150))
            placeOver(img, displayText(f"Processor: {self.processor}", "m"), (20,120))

        if not(COMMS):
            placeOver(img, displayText(f"Comms has been disabled!", "m", colorTXT=(255,100,100,255)), (20,90))

        if self.comms.getIsConnected():
            placeOver(img, displayText("Alliance: {}".format("Blue" if self.comms.getBlueAlliance() else "Red"), "m", colorTXT=(100,100,255,255) if self.comms.getBlueAlliance() else (255,100,100,255)), (20,775))
            placeOver(img, displayText(f"Nearest: {self.comms.getNearest()}", "m"), (20,800))
            placeOver(img, displayText(f"Connection: {True}", "m", colorTXT=(100,255,100,255)), (20,750))
        
        if not self.comms.getIsConnected():
            placeOver(img, displayText(f"Alliance: Disconnected", "m", colorTXT=(100,100,100,255)), (20,775))
            placeOver(img, displayText(f"Nearest: Disconnected", "m", colorTXT=(100,100,100,255)), (20,800))
            placeOver(img, displayText(f"Connection: {False}", "m", (255,100,100,255)), (20,750))

        if self.alliance in STIMULATION:
            frame = getFrameFromGIF(SUBWAY_GIF, time.time()*16)
            placeOver(img, frame, ( 230,  10))
            placeOver(img, frame, (1130,  10))
            placeOver(img, frame, ( 230, 615))
            placeOver(img, frame, (1130, 615))
            placeOver(img, frame, ( 670, 300))

        for id in self.ivos:
            if self.ivos[id][0] == "b": 
                self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or id=="ABCDEFGHIJKL ".find(self.selectedBranch)) 
            elif self.ivos[id][0] == "l": 
                self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or id==self.selectedLevel+50)
            elif self.ivos[id][0] == "s": 
                self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or self.selectedBranch=="processor")
            else: self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id)

        return img
    
    def toggleDebugMode() -> None:
        ''' Toggle Debug Mode '''
        debugMode = not(debugMode)