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
            # IVO SYSTEM
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling

            # DASHBOARD TOP CONTROL
            -51 : ["a", LevelButtonVisualObject("reset", (111, 865/2-110), "RS")],
            -50 : ["a", LevelButtonVisualObject("go", (111, 865/2), "GO")],
            -49 : ["a", LevelButtonVisualObject("processor", (111, 865/2+110), "PS")],

            # DASHBOARD MANUAL ELEVATOR
            -30 : ["a", VerticalSliderVisualObject("GO", (1375, 0), [round(865/2-200)+125,round(865/2+200)+125])],
            -29 : ["a", VerticalSliderVisualObject("NOW", (1505, 0), [round(865/2-200)+125,round(865/2+200)+125])],

            # DASHBOARD CAMERAS
            -20 : ["a", CameraVisualObject("FL", (1464, 105))],
            -19 : ["a", CameraVisualObject("FR", (1574, 105))],
            -18 : ["a", CameraVisualObject("BL", (1464, 215))],
            -17 : ["a", CameraVisualObject("BR", (1574, 215))],
            -16 : ["a", CameraVisualObject("BM", (1354, 160))],

            # DASHBOARD BEAMBREAK STATUS
            # -10 : ["a", BeambreakVisualObject("SCL", (300, 215))],
            # - 9 : ["a", BeambreakVisualObject("HPI", (300, 105))],
        }

        for i in range(12):
            id = "ABCDEFGHIJKL"[i]
            self.ivos[i] = ["a", BranchButtonVisualObject("Branch " + id, (round(math.cos(math.pi * i / 6 - 7 * math.pi /12) * 350) + 1500/2, round(math.sin(math.pi * i / 6 - 7 * math.pi /12) * -350) + 865/2), id)]

        for i in range(2,4+1):
            self.ivos[i+50] = ["a",LevelButtonVisualObject("Level " + str(i),(1809, (3-i-0.5)*(110)+865/2),"L" + str(i))]
        
        algae = ["AB", "CD", "FE", "HG", "JI", "KL"]
        for i in range(6):
            self.ivos[i+70] = ["a",LevelButtonVisualObject("Algae " + algae[i],(round(math.cos(math.pi * i / 3 - 6 * math.pi /12) * 145) + 1500/2, round(math.sin(math.pi * i / 3 - 6 * math.pi /12) * -145) + 865/2), algae[i])]


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
        self.enabledReef = [[True for i in range(12)] for ie in range(3)]
        self.selectedLevel = 4
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
                self.ivos[self.interacting][1].enabled = not(self.ivos[self.interacting][1].enabled)
                self.enabledReef[self.selectedLevel-2][self.interacting] = self.ivos[self.interacting][1].enabled
                self.comms.setAvailableBranches("".join([("ABCDEFGHIJKL"[i] if self.ivos[i][1].enabled else " ") for i in range(12)]))
                # print(f"level {self.selectedLevel-2} branch {self.interacting} set to {self.ivos[self.interacting][1].enabled}")
                self.needUpdate = True
            elif 52 <= self.interacting <= 54:
                self.selectedLevel = self.interacting - 50
                for i in range(12):
                    self.ivos[i][1].enabled = self.enabledReef[self.selectedLevel-2][i]
                self.comms.setAvailableBranches("".join([("ABCDEFGHIJKL"[i] if self.ivos[i][1].enabled else " ") for i in range(12)]))
                self.comms.setSelectedLevel(self.interacting - 50)
                self.needUpdate = True
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
            self.needUpdate = True
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

        if self.needUpdate:
            self.comms.setCameraFL(self.ivos[-20][1].enabled)
            self.comms.setCameraFR(self.ivos[-19][1].enabled)
            self.comms.setCameraBL(self.ivos[-18][1].enabled)
            self.comms.setCameraBR(self.ivos[-17][1].enabled)
            self.comms.setCameraBM(self.ivos[-16][1].enabled)
            # self.comms.setBeambreakSCLInvert(self.ivos[-10][1].inverted)
            # self.comms.setBeambreakHPIInvert(self.ivos[-9][1].inverted)
        # if self.comms.mode != "elevator": self.ivos[-30][1].setPercent(self.lastElevatorPos)

        alliance = ("blue" if self.comms.getBlueAlliance() else "red") if self.comms.getIsConnected() else "disconnected"
        if self.alliance != alliance:
            for i in range(0,11+1):
                self.ivos[i][1].setAlliance(alliance)
            for i in range(52,54+1):
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

        placeOver(img, displayText("FPS: {}".format(self.fps), "mml"), (20,20))
        # placeOver(img, displayText(f"Interacting With: {self.interacting}", "m"), (20,55))
        # placeOver(img, displayText(f"length of IVO: {len(self.ivos)}", "m"), (20,90))
        # placeOver(img, displayText(f"Mouse Pos: ({self.mx}, {self.my})", "m"), (200,20))
        # placeOver(img, displayText(f"Mouse Press: {self.mPressed}", "m", colorTXT=(100,255,100,255) if self.mPressed else (255,100,100,255)), (200,55))

        if not(COMMS):
            placeOver(img, displayText("Comms has been disabled!", "mml", colorTXT=(255,100,100,255)), (20,160))

        placeOver(img, displayText("Mode: {}".format(self.comms.mode), "mml", colorTXT=(255,255,255,255)), (20,55))
        placeOver(img, displayText("FRC 1155 {}".format(self.comms.getMatch()), "mml", colorTXT=(255,255,12,255)), (20,90))
        placeOver(img, displayText("Time Left: {} s".format(round(self.comms.getMatchTime()*10)/10), "mml", colorTXT=(255,255,12,255)), (20,125))

        connected = self.comms.getIsConnected()
        placeOver(img, displayText("Comms: Connected: {}".format(connected), "mml", colorTXT=(100,255,100,255) if connected else (255,100,100,255)), (20,750))
        if connected:
            placeOver(img, displayText("Comms: Alliance: {}".format("Blue" if self.comms.getBlueAlliance() else "Red"), "mml", colorTXT=(100,100,255,255) if self.comms.getBlueAlliance() else (255,100,100,255)), (20,785))
            placeOver(img, displayText("Comms: Request: {}".format(self.comms.getRequest() if self.comms.getRequest()!="" else "Idle"), "mml", colorTXT=(100,255,100,255) if self.comms.getRequest()!="" else (100,100,100,255)), (20,820))
        else:
            placeOver(img, displayText("Comms: Alliance: Disconnected", "mml", colorTXT=(100,100,100,255)), (20,785))
            placeOver(img, displayText("Comms: Request: Disconnected", "mml", colorTXT=(100,100,100,255)), (20,820))

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
                    # REEF BRANCHES
                    self.ivos[id][1].tick(img)
                elif 52 <= id <= 54:
                    # REEF LEVELS
                    self.ivos[id][1].tick(img, self.interacting==id or id==self.selectedLevel+50)
                elif id == -49:
                    # PROCESSOR
                    self.ivos[id][1].tick(img, self.interacting==id or self.comms.selectedProcessor)
                elif 70 <= id <= 75:
                    # REEF ALGAE
                    self.ivos[id][1].tick(img, self.interacting==id or id==self.comms.selectedAlgae+70)
                elif id == -30:
                    # MANUAL TARGET ELEVATOR
                    self.ivos[id][1].tick(img, self.interacting==id or self.comms.mode == "elevator")
                elif id == -29:
                    # MANUAL CURRENT ELEVATOR
                    self.ivos[id][1].tick(img, self.interacting==id)
                elif -20 <= id <= -16:
                    # CAMERAS
                    self.ivos[id][1].tick(img, self.interacting==id, self.comms.getCameraEstimates(id+20), self.ivos[id][1].enabled)
                elif id == -10:
                    # SCORAL BEAMBREAK
                    self.ivos[id][1].tick(img, self.interacting==id, self.comms.getBeambreakSCL())
                elif id == -9:
                    # HOPPER BEAMBREAK
                    self.ivos[id][1].tick(img, self.interacting==id, self.comms.getBeambreakHPI())
                else:
                    # UNKNOWN 
                    self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def saveState(self):
        pass

    def close(self):
        pass