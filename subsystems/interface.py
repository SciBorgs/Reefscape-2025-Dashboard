'''This file is all about managing what the user sees'''

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
    def __init__(self):
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
        '''Interactable Visual Objects'''
        '''
        Code:
        a - example A
        b - example B
        '''
        self.ivos = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling

            # Example Usage
            -50 : ["a", BranchButtonVisualObject("go", (111, 865/2-55), "GO")],
            -49 : ["a", BranchButtonVisualObject("processor", (111, 865/2+55), "PS")],
        }

        for i in range(12):
            id = "ABCDEFGHIJKL"[i]
            self.ivos[i] = ["a", BranchButtonVisualObject("Branch " + id, (round(math.cos(math.pi * i / 6 - 7 * math.pi /12) * 350) + 1500/2, round(math.sin(math.pi * i / 6 - 7 * math.pi /12) * -350) + 865/2), id)]

        for i in range(1,5):
            self.ivos[i+50] = ["a",BranchButtonVisualObject("Level " + str(i),(1389, (3-i-0.5)*(110)+865/2),"L" + str(i))]


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
        self.selectedBranch = ""
        self.selectedLevel = 0
        pass

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1499, 864)`: size `(1500, 865)`'''
        self.prevmx = self.mx
        self.prevmy = self.my
        self.mx = mx if (0<=mx and mx<=1499) and (0<=my and my<=864) else self.mx 
        self.my = my if (0<=mx and mx<=1499) and (0<=my and my<=864) else self.my

        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        if TOUCHSCREEN:
            if abs(self.prevmx-self.mx)+abs(self.prevmy-self.my) > 0:
                self.lastTouchScreenPress = time.time()
                self.mPressed = True
                self.mRising = True
            elif  abs(time.time()-self.lastTouchScreenPress) < 0.1:
                self.mPressed = True
            else:
                self.mPressed = mPressed

        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks

        '''Mouse Scroll'''
        self.mouseScroll = mouseScroll
        if abs(self.mouseScroll) > 0:
            if self.interacting == -999: self.interacting = -996
            if self.interacting == -996:
                print("scrolling!")
        else:
            if self.interacting == -996: self.interacting = -999
        pass

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
        if 0 <= self.interacting <= 11:
            self.selectedBranch = "ABCDEFGHIJKL"[self.interacting]
        elif 51 <= self.interacting <= 54:
            self.selectedLevel = self.interacting - 50
        elif self.interacting == -50:
            if self.selectedBranch != "" and self.selectedLevel != 0:
                self.comms.setProcessor(False)
                self.comms.setBranch(self.selectedBranch)
                self.comms.setLevel(self.selectedLevel)
        elif self.interacting == -49:
            self.comms.setProcessor(True)
        else: pass
        alliance = ("blue" if self.comms.getBlueAlliance() else "red") if self.comms.getIsConnected() else "disconnected"
        for i in range(0,11+1):
            self.ivos[i][1].setAlliance(alliance)
        for i in range(51,54+1):
            self.ivos[i][1].setAlliance(alliance)




    def process(self, im):
        img = im.copy()

        placeOver(img, displayText(f"FPS: {self.fps}", "m"), (20,20))
        # placeOver(img, displayText(f"Interacting With: {self.interacting}", "m"), (20,55))
        # placeOver(img, displayText(f"length of IVO: {len(self.ivos)}", "m"), (20,90))
        # placeOver(img, displayText(f"Mouse Pos: ({self.mx}, {self.my})", "m"), (200,20))
        # placeOver(img, displayText(f"Mouse Press: {self.mPressed}", "m", colorTXT=(100,255,100,255) if self.mPressed else (255,100,100,255)), (200,55))

        connected = self.comms.getIsConnected()
        placeOver(img, displayText(f"Comms: Connected: {connected}", "m", colorTXT=(100,255,100,255) if connected else (255,100,100,255)), (20,775))
        if connected:
            placeOver(img, displayText(f"Comms: Alliance: {"Blue" if self.comms.getBlueAlliance() else "Red"}", "m", colorTXT=(100,100,255,255) if self.comms.getBlueAlliance() else (255,100,100,255)), (20,800))
            placeOver(img, displayText(f"Comms: Nearest: {self.comms.getNearest()}", "m"), (20,825))
        else:
            placeOver(img, displayText(f"Comms: Alliance: Disconnected", "m", colorTXT=(100,100,100,255)), (20,800))
            placeOver(img, displayText(f"Comms: Nearest: Disconnected", "m", colorTXT=(100,100,100,255)), (20,825))

        for id in self.ivos:
            if self.ivos[id][0] == "a":
                if 0 <= id <= 11:
                    self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or id=="ABCDEFGHIJKL".find(self.selectedBranch))
                elif 51 <= id <= 54:
                    self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or id==self.selectedLevel+50)
                else:
                    self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id)

        return img    

    def saveState(self):
        pass

    def close(self):
        pass