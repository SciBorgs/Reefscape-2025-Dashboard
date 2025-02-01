'''This file is all about managing what the user sees'''

from typing import LiteralString

from PIL.Image import Image
from PIL.ImageTk import PhotoImage
from settings import *
import time
from subsystems.lib.render import *
from subsystems.lib.fancy import *
from subsystems.lib.simplefancy import *
from subsystems.lib.visuals import *
from subsystems.lib.counter import Counter
from subsystems.comms import *
from subsystems.lib.visuals import BranchButtonVisualObject, DummyVisualObject

class Interface:
    def __init__(self) -> None:
        self.mx: int = 0
        self.my: int = 0
        self.prevmx: float = 0
        self.prevmy: float = 0
        self.mPressed: bool = False
        self.mRising: bool = False
        self.fps: float = 0
        self.ticks: int = 0
        self.c = Counter()
        self.comms = Comms()
        '''Interactable Visual Objects'''
        '''
        Code:
        a - entire screen
        '''
        self.ivos: dict[int, tuple[str, VisualObject]] = {
            -999 : (" ", DummyVisualObject(name="dummy", pos=(0,0))), # used for not interacting with anything
            -998 : (" ", DummyVisualObject(name="dummy", pos=(0,0))), # used for text boxes
            -997 : (" ", DummyVisualObject(name="dummy", pos=(0,0))), # used by keybinds
            -996 : (" ", DummyVisualObject(name="dummy", pos=(0,0))), # used by scrolling

            # Example Usage
            -50 : ("a", BranchButtonVisualObject(name="go", pos=(111, 865/2-55), branch="GO")),
            -49 : ("a", BranchButtonVisualObject(name="processor", pos=(111, 865/2+55), branch="PS")),
        }

        for i in range(12):
            id: LiteralString = "ABCDEFGHIJKL"[i]
            self.ivos[i] = ("a", BranchButtonVisualObject(name="Branch " + id, pos=(round(number=math.cos(math.pi * i / 6 - 7 * math.pi /12) * 350) + 1500/2, round(number=math.sin(math.pi * i / 6 - 7 * math.pi /12) * -350) + 865/2), branch=id))

        for i in range(1,5):
            self.ivos[i+50] = ("a",BranchButtonVisualObject(name="Level " + str(object=i),pos=(1389, (3-i-0.5)*(110)+865/2),branch="L" + str(object=i)))


        '''Control'''
        self.interacting: int = -999
        self.previousInteracting: int = -999
        self.stringKeyQueue: Literal[''] = ""
        self.previousKeyQueue: list[str] = []
        self.mouseScroll: float = 0 
        self.consoleAlerts: list[str] = []
        self.keybindLastUpdate: float = time.time()
        self.lastTouchScreenPress: float = 0
        '''Sliders'''
        self.sliders: list[Any] = []
        self.slidersData: list[Any] = []
        '''DASHBOARD STUFF'''
        self.selectedBranch: str = " "
        self.selectedLevel: int = 0
        self.alliance: str = ""
        self.needUpdate = True
        pass

    def tick(self,mx: int,my: int,mPressed: int,fps: float) -> None:
        '''Entire Screen: `(0,0) to (1499, 864)`: size `(1500, 865)`'''
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
        self.deltaTicks: int = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks

        '''Interacting With...'''
        self.previousInteracting = self.interacting
        if not(self.mPressed):
            self.interacting = -999
        if self.interacting == -999 and self.mPressed and self.mRising:
            processed = False
            for id in self.ivos:
                if self.ivos[id][1].getInteractable(rmx=self.mx - SECTION_DATA[0][0], rmy=self.my - SECTION_DATA[0][1]):
                    self.interacting = id
                    processed = True
                    break
                if processed: break
        if self.interacting != -999:
            try:
                self.ivos[self.interacting][1].updatePos(self.mx - SECTION_DATA[0][0], self.my - SECTION_DATA[0][1]) # type: ignore
                self.ivos[self.interacting][1].keepInFrame(minX=SECTION_DATA[3][0],minY=SECTION_DATA[3][1],maxX=SECTION_DATA[4][0],maxY=SECTION_DATA[4][1]) # type: ignore
            except:
                pass

        '''DASHBOARD THINGS'''
        self.comms.tick()
        if self.mRising or self.interacting != self.previousInteracting:
            self.needUpdate = True
        if self.mRising:
            if 0 <= self.interacting <= 11:
                new: str | int = "ABCDEFGHIJKL"[self.interacting]
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
                    self.comms.setProcessor(boolean=True)
                    self.selectedBranch = " "
                    self.selectedLevel = 0
                elif self.selectedBranch != " " and self.selectedLevel != 0:
                    self.comms.setProcessor(boolean=False)
                    self.comms.setBranch(branch=self.selectedBranch)
                    self.comms.setLevel(level=self.selectedLevel)
                    self.selectedBranch = " "
                    self.selectedLevel = 0
                else: pass
            else: pass

        alliance: Literal['blue','red','disconnected'] = ("blue" if self.comms.getBlueAlliance() else "red") if self.comms.getIsConnected() else "disconnected"
        if self.alliance != alliance:
            for i in range(0,11+1):
                try:
                    self.ivos[i][1].setAlliance(alliance) # type: ignore
                except:
                    pass
            for i in range(51,54+1):
                try:
                    self.ivos[i][1].setAlliance(alliance) # type: ignore
                except:
                    pass
            
            try:
                self.ivos[-50][1].setAlliance(alliance) # type: ignore
                self.ivos[-49][1].setAlliance(alliance) # type: ignore
            except:
                pass

            self.alliance = alliance
            self.needUpdate = True
        if alliance in STIMULATION:
            self.needUpdate = True



    def process(self, im : Image.Image) -> PhotoImage:
        img: Image.Image = im.copy()

        placeOver(img1=img, img2=displayText(text=f"FPS: {self.fps}", size="m"), position=(20,20))
        # placeOver(img, displayText(f"Interacting With: {self.interacting}", "m"), (20,55))
        # placeOver(img, displayText(f"length of IVO: {len(self.ivos)}", "m"), (20,90))
        # placeOver(img, displayText(f"Mouse Pos: ({self.mx}, {self.my})", "m"), (200,20))
        # placeOver(img, displayText(f"Mouse Press: {self.mPressed}", "m", colorTXT=(100,255,100,255) if self.mPressed else (255,100,100,255)), (200,55))

        placeOver(img1=img, img2=displayText(text=f"Selected: {self.selectedBranch}{" " if self.selectedLevel==0 else self.selectedLevel}", size="m"), position=(20,55))
        if not(COMMS):
            placeOver(img1=img, img2=displayText(text=f"Comms has been disabled!", size="m", colorTXT=(255,100,100,255)), position=(20,90))

        connected: bool = self.comms.getIsConnected()
        placeOver(img1=img, img2=displayText(text=f"Comms: Connected: {connected}", size="m", colorTXT=(100,255,100,255) if connected else (255,100,100,255)), position=(20,775))
        if connected:
            placeOver(img1=img, img2=displayText(text="Comms: Alliance: {}".format("Blue" if self.comms.getBlueAlliance() else "Red"), size="m", colorTXT=(100,100,255,255) if self.comms.getBlueAlliance() else (255,100,100,255)), position=(20,800))
            placeOver(img1=img, img2=displayText(text=f"Comms: Nearest: {self.comms.getNearest()}", size="m"), position=(20,825))
        else:
            placeOver(img1=img, img2=displayText(text=f"Comms: Alliance: Disconnected", size="m", colorTXT=(100,100,100,255)), position=(20,800))
            placeOver(img1=img, img2=displayText(text=f"Comms: Nearest: Disconnected", size="m", colorTXT=(100,100,100,255)), position=(20,825))

        if self.alliance in STIMULATION:
            subway: Image.Image = getFrameFromGIF(image=SUBWAY_GIF, frame=int(time.time()*16))
            placeOver(img1=img, img2=subway, position=( 230,  10))
            placeOver(img1=img, img2=subway, position=(1130,  10))
            placeOver(img1=img, img2=subway, position=( 230, 615))
            placeOver(img1=img, img2=subway, position=(1130, 615))
            placeOver(img1=img, img2=subway, position=( 670, 300))

        for id in self.ivos:
            if self.ivos[id][0] == "a":
                if 0 <= id <= 11:
                    try:
                        self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or id=="ABCDEFGHIJKL ".find(self.selectedBranch)) # type: ignore
                    except:
                        pass
                elif 51 <= id <= 54:
                    try:
                        self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or id==self.selectedLevel+50) # type: ignore
                    except:
                        pass
                elif id == -49:
                    try:
                        self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id or self.selectedBranch=="processor") # type: ignore
                    except:
                        pass
                else:
                    try:
                        self.ivos[id][1].tick(img, self.interacting==id, self.interacting==id) # type: ignore
                    except:
                        pass

        return PhotoImage(image=img)

    def saveState(self) -> None:
        pass

    def close(self) -> None:
        pass