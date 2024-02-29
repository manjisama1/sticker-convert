#!/usr/bin/env python3
import platform
from typing import TYPE_CHECKING

from ttkbootstrap import Toplevel  # type: ignore

if TYPE_CHECKING:
    from sticker_convert.gui import GUI  # type: ignore

from sticker_convert.gui_components.gui_utils import GUIUtils


class BaseWindow(Toplevel):
    def __init__(self, gui: "GUI"):
        super(BaseWindow, self).__init__(alpha=0)  # type: ignore
        self.gui = gui

        GUIUtils.set_icon(self)

        self.mousewheel: tuple[str, ...]
        if platform.system() == "Windows":
            self.mousewheel = ("<MouseWheel>",)
            self.delta_divide = 120
        elif platform.system() == "Darwin":
            self.mousewheel = ("<MouseWheel>",)
            self.delta_divide = 1
        else:
            self.mousewheel = ("<Button-4>", "<Button-5>")
            self.delta_divide = 120

        (
            self.main_frame,
            self.horizontal_scrollbar_frame,
            self.canvas,
            self.x_scrollbar,
            self.y_scrollbar,
            self.scrollable_frame,
        ) = GUIUtils.create_scrollable_frame(self)
