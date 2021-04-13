import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import platform

'''
The following widgets have not been Simplified:
    ttk.Scale
    ttk.Spinbox
    ttk.Progressbar
    ttk.Notebook
'''

class SimpleWidget:
    def __init__(self, view, padding_type='both'):
        padding_type = padding_type.strip().lower()
        if padding_type not in ['both', 'none', 'x', 'y']:
            raise ValueError(f'padding type must be one of: both, none, x, y, not: {padding_type}')

        self.view = view
        self.padding_type = padding_type
        self.cursor_enabled = 'hand2'
        self.cursor_disabled = 'x_cursor'

        try: self.clickable
        except: self.clickable = False

        if self.clickable: self.config(cursor=self.cursor_enabled)

    def get_state(self):
        return self['state']

    def enable(self):
        self.config(state='normal')
        if self.clickable: self.config(cursor=self.cursor_enabled)

    def disable(self):
        self.config(state='disabled')
        if self.clickable: self.config(cursor=self.cursor_disabled)

class BlankWidget(tk.Label, SimpleWidget):
    def __init__(self, view):
        super().__init__(view.frame, **view.style.label)
        SimpleWidget.__init__(self, view)


class SimpleMenu(tk.Menu, SimpleWidget):
    '''
    accepts a dictionary of menu labels and commands
    menu labels can be nested to create cascading menus
    ex: {'File': {'New': create_file(), 'Open': open_file()}

    the following keys can be used for special functions:
        'sep' or '---': add a separator (value will be ignored)
        'checkbutton': add a checkbutton (must provide 'label' and 'variable' keys)
            ex: {'checkbutton': {'label': 'mycheckbutton', 'variable': mybooleanvar}}
        'radiobutton': add a radiobutton (must provide dictionary with 'options' (list or dict) and 'variable' keys)
            ex: {'radiobutton': {'options': [myoption1, myoption2], 'variable': mystringvar}}

        to get the value of a checkbutton or radiobutton, call the .get() method on your variable

    to use as a context menu, set view = mywidget, and set context_menu = True
    '''
    def __init__(self, view, command_dict, context_menu=False):
        self.clickable = True
        self.context_menu = context_menu

        if self.context_menu: super().__init__(view)
        else: super().__init__(view.frame)
        SimpleWidget.__init__(self, view)

        self.choices = {}
        index = 0
        for label in command_dict:
            if label == '_index' or label == '_menu': raise ValueError('"_index" and "_menu" are reserved labels')
            command = command_dict[label]

            if label.strip().lower() == 'sep' or label.strip().lower() == '---': self.add_separator()
            elif label.strip().lower() == 'checkbutton':
                if type(command) != dict:
                    raise TypeError('checkbutton value must be a dictionary with "label" and "variable" keys')
                self.add_checkbutton(label=command['label'], variable=command['variable'])

            elif label.strip().lower() == 'radiobutton':
                if type(command) != dict:
                    raise TypeError('radiobutton value must be a dictionary with "choices" and "variable" keys')

                if type(command['choices']) != list and type(command['choices']) != dict:
                    raise TypeError('radiobutton choices must be a list of strings, or a dictionary of {string: value} pairs')
                
                for choice in command['choices']:
                    if type(command['choices']) == dict: value = command['choices'][choice]
                    else: value = choice
                    self.add_radiobutton(label=choice, value=value, variable=command['variable'])

            elif type(command) == dict:
                submenu = self._add_cascade(label, command)
                self.choices[label] = {'_index': index, '_menu': submenu}
                self.choices[label].update(submenu.choices)

            else:
                self.add_command(label=label, command=command)
                self.choices[label] = {'_index': index}
            index += 1

        if context_menu:
            view.bind('<Button-3>', lambda e: self.post(e.x_root, e.y_root))

        else: self.view.root.config(menu=self)

    def _add_cascade(self, label, command_dict):
        cascade_menu = SimpleMenu(self.view, command_dict, context_menu=self.context_menu)
        self.add_cascade(label=label, menu=cascade_menu)
        return cascade_menu

    def _finditem(self, labels):
        '''
        should not be called directly
        finds an item in the menu to perform an action, such as disabling
        returns list of (menu, label) tuples

        provide a label for the menu option
        if the option is nested, provide a dictionary of label keys
        ex: {'File': {'New': 'PDF'}}

        you can only change the state of one label per dictionary, but you may provide a list of labels/dictionaries
        if multiple entries are found in a dictionary, only the first one will be used
        '''
        if type(labels) != list: labels = [labels] # correction for single values

        try:
            menuitems = [] # build a list of (menu, label) tuples
            for label in labels:
                menu = self # set root menu
                while type(label) == dict: # dig deeper until we reach the bottom level of the nest
                    menu = menu.choices[list(label.keys())[0]]['_menu'] # get the nested menu widget and update root menu
                    label = label[list(label.keys())[0]] # go deeper into the tree

                menuitems.append((menu, label))
            return menuitems

        except Exception as e: raise ValueError(f'label not found: {e}')

    def _changeconfig(self, labels, **kwargs):
        # should not be called directly

        menuitems = self._finditem(labels)
        for menuitem in menuitems:
            menu = menuitem[0]
            label = menuitem[1]
            menu.entryconfig(label, **kwargs)

    def enable(self, labels):
        # see _finditem() for labels format
        self._changeconfig(labels, state='normal')

    def disable(self, labels):
        # see _finditem() for labels format
        self._changeconfig(labels, state='disabled')

    def add_accelerator(self, label, keys, literal=False):
        '''
        key should be a string, or a tuple of strings (modifer, key)
        will automatically swap "control" with "command" on macOS, and vice versa on Windows and Linux
        this can be overridden with the "literal" argument
        see _finditem() for labels format
        '''

        if self.context_menu: raise Exception('context menus cannot have accelerators')
        if type(keys) == str: keys = (keys) # correction for single values
        if type(keys) != tuple:
            raise TypeError('keys must be a tuple of strings (modifier1, modifier2, key)')
        
        os_platform = platform.system()
        accelerator = ''
        keybind = '<'
        for key in keys:
            if 'command' in key.lower() or 'cmd' in key.lower():
                key = 'Cmd' # sanitization
                if not literal and (os_platform == 'Windows' or os_platform == 'Linux'):
                    key = 'Ctrl' # swap for Win/Linux standard

            if 'control' in key.lower() or 'ctrl' in key.lower() or 'ctl' in key.lower():
                key = 'Ctrl' # sanitization
                if not literal and os_platform == 'Darwin': # for macOS
                    key = 'Cmd' # swap for macOS standard

            # sanitization
            if key.strip() == 'alt': key = 'Alt'
            if key.strip() == 'tab': key = 'Tab'
            if 'shift' in key.lower() or 'shft' in key.lower(): key = 'Shift'

            accelerator += key + '+'
            if key == 'Ctrl': keybind += 'Control-'
            elif key == 'Cmd': keybind += 'Command-'
            elif key == 'Alt': keybind += 'Alt-'
            elif key == 'Tab': keybind += 'Keypress-Tab'
            elif key == 'Shift': pass # shift behavior modifies case of key
            elif len(key) == 1:
                if 'Shift' not in accelerator: key = key.lower() # lowercase key for default behavior
                else: key = key.upper() # uppercase key to require shift
                keybind += f'Key-{key}'

            else: keybind += f'{key}-' # catch-all

        accelerator = accelerator[:-1]
        keybind += '>'

        self._changeconfig(label, accelerator=accelerator)
        
        # get command to bind
        menuitem = self._finditem(label)[0]
        menu = menuitem[0]
        label = menuitem[1]
        index = menu.choices[label]['_index']
        command = menu.entrycget(index, 'command')

        self.bind_all(keybind, command)

class SimpleLabel(tk.Label, SimpleWidget):
    def __init__(self, view, text, font=None):
        if font == None: font=view.style.font.h3
        
        super().__init__(view.frame, text=text, font=font, **view.style.label)
        SimpleWidget.__init__(self, view)

    def change_text(self, text):
        self.configure(text=text)

    def read(self):
        return self.cget('text')

class SimpleImage(tk.Label, SimpleWidget):
    def __init__(self, view, image_file, size=None):
        with Image.open(image_file) as image:
            if size != None:
                if isinstance(size, (int, float)): size = (size, size) # correction for single values
                elif type(size) != tuple or len(size) != 2:
                    raise TypeError('size must be a tuple of two numbers')

                image = image.resize(size)
            self.image = ImageTk.PhotoImage(image)

        super().__init__(view.frame, image=self.image, **view.style.label)
        SimpleWidget.__init__(self, view)


class SimpleButton(tk.Button, SimpleWidget):
    def __init__(self, view, text, command, font=None):
        if font == None: font=view.style.font.body
        self.clickable = True

        super().__init__(view.frame, text=text, command=command, font=view.style.font.h3, **view.style.button)
        SimpleWidget.__init__(self, view)


class SimpleEntry(tk.Entry, SimpleWidget):
    def __init__(self, view, font=None, censor=False):
        if font == None: font=view.style.font.body
        
        super().__init__(view.frame, font=font, **view.style.entry['normal'])
        SimpleWidget.__init__(self, view)

        if censor: self.config(show='*')

    def disable(self):
        self.config(state='readonly')

    def change_text(self, text):
        current_state = self.get_state()

        self.enable()
        self.delete(0, 'end')
        self.insert(0, text)
        self.configure(state=current_state)

    def read(self):
        return self.get()

    def clear(self):
        self.change_text('')


class SimpleTextbox(tk.Text, SimpleWidget):
    def __init__(self, view, size=(5,2), font=None):
        if type(size) == int: size = (size, size) # correction for single values
        elif type(size) != tuple or len(size) != 2:
            raise TypeError('size must be a tuple of two integers (charcters, rows)')

        if font == None: font=view.style.font.body
        width = size[0]
        height = size[1]

        self.custom_state = 'normal' # used for fudging a readonly state and fixing missing style support

        super().__init__(view.frame, width=width, height=height, font=font, **view.style.textbox['normal'])
        SimpleWidget.__init__(self, view)

    def enable(self):
        self.config(state='normal', **self.view.style.textbox['normal'])
        self.custom_state = 'normal'
        self.unbind('<Key>')

    def disable(self):
        self.config(state='normal', **self.view.style.textbox['readonly'])
        self.custom_state = 'readonly'
        self.bind('<Key>', lambda e: 'break')

    def change_text(self, text):
        current_state = self.get_state()

        self.enable()
        self.delete(1.0, 'end')
        self.insert(1.0, text)
        if current_state == 'readonly': self.disable()

    def read(self):
        return self.get(1.0, 'end')

    def clear(self):
        self.change_text('')

    def get_state(self):
        return self.custom_state


class SimpleCheckbutton(tk.Checkbutton, SimpleWidget):
    def __init__(self, view, text, command=None, font=None, onvalue=True, offvalue=False):
        if font == None: font=view.style.font.body
        self.clickable = True

        self.variable = tk.StringVar()
        self.variable.set(offvalue)

        super().__init__(view.frame, text=text, command=command, variable=self.variable, onvalue=onvalue, offvalue=offvalue, font=view.style.font.h3, **view.style.checkbutton)
        SimpleWidget.__init__(self, view)

    def change_text(self, text):
        self.configure(text=text)

    def read(self):
        return self.variable.get()


class SimpleRadioMenu(tk.Frame, SimpleWidget):
    '''
    accepts a list of values, or a dictionary of label: value pairs
    displays the label, outputs the value
    use .read() to return the value
    '''

    def __init__(self, view, choices, command=None, font=None):
        if type(choices) != list and type(choices) != dict:
            raise TypeError('choices must be a list of strings, or a dictionary of {string: value} pairs')

        if font == None: font=view.style.font.body
        self.variable = tk.StringVar()
        self.clear()

        super().__init__(view.frame, **view.style.frame)
        SimpleWidget.__init__(self, view)

        self.choices = {}
        index = 0
        for choice in choices:
            if choice in self.choices: raise IndexError(f'duplicate widget text found in choices: {choice}')
            if type(choices) == dict: value = choices[choice]
            else: value = choice

            radiobutton = tk.Radiobutton(self, variable=self.variable, text=choice, command=command, value=value, font=font, cursor=self.cursor_enabled, **view.style.radiobutton)
            radiobutton.grid(row=index, column=0, sticky='NSEW')
            self.choices[choice] = radiobutton
            index += 1

    def enable(self, choice=None):
        if choice == None:
            for radiobutton in self.winfo_children():
                radiobutton.config(state='normal', cursor=self.cursor_enabled)

        else:
            try: self.choices[choice].config(state='normal', cursor=self.cursor_enabled)
            except: raise ValueError(f'Radiobutton {choice} not found')

    def disable(self, choice=None):
        if choice == None:
            for radiobutton in self.winfo_children():
                radiobutton.config(state='disabled', cursor=self.cursor_disabled)

        else:
            try: self.choices[choice].config(state='disabled', cursor=self.cursor_disabled)
            except: raise ValueError(f'Radiobutton choice "{choice}" not found')

    def invoke(self, choice):
        for radiobutton in self.winfo_children():
            try: self.choices[choice].invoke()
            except: raise ValueError(f'Radiobutton choice "{choice}" not found')

    def select(self, choice):
        for radiobutton in self.winfo_children():
            try: self.choices[choice].select()
            except: raise ValueError(f'Radiobutton choice "{choice}" not found')

    def read(self):
        return self.variable.get()

    def clear(self):
        self.variable.set(None)


class SimpleListbox(tk.Listbox, SimpleWidget):
    '''
    accepts a list of values, or a dictionary of string: value pairs
    displays the string
    use .read() to return the value
    '''
    def __init__(self, view, choices, allow_multiple=True, font=None):
        if font == None: font=view.style.font.body
        self.clickable = True

        self.update_choices(choices)
        self.variable = tk.StringVar(value=self.choices)

        super().__init__(view.frame, listvariable=self.variable, font=font, **view.style.listbox)
        SimpleWidget.__init__(self, view)

        if allow_multiple: self.configure(selectmode='multiple')

    def update_choices(self, choices):
        if type(choices) != list and type(choices) != dict:
            raise TypeError('choices must be a list of strings, or a dictionary of {string: value} pairs')

        self.choices_dict = None # supports calls for parsing {key: value} pairs instead of simple strings
        self.choices = choices
        if type(choices) == dict:
            self.choices_dict = choices
            self.choices = list(choices.keys()) # converts choices into a list for tk.Listbox

    def select(self, choices, ):
        if type(choices) != list: choices = [choices] # correction for single values

        for choice in choices:
            try: self.select_set(self.choices.index(choice))
            except: raise ValueError(f'Listbox choice "{choice}" not found')

            if len(choices) > 1 and not self.cget('selectmode') == 'multiple':
                print('Warning: cannot select more than one choice, please set selectmode to multiple')
                break

    def read(self):
        selections = self.curselection()
        selected_values = []

        for selection in selections:
            if self.choices_dict != None: selected_values.append(self.choices_dict[self.choices[selection]])
            else: selected_values.append(self.choices[selection])
        
        return selected_values

    def clear(self):
        self.selection_clear(0, 'end')


class SimpleCombobox(ttk.Combobox, SimpleWidget):
    '''
    accepts a list of values, or a dictionary of string: value pairs
    displays the string
    use .read() to return the value
    '''
    def __init__(self, view, choices, postcommand=None, font=None):
        if font == None: font=view.style.font.body
        self.clickable = True

        super().__init__(view.frame, postcommand=postcommand, font=font)
        SimpleWidget.__init__(self, view)

        self.update_choices(choices)
        self.bind('<<ComboboxSelected>>', lambda event: self._clearfocus())

    def _clearfocus(self):
        self.view.frame.focus()

    def enable(self):
        self.configure(state='enable')
        self.view.frame.focus()

    def disable(self):
        self.configure(state='disable')
        self.view.frame.focus()

    def disable_entry(self):
        self.configure(state='readonly')
        self.view.frame.focus()

    def update_choices(self, choices):
        if type(choices) != list and type(choices) != dict:
            raise TypeError('choices must be a list of strings, or a dictionary of {string: value} pairs')

        self.choices_dict = None # supports calls for parsing {key: value} pairs instead of simple strings
        self.choices = choices
        if type(choices) == dict:
            self.choices_dict = choices
            self.choices = list(choices.keys()) # converts choices into a list for ttk.Combobox

        self.configure(values=self.choices)

    def clear(self):
        self.set('')

    def read(self):
        if self.choices_dict != None: return self.choices_dict[self.variable.get()]
        else: return self.variable.get()


class SimpleSeparator(ttk.Separator, SimpleWidget):
    def __init__(self, view, orient):
        if 'horiz' in orient.lower(): orient = 'horizontal'
        elif 'vert' in orient.lower(): orient = 'vertical'
        else: raise ValueError(f'orient must ve either horizontal or vertical, not {orient}')

        if orient == 'horizontal': padding_type = 'y'
        if orient == 'vertical': padding_type = 'x'

        super().__init__(view.frame, orient=orient)
        SimpleWidget.__init__(self, view, padding_type=padding_type)