"""This file contains a wrapper for tkinter labels!"""

import tkinter as tk
from PIL import ImageTk
from settings import *
from subsystems.lib.render import *
from typing import Tuple


class LabelWrapper:
    """A wrapper for tkinter labels"""

    def __init__(
        self,
        root: tk.Tk,
        size: Tuple[int, int],
        offset: Tuple[float, float] = (0, 0),
        place: Tuple[int, int] = (0, 0),
        bg: str = "#ffffff",
    ) -> None:
        self.offset: Tuple[float, float] = offset
        self.size: Tuple[int, int] = size
        self.section: tk.Label = tk.Label(master=root, width=size[0], height=size[1], bg=bg, highlightthickness=0, bd=0, image=ImageTk.PhotoImage(image=TEST_IMAGE))  # type: ignore
        self.section.pack()
        self.position: Tuple[int, int] = place
        self.shown: bool = True
        self.section.place(x=place[0], y=place[1])

    def update(self, img: tk.PhotoImage) -> None:
        """Updates the label's image to the given array"""
        self.section.configure(image=img)

    def hide(self) -> None:
        """Hides the label by moving it far off screen"""
        self.section.place(x=5000, y=0)
        self.shown = False

    def show(self) -> None:
        """Shows the label by placing it back to its proper position"""
        self.section.place(x=self.position[0], y=self.position[1])
        self.shown = True
