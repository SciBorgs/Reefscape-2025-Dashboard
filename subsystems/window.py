'''This file is just the window that pops up and refreshes itself!'''

from PIL.Image import Image
from settings import *
import tkinter as tk
import time
from subsystems.interface import Interface
from subsystems.lib.label import LabelWrapper
from settings import *

class Window:
    def __init__(self) -> None:
        '''initalize tk window'''
        self.window = tk.Tk()
        self.window.title(string="Reefscape 2025 - Dashboard")
        self.window.geometry(newGeometry="1500x865")
        # self.window.wm_attributes('-alpha', 0.5)
        # self.window.minsize(500,500)
        # self.window.maxsize(500,500)
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsTimestamps: list[float] = []
        self.mPressed = False

        '''load test image'''
        self.label = LabelWrapper(root=self.window, size=SECTION_DATA[2], offset=SECTION_DATA[0], place=SECTION_DATA[0], bg=BACKGROUND_COLOR)
        self.blankConnected: Image = CONNECTED_ALLIANCE_BACKGROUND.copy()
        self.blankDisconnected: Image = DISCONNECTED_ALLIANCE_BACKGROUND.copy()

        '''start interface'''
        self.interface = Interface()
        self.window.grid() # type: ignore

    def windowProcesses(self) -> None:
        '''window processes'''
        mx: int = self.window.winfo_pointerx()-self.window.winfo_rootx()
        my: int = self.window.winfo_pointery()-self.window.winfo_rooty()
        if self.mPressed > 0: 
            self.mPressed += 1
        else: 
            self.mPressed = 0

        '''update screens'''
        self.interface.tick(mx=mx,my=my,mPressed=self.mPressed, fps=self.fps)
        self.mouseScroll = 0

        if self.interface.needUpdate and INTERFACE_FPS < self.fps:
            self.label.update(img=self.interface.process(im=self.blankConnected if self.interface.comms.getIsConnected() else self.blankDisconnected)) 
            self.interface.needUpdate = False

        now: float = time.time()
        self.fpsTimestamps.append(now)
        while now-self.fpsTimestamps[0] > FPS_DAMPENING:
            self.fpsTimestamps.pop(0)
        self.fps: float = round(number=len(self.fpsTimestamps)/FPS_DAMPENING)

        self.window.after(ms=TICK_MS, func=self.windowProcesses)

    def windowOccasionalProcesses(self) -> None:
        '''window processes that happen less frequently (once every 5 seconds)'''
        print("windowOccaionalProcess")
        print(self.getFPS())

        if self.label.shown:
            self.label.update(img=self.interface.process(im=self.blankConnected if self.interface.comms.getIsConnected() else self.blankDisconnected))

        self.window.after(ms=OCCASIONAL_TICK_MS, func=self.windowOccasionalProcesses)

    def windowStartupProcesses(self) -> None:
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self) -> float: return self.fps
    def mPress(self) -> None: self.mPressed = 1
    def mRelease(self) -> None: self.mPressed = -999

    def start(self) -> None:
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind(sequence="<ButtonPress>", func=lambda event: self.mPress())
        self.window.bind(sequence="<ButtonRelease>", func=lambda event: self.mRelease())

        self.window.after(ms=2, func=self.windowProcesses)
        self.window.after(ms=2, func=self.windowOccasionalProcesses)
        self.window.after(ms=1, func=self.windowStartupProcesses)
        self.window.mainloop()