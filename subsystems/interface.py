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
        a - entire screen
        '''
        self.ivos = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling

            -51 : ["a", BranchButtonVisualObject("reset", (111, 865/2-110), "RS")],
            -50 : ["a", BranchButtonVisualObject("go", (111, 865/2), "GO")],
            -49 : ["a", BranchButtonVisualObject("processor", (111, 865/2+110), "PS")],

            -30 : ["a", VerticalSliderVisualObject("GO", (1375, 0), [round(865/2-200)+125,round(865/2+200)+125])],
            -29 : ["a", VerticalSliderVisualObject("NOW", (1505, 0), [round(865/2-200)+125,round(865/2+200)+125])],

            -20 : ["a", CameraVisualObject("FL", (1410, 105))],
            -19 : ["a", CameraVisualObject("FR", (1520, 105))],
            -18 : ["a", CameraVisualObject("BL", (1410, 215))],
            -17 : ["a", CameraVisualObject("BR", (1520, 215))],
        }

        for i in range(12):
            id = "ABCDEFGHIJKL"[i]
            self.ivos[i] = ["a", BranchButtonVisualObject("Branch " + id, (round(math.cos(math.pi * i / 6 - 7 * math.pi /12) * 350) + 1500/2, round(math.sin(math.pi * i / 6 - 7 * math.pi /12) * -350) + 865/2), id)]

        for i in range(1,4+1):
            self.ivos[i+50] = ["a",BranchButtonVisualObject("Level " + str(i),(1809, (3-i-0.5)*(110)+865/2),"L" + str(i))]
        
        algae = ["AB", "CD", "FE", "HG", "JI", "KL"]
        for i in range(6):
            self.ivos[i+70] = ["a",BranchButtonVisualObject("Algae " + algae[i],(round(math.cos(math.pi * i / 3 - 6 * math.pi /12) * 145) + 1500/2, round(math.sin(math.pi * i / 3 - 6 * math.pi /12) * -145) + 865/2), algae[i])]


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
        self.alliance = ""
        self.needUpdate = True
        self.lastElevatorPos = self.comms.getCurrentElevator()
        self.lastCameraEstimates = None
        pass

    def tick(self,mx,my,mPressed,fps):
        '''Entire Screen: `(0,0) to (1919, 864)`: size `(1920, 865)`'''
        self.prevmx = self.mx
        self.prevmy = self.my
        self.mx = mx if (0<=mx and mx<=1919) and (0<=my and my<=864) else self.mx 
        self.my = my if (0<=mx and mx<=1919) and (0<=my and my<=864) else self.my

        if TOUCHSCREEN:
            self.mRising = False
            if (abs(self.prevmx-self.mx)+abs(self.prevmy-self.my) > 0 and (not(mPressed > 0))):
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
                if self.ivos[id][1].getInteractable(self.mx - SECTION_DATA[0][0], self.my - SECTION_DATA[0][1]) and not(id in EXCLUDE_IVOS):
                    self.interacting = id
                    processed = True
                    break
                if processed: break
        if self.interacting != -999:
            self.ivos[self.interacting][1].updatePos(self.mx - SECTION_DATA[0][0], self.my - SECTION_DATA[0][1])
            self.ivos[self.interacting][1].keepInFrame(SECTION_DATA[3][0],SECTION_DATA[3][1],SECTION_DATA[4][0],SECTION_DATA[4][1])

        '''DASHBOARD THINGS'''
        self.comms.tick()
        if self.mRising or self.interacting != self.previousInteracting or self.interacting != -999 or self.previousInteracting != -999:
            self.needUpdate = True
        if self.mRising:
            if 0 <= self.interacting <= 11:
                self.comms.setSelectedBranch("ABCDEFGHIJKL"[self.interacting])
            elif 51 <= self.interacting <= 54:
                self.comms.setSelectedLevel(self.interacting - 50)
            elif 70 <= self.interacting <= 75:
                self.comms.setSelectedAlgae(self.interacting - 70)
            elif self.interacting == -51:
                self.comms.mode = "reset"
                self.comms.transmit()
            elif self.interacting == -50:
                self.comms.transmit()
            elif self.interacting == -49:
                self.comms.setProcessor()
            elif self.interacting == -30:
                self.comms.setElevator(self.ivos[-30][1].getPercent())
            else: pass
        self.comms.setCameraFL(self.ivos[-20][1].enabled)
        self.comms.setCameraFR(self.ivos[-19][1].enabled)
        self.comms.setCameraBL(self.ivos[-18][1].enabled)
        self.comms.setCameraBR(self.ivos[-17][1].enabled)
        if self.interacting == -30 or self.previousInteracting == -30:
            self.comms.setElevator(self.ivos[-30][1].getPercent())
            self.needUpdate = True
        if self.lastElevatorPos != self.comms.getCurrentElevator():
            self.lastElevatorPos = self.comms.getCurrentElevator()
            self.ivos[-29][1].setPercent(self.lastElevatorPos)
            self.needUpdate = True
        currentEstimates = [self.comms.getCameraEstimates(x) for x in range(4)]
        if self.lastCameraEstimates != currentEstimates:
            self.lastCameraEstimates = currentEstimates.copy()
            self.needUpdate = True
        # if self.comms.mode != "elevator": self.ivos[-30][1].setPercent(self.lastElevatorPos)

        alliance = ("blue" if self.comms.getBlueAlliance() else "red") if self.comms.getIsConnected() else "disconnected"
        if self.alliance != alliance:
            for i in range(0,11+1):
                self.ivos[i][1].setAlliance(alliance)
            for i in range(51,54+1):
                self.ivos[i][1].setAlliance(alliance)
            for i in range(70, 76):
                self.ivos[i][1].setAlliance(alliance)
            self.ivos[-51][1].setAlliance(alliance)
            self.ivos[-50][1].setAlliance(alliance)
            self.ivos[-49][1].setAlliance(alliance)
            self.alliance = alliance
            self.needUpdate = True
        if alliance in STIMULATION:
            self.needUpdate = True



    def process(self, im):
        img = im.copy()

        placeOver(img, displayText("FPS: {}".format(self.fps), "m"), (20,20))
        # placeOver(img, displayText(f"Interacting With: {self.interacting}", "m"), (20,55))
        # placeOver(img, displayText(f"length of IVO: {len(self.ivos)}", "m"), (20,90))
        # placeOver(img, displayText(f"Mouse Pos: ({self.mx}, {self.my})", "m"), (200,20))
        # placeOver(img, displayText(f"Mouse Press: {self.mPressed}", "m", colorTXT=(100,255,100,255) if self.mPressed else (255,100,100,255)), (200,55))

        placeOver(img, displayText("Selected: {}{}".format(self.comms.selectedBranch, " " if self.comms.selectedLevel==-1 else self.comms.selectedLevel), "m"), (20,55))
        if not(COMMS):
            placeOver(img, displayText("Comms has been disabled!", "m", colorTXT=(255,100,100,255)), (20,195))

        placeOver(img, displayText("Mode: {}".format(self.comms.mode), "m", colorTXT=(255,255,255,255)), (20,90))
        placeOver(img, displayText("FRC 1155 {}".format(self.comms.getMatch()), "m", colorTXT=(255,255,12,255)), (20,125))
        placeOver(img, displayText("Time Left: {} s".format(round(self.comms.getMatchTime()*10)/10), "m", colorTXT=(255,255,12,255)), (20,160))

        connected = self.comms.getIsConnected()
        placeOver(img, displayText("Comms: Connected: {}".format(connected), "m", colorTXT=(100,255,100,255) if connected else (255,100,100,255)), (20,750))
        if connected:
            placeOver(img, displayText("Comms: Alliance: {}".format("Blue" if self.comms.getBlueAlliance() else "Red"), "m", colorTXT=(100,100,255,255) if self.comms.getBlueAlliance() else (255,100,100,255)), (20,800))
            placeOver(img, displayText("Comms: Request: {}".format(self.comms.getRequest() if self.comms.getRequest()!="" else "Idle"), "m", colorTXT=(100,255,100,255) if self.comms.getRequest()!="" else (100,100,100,255)), (20,825))
            
        else:
            placeOver(img, displayText("Comms: Alliance: Disconnected", "m", colorTXT=(100,100,100,255)), (20,775))
            placeOver(img, displayText("Comms: Nearest: Disconnected", "m", colorTXT=(100,100,100,255)), (20,800))
            placeOver(img, displayText("Comms: Request: Disconnected", "m", colorTXT=(100,100,100,255)), (20,825))

        if self.alliance in STIMULATION:
            subway = getFrameFromGIF(SUBWAY_GIF, time.time()*16)
            placeOver(img, subway, ( 230,  10))
            placeOver(img, subway, (1130,  10))
            placeOver(img, subway, ( 230, 615))
            placeOver(img, subway, (1130, 615))
            placeOver(img, subway, ( 670, 300))

        for id in self.ivos:
            if self.ivos[id][0] == "a":
                if 0 <= id <= 11:
                    self.ivos[id][1].tick(img, self.interacting==id or id=="ABCDEFGHIJKL ".find(self.comms.selectedBranch))
                elif 51 <= id <= 54:
                    self.ivos[id][1].tick(img, self.interacting==id or id==self.comms.selectedLevel+50)
                elif id == -49:
                    self.ivos[id][1].tick(img, self.interacting==id or self.comms.selectedProcessor)
                elif 70 <= id <= 75:
                    self.ivos[id][1].tick(img, self.interacting==id or id==self.comms.selectedAlgae+70)
                elif id == -30:
                    self.ivos[id][1].tick(img, self.interacting==id or self.comms.mode == "elevator")
                elif id == -29:
                    self.ivos[id][1].tick(img, self.interacting==id)
                elif -20 <= id <= -17:
                    self.ivos[id][1].tick(img, self.interacting==id, self.comms.getCameraEstimates(id+20), self.ivos[id][1].enabled)
                else:
                    self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def saveState(self):
        pass

    def close(self):
        pass