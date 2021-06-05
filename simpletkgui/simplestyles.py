import tkinter as tk
import tkinter.font as tkFont

class Font:
    def __init__(self, family, h1_size=26, h2_size=22, h3_size=14, body_size=12):
        self.family = family
        self.h1 = tkFont.Font(family=family, size=h1_size, weight='bold')
        self.h2 = tkFont.Font(family=family, size=h2_size, weight='bold')
        self.h3 = tkFont.Font(family=family, size=h3_size, weight='bold')
        self.body = tkFont.Font(family=family, size=body_size, weight='normal')
        self.custom = {}

    def create_custom(self, name, family=None, size=None, weight='normal', slant='roman', underline=0, overstrike=0):
        if family == None: family = self.family
        if size == None: size = self.body

        self.custom[name] = tkFont.Font(family=family, size=size, weight=weight, slant=slant, underline=underline, overstrike=overstrike)
        return self.custom[name]

    def get_custom(self, name):
        return self.custom[name]


class ColorPalette:
    def __init__(self, primary='#1D2025', secondary='#2E3640', accent='#607371', accent_alt='#4C5359', text='#DDE5E5', textcursor='white'):
        self.primary = primary
        self.secondary = secondary
        self.accent = accent
        self.accent_alt = accent_alt
        self.text = text
        self.textcursor = textcursor
        self.custom = {}

    def create_custom(self, name, color):
        self.custom[name] = color
        return self.custom[name]

    def get_custom(self, name):
        return self.custom[name]


class Style:
    def __init__(self, font, color, padding):
        if not isinstance(font, Font):
            raise TypeError(f'font must be a Font class, not {type(font)}')

        if not isinstance(color, ColorPalette):
            raise TypeError(f'font must be a ColorPalette class, not {type(color)}')

        if type(padding) != tuple or len(padding) != 2:
            raise TypeError(f'padding must be a tuple of length 2')

        self.font = font
        self.color = color
        self.padding = {'padx': padding[0], 'pady': padding[1]}
        self.custom = {}

        self.frame = {'bg': self.color.primary}
        self.label = {'bg': self.color.primary, 'activebackground': self.color.accent_alt, 'fg': self.color.text}
        self.button = {'bg': self.color.accent, 'activebackground': self.color.accent_alt, 'fg': self.color.text, 'activeforeground':  self.color.text, 'disabledforeground': self.color.accent_alt}
        self.checkbutton = {'bg': self.color.primary, 'activebackground':  self.color.primary, 'selectcolor': self.color.accent, 'fg': self.color.text, 'activeforeground':  self.color.text}
        self.radiobutton = {'bg': self.color.primary, 'activebackground':  self.color.primary, 'selectcolor': self.color.accent, 'fg': self.color.text, 'activeforeground':  self.color.text}
        self.listbox = {'bg': self.color.secondary, 'selectbackground': self.color.accent, 'fg': self.color.text, 'activestyle': 'none'}
        self.entry = {
            'normal': {'bg': self.color.secondary, 'readonlybackground': self.color.accent, 'disabledbackground': self.color.secondary, 'fg': self.color.text, 'disabledforeground': self.color.accent_alt, 'insertbackground': self.color.textcursor},
            'warning': {'bg': 'yellow2', 'fg': 'black', 'insertbackground': 'black'},
            'error': {'bg': 'firebrick1', 'fg': 'black', 'insertbackground': 'black'}
        }
        self.textbox = {
            # textbox does not support disabled styles, so SimpleTextbox fudges it using config commands
            'normal': {'bg': self.color.primary, 'fg': self.color.text, 'insertbackground': self.color.textcursor},
            'readonly': {'bg': self.color.accent},
            'disabled': {'bg': self.color.secondary}
        }

        self.style_types = [self.frame, self.label, self.button, self.checkbutton, self.radiobutton, self.listbox, self.entry['normal'], self.textbox]

    def create_custom(self, name, properties):
        if not type(properties) == dict:
            raise TypeError(f'Properties must be of type {dict}, not {type(properties)}')

        self.custom[name] = properties
        return self.custom[name]

    def get_custom(self, name):
        return self.custom[name]