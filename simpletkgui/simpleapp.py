# !/usr/bin/env python
__author__ = 'Michael Genson'

from simpletkgui import simpleconfig
from simpletkgui import simpleicons
from simpletkgui import simplestyles

import tkinter as tk

class App(tk.Tk):
    def __init__(self, appname, font={'family': 'Arial'}, color={}, padding=(8, 12), resize=True, minsize=(200, 100), appconfig='to be generated', icon_data=simpleicons.generic(), start_hidden=False):
        if type(minsize) != tuple:
            raise TypeError(f'Minimum size must be of type {tuple}, not {type(minsize)}')

        if appconfig == 'to be generated': appconfig = simpleconfig.SimpleConfig(appname)
        self.appconfig = appconfig

        super().__init__()
        if start_hidden: self.hide()

        self.option_add('*tearOff', False)

        self.appname = appname
        self.style = simplestyles.Style(simplestyles.Font(**font), simplestyles.ColorPalette(**color), padding)
        self.title(f'{appname}')
        self.configure(**self.style.frame)

        if resize: self.minsize(minsize[0], minsize[1])
        else:
            self.resizable(width=False, height=False)
            self.geometry(f'{minsize[0]}x{minsize[1]}')

        self.icon = None
        if icon_data != None:
            self.icon = tk.PhotoImage(data=icon_data)
            self.tk.call('wm', 'iconphoto', self._w, self.icon)

        self.active_view = None
        self.active_windows = []

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()

    def start(self):
        self.show()
        self.mainloop()

    def change_view(self, new_view):
        if self.active_view != None: self.active_view.pack_forget()
        self.active_view = new_view
        self.active_view.pack()


class SimpleWindow(tk.Toplevel, App):
    def __init__(self, parent, windowname=None, style=None, resize=True, minsize=(200, 100), icon_data=None, start_hidden=False):
        if type(minsize) != tuple:
            raise TypeError(f'Minimum size must be of type {tuple}, not {type(minsize)}')

        if windowname == None: windowname=parent.appname
        if style == None: style=parent.style

        self.parent = parent
        self.style = style

        super().__init__(parent)
        if start_hidden: self.hide()

        self.title(windowname)
        self.configure(**style.frame)

        if resize: self.minsize(minsize[0], minsize[1])
        else:
            self.resizable(width=False, height=False)
            self.geometry(f'{minsize[0]}x{minsize[1]}')

        self.icon = None
        if icon_data != None:
            self.icon = tk.PhotoImage(data=icon_data)
            self.tk.call('wm', 'iconphoto', self._w, self.icon)

        elif parent.icon != None: self.tk.call('wm', 'iconphoto', self._w, parent.icon)

if __name__ == '__main__':
    app = App('title')
    window = SimpleWindow(app)
    app.start()