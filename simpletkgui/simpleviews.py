from simpletkgui import simplewidgets
import os
import tkinter as tk
import re

class Nav:
    def __init__(self, root, return_view_text=None, return_view=None, page_list=None, page_func=None, page_index=0, title='', button_1_text='', button_1_func=None, button_2_text='', button_2_func=None):
        # Creates a nav menu with simple buttons 1 and 2.
        # If you include a page_func to be run upon switching pages, you must include "list_value" in your lambda
            # ex: lambda list_value: print(list_value)

        if return_view != None and not isinstance(return_view, View):
            raise TypeError(f'return_view must be a View class, not {type(return_view)}')

        if page_list != None and type(page_list) != list:
            raise TypeError(f'page_list must be of type {list}, not {type(page_list)}')

        self.root = root
        self.style = root.style
        self.page_list = page_list
        self.page_func = page_func
        self.page_index = page_index
        self.title_base = title.strip()

        self.frame = tk.Frame(self.root, **self.style.frame)
        self.visible = False
        
        # return view
        return_view_frame = tk.Frame(self.frame, **self.style.frame)
        return_view_frame.grid(row=0, column=0, sticky='NSW')
        if return_view != None:
            return_view_button = tk.Button(return_view_frame, text=return_view_text, command=lambda: self.root.change_view(return_view), font=self.style.font.h3, cursor='hand2', **self.style.button)
            return_view_button.pack(side='left')

        # page nav buttons
        page_frame = tk.Frame(self.frame, **self.style.frame)
        page_frame.grid(row=0, column=2, sticky='NSW')
        if page_list != None:

            def go_prev():
                self.page_index -= 1
                self.reset()

            def go_next():
                self.page_index += 1
                self.reset()

            self.prev = tk.Button(page_frame, text='⮜', command=go_prev, font=self.style.font.h3, cursor='hand2', **self.style.button)
            self.next = tk.Button(page_frame, text='⮞', command=go_next, font=self.style.font.h3, cursor='hand2', **self.style.button)
            for x in range(0,2):
                page_frame.columnconfigure(x, weight=1, uniform='uniform')

        # title
        self.title = tk.Label(self.frame, text=self.title_base, font=self.style.font.h2, **self.style.label)
        self.title.grid(row=0, column=2, columnspan=3, sticky='NSEW')

        # extra buttons
        button_frame = tk.Frame(self.frame, **self.style.frame)
        button_frame.grid(row=0, column=5, columnspan=2, sticky='NSE')
        if button_1_func != None or button_2_func != None:
            if button_1_func != None:
                button_1 = tk.Button(button_frame, text=button_1_text, command=button_1_func, font=self.style.font.h3, cursor='hand2', **self.style.button)
                button_1.grid(row=0, column=0, sticky='E', padx=(self.style.padding['padx'], 0))

            if button_2_func != None:            
                button_2 = tk.Button(button_frame, text=button_2_text, command=button_2_func, font=self.style.font.h3, cursor='hand2', **self.style.button)
                button_2.grid(row=0, column=1, sticky='E', padx=(self.style.padding['padx'], 0))

            for x in range(0,2):
                button_frame.columnconfigure(x, weight=1, uniform='uniform')

        # weight nav grid
        for x in range(0, 7):
            self.frame.columnconfigure(x, weight=1, uniform='uniform')

    def reset(self):
        # hide nav buttons at either end of the list
        if self.page_list != None:
            title_text = f'{self.title_base} {self.page_index+1} of {len(self.page_list)}'.strip()

            if self.page_index > 0:
                self.prev.grid(row=0, column=0, sticky='NS')
            else: self.prev.grid_forget()

            if self.page_index < len(self.page_list)-1:
                self.next.grid(row=0, column=1, sticky='NS')
            else: self.next.grid_forget()

            # update title if displaying current page
            self.title.configure(text=title_text)

        # run page_func if defined
        if self.page_func != None: self.page_func(list_value=self.page_list[self.page_index])

    def pack(self):
        if not self.visible:
            self.frame.pack(fill='x', **self.style.padding)
            self.visible = True
            self.reset()

    def pack_forget(self):
        if self.visible:
            self.frame.pack_forget()
            self.visible = False


class View:
    def __init__(self, root, nav=None, scrollable=False, scroll_height=200, padding_type=None, hierarchy='primary'):
        '''
        base view class - holds basic functions for interacting with SimpleWidgets
        use frame for adding widgets
        set hierarchy to 'secondary' to change some default options for non-primary windows
        use geometric_frame to pack, grid, and place
            the purpose of this distinction is to accommodate the ScrolledFrame
        '''

        if nav != None and not isinstance(nav, Nav):
            raise TypeError(f'nav must be a Nav class, not {type(nav)}')

        if scrollable and type(scroll_height) != int:
            raise TypeError('scroll_height must be an integer')

        self.padding_type = padding_type
        if isinstance(root, View): self.root = root.frame # enables nested views
        else: self.root = root

        self.nav = nav
        self.style = root.style.copy()

        if hierarchy == 'primary':
            if padding_type == None: self.padding_type = 'none' # removes padding from main frame

        if hierarchy == 'secondary':
            if padding_type == None: self.padding_type = 'both' # adds padding for secondary frames
            for style in self.style.style_types: style['bg'] = self.style.color.primary = self.style.color.secondary # changes background for widgets in a secondary frame
        
        if scrollable:
            self.geometric_frame = ScrolledFrame(self.root, scroll_height, **self.style.frame)
            self.frame = self.geometric_frame.interior

        else:
            self.frame = tk.Frame(self.root, **self.style.frame)
            self.geometric_frame = self.frame

        self.visible = False

    def pack(self):
        if not self.visible:
            if self.nav != None:  self.nav.pack()

            if self.padding_type == 'both': padding = self.style.padding
            elif self.padding_type == 'x': padding = {'padx': self.style.padding['padx']}
            elif self.padding_type == 'y': padding = {'pady': self.style.padding['pady']} 
            else: padding = {}

            self.geometric_frame.pack(fill='both', expand=True, **padding)
            self.visible = True

    def pack_forget(self):
        if self.visible:
            if self.nav != None:  self.nav.pack_forget()
            self.geometric_frame.pack_forget()
            self.visible = False

    def grid(self, **kwargs):
        self.geometric_frame.grid(**kwargs)

    def grid_forget(self, **kwargs):
        self.geometric_frame.grid_forget(**kwargs)


class SimpleView(View):
    def build_grid(self, widget_dict, even_rows=False):
        # creates a grid of widgets evenly spread along the view
        # optional toggle for weighting rows
        # each key should be formatted 'row1', 'row2', etc. with a corresponding list of widgets
        # each cell will be evenly spaced
            # use None for blank cells
            # use 'ext' to increase length

        # sample: {'row0': [label0, button0, button1], 'row1': [label1, button2, button3]}

        if type(widget_dict) != dict:
            raise TypeError(f'widget_dictionary must be of type {dict}, not {type(widget_dict)}')

        for key, value in widget_dict.items():
            if not re.search(r'row\d+', key):
                raise ValueError(f'invalid key in widget_dict: {key}')

        class WidgetToGrid:
            def __init__(self, column, row, widget):
                self.column = column
                self.row = row
                self.widget = widget
                self.span = 1

        # track number of columns and rows
        row_set = {0}
        column_set = {0}

        widgets_to_grid = []
        for row, widget_list in widget_dict.items():
            if type(widget_list) != list: widget_list = [widget_list] # correction for single widget
            if widget_list == []: widget_list = [None] # correction for empty lists

            current_row = int(row[3:])
            current_column = 0
            row_set.add(current_row)

            for widget in widget_list:
                if widget == None: widget = simplewidgets.BlankWidget(self)
                if widget == 'ext': widgets_to_grid[-1].span += 1
                else: widgets_to_grid.append(WidgetToGrid(row=current_row, column=current_column, widget=widget))
                column_set.add(current_column)
                current_column += 1

        for widget_to_grid in widgets_to_grid:
            if widget_to_grid.widget.padding_type == 'both': padding = self.style.padding
            elif widget_to_grid.widget.padding_type == 'x': padding = {'padx': self.style.padding['padx']}
            elif widget_to_grid.widget.padding_type == 'y': padding = {'pady': self.style.padding['pady']} 
            else: padding = {}

            widget_to_grid.widget.grid(row=widget_to_grid.row, column=widget_to_grid.column, columnspan=widget_to_grid.span, sticky='NSEW', **padding)

        number_of_rows = max(row_set)+1
        number_of_columns = max(column_set)+1

        for x in range(0, number_of_rows):
            self.frame.grid_rowconfigure(x, weight=1)
            if even_rows: self.frame.grid_rowconfigure(x, uniform='uniform')

        for x in range(0, number_of_columns):
            self.frame.grid_columnconfigure(x, weight=1, uniform='uniform')


class GridView(View):
    # creates a grid of widgets of various sizes
    # add widgets to the grid via add_widget
    # create the grid using build_grid

    class Cell:
            def __init__(self, widget, column, row, width, height):
                self.widget = widget
                self.column = column
                self.row = row
                self.width = width
                self.height = height

    def __init__(self, root, nav=None, scrollable=False, scroll_height=200, padding_type=None, hierarchy='primary'):
        super().__init__(root, nav=nav, scrollable=scrollable, padding_type=padding_type, hierarchy=hierarchy)
        self.cells = {}

    def check_location(self, location):
        if type(location) != tuple or len(location) != 2 or location[0] < 0 or location[1] < 0:
            raise TypeError(f'location must be a tuple of two integers greater than or equal to zero')

    def check_size(self, size):
        if type(size) != tuple or len(size) != 2 or size[0] < 1 or size[1] < 1:
            raise TypeError(f'size must be a tuple of two integerss greater than zero')

    def add_widget(self, location, size, widget):
        self.check_location(location)
        self.check_size(size)

        column = location[0]
        row = location[1]
        width = size[0]
        height = size[1]

        # check if a widget already exists at that location
        if column in self.cells.setdefault(row, {}):
            raise IndexError(f'cannot place widget at {location}: that cell is taken')

        # add widget to widget dict
        widget = self.Cell(widget, row=row, column=column, width=width, height=height)
        self.cells[row][column] = widget

    def add_widgets(self, widget_tuples):
        # add widgets in bulk by providing a list of tuples: (location, size, widget)
        if type(widget_tuples) != list:
            raise TypeError(f'must provide type {list}, not {type(widget_tuples)}')

        for widget_tuple in widget_tuples:
            if type(widget_tuple) != tuple or len(widget_tuple) != 3:
                raise TypeError(f'must provide a list of tuples of size 3')

            self.add_widget(*widget_tuple)

    def remove_widget(self, location, location_2=None):
        if location_2 != None: # correction for if tuple is provided as arguments
            location = (location, location_2)

        self.check_location(location)

        row = location[0]
        column = location[1]

        if column in self.cells.setdefault(row, {}):
            del self.cells[row][column]

        else: raise IndexError(f'cannot find widget at {location}')

    def build_grid(self, even_rows=False):
        self.pack_forget()

        # track number of rows and columns
        row_set = {0}
        column_set = {0}
        widget_list = [] # track active widgets to reuse

        for row, columns in self.cells.items():
            for column, cell in columns.items():
                row_set.add(row+cell.height-1)
                column_set.add(column+cell.width-1)
                widget_list.append(cell.widget)

                sticky = 'NSEW'
                if isinstance(cell.widget, simplewidgets.SimpleSeparator):
                    if cell.widget.cget('orient') == 'horizontal': sticky='EW'
                    else: sticky='NS'

                cell.widget.grid(row=row, column=column, rowspan=cell.height, columnspan=cell.width, sticky=sticky, **self.style.padding)

        number_of_rows = max(row_set)+1
        number_of_columns = max(column_set)+1

        for x in range(0, number_of_rows):
            self.frame.grid_rowconfigure(x, weight=1)
            if even_rows: self.frame.grid_rowconfigure(x, uniform='uniform')

        for x in range(0, number_of_columns):
            self.frame.grid_columnconfigure(x, weight=1, uniform='uniform')


class ScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    * Modified version of solution from:
        https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    """
    def __init__(self, root, height, **kwargs):
        tk.Frame.__init__(self, root, borderwidth=2, relief='sunken', **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tk.Scrollbar(self, orient='vertical', cursor='hand2')
        self.vscrollbar.pack(fill='y', side='right', expand=False)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.vscrollbar.set, height=height, **kwargs)
        canvas.pack(side='left', fill='both', expand=True)
        self.vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(canvas, **kwargs)
        interior_id = canvas.create_window(0, 0, window=self.interior, anchor='nw')
        def _bound_to_mousewheel(event):
            canvas.bind_all('<MouseWheel>', _on_mousewheel)   

        def _unbound_to_mousewheel(event):
            canvas.unbind_all('<MouseWheel>') 

        def _on_mousewheel(event):
            if not (self.vscrollbar.get()[0] == 0 and self.vscrollbar.get()[1] == 1):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        self.interior.bind('<Enter>', _bound_to_mousewheel)
        self.interior.bind('<Leave>', _unbound_to_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            canvas.config(scrollregion='0 0 %s %s' % size)
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)