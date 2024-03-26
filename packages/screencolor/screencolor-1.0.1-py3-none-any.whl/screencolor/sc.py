import os
import time
from colorthief import ColorThief
from mss import mss
from datetime import datetime


class ScreenColorInitException(Exception):
    pass


class ScreenColorTakeSSException(Exception):
    pass


class ScreenColorPickColorException(Exception):
    pass


class ScreenColor:
    def __init__(self, default_color = 0xFFFFFFF, monitor_id: int = -1, buffer_folder: str = os.getcwd() + '\\buffer\\', quality: int = 1, delete_after: bool = True):
        """
        ScreenColor class.

        Params:
            monitor_id: int (optional) Defaults to -1 (all monitors)
            buffer_folder: str (optional) Defaults to /buffer/
            delete_after: bool (optional) Defaults to True
        """
        try:
            self.buffer_folder = buffer_folder
            self.quality = quality
            try: os.mkdir(self.buffer_folder)
            except FileExistsError: pass
            self.color_hex = default_color
            self.color_rgb = None
            self.api_thread = None
            self.buffer = []
            self.mss = mss()
            self.monitor_id = monitor_id
            self.active_path = None
            self.delete_after = delete_after
        except Exception as exc: raise ScreenColorInitException(exc)

    def take_ss(self):
        try:
            self.active_path = self.mss.shot(mon=self.monitor_id, output=self.buffer_folder + datetime.now().strftime('%d-%m-%Y-%H-%M-%S') + '.png')
            return self.active_path
        except Exception as exc: raise ScreenColorTakeSSException(exc)

    def get_color(self, delete_after: bool = True, rgb: bool = False):
        try:
            self.color_rgb = ColorThief(self.active_path).get_color(quality=self.quality)
            self.color_hex = '#{:02x}{:02x}{:02x}'.format(self.color_rgb[0], self.color_rgb[1], self.color_rgb[2])
            if delete_after: os.remove(self.active_path)
            return self.color_rgb if rgb else self.color_hex
        except Exception as exc: raise ScreenColorPickColorException(exc)

    def get(self, rgb: bool = False):
        """
        Get current color.

        :param rgb:
        :return:
        """
        self.take_ss()
        return self.get_color(delete_after=self.delete_after, rgb=rgb)

    def start_loop(self, delay_seconds: int = 1):
        """
        Start loop. You may want to call it with threading or multithreading.

        :param delay_seconds:
        :return:
        """
        while True:
            self.get()
            time.sleep(delay_seconds)
