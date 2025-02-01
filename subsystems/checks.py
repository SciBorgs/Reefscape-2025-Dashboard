"""This file makes sure that everything the program needs is set and ready to run!"""

"""Test import all major modules"""
from PIL import Image, ImageTk, ImageDraw  # type: ignore
import tkinter as tk  # type: ignore
import os, numpy, time, math  # type: ignore

from settings import *

if COMMS:
    import robotpy  # type: ignore

"""Test import all subsystems"""
from subsystems.lib.counter import *
from subsystems.lib.fancy import *
from subsystems.lib.label import *
from subsystems.lib.render import *
from subsystems.lib.simplefancy import *
from subsystems.lib.visuals import *
from subsystems.comms import *
from subsystems.interface import *
from subsystems.window import *
from settings import *


class Check:
    @staticmethod
    def check() -> None:
        print("Finished Checks")

    @staticmethod
    def error(message: str) -> None:
        print(f"The check has detected an issue: {message}")
