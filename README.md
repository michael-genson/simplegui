# SimpleTkGUI

### What is SimpleTkGUI?
For one reason or another, you've decided your scripts need a GUI. Maybe it's a small project for you and your friends, or maybe you're distributing your code to users who don't know how to open command line. Whatever the reason, you want to wrap your code in an interface for non-technical use (or maybe you just like GUIs). If you're like me, you want to write your code, then deploy it as easily as possible, while also being user-friendly.

SimpleTkGUI is a wrapper for the native python module tkinter. It aims to simplify many of the decisions and complexities in building a tkinter UI, making broad assumptions that will fit 80% of use-cases, while allowing for proper customization as needed.

SimpleTkGUI is a pet project of mine that has evolved from spaghetti UI code I never want to look at again. Hopefully you find it as a way to spend less time on the presentation, and more time on the functionality.

### Installation
Currently the only way to use SimpleTkGUI is to get it from git.

### Usage
```
from simpletkgui import *
```

The core functionality of SimpleTkGUI lies mostly in the simpleviews and simplewidgets modules. The remaining modules are mainly just helper functions and objects.
Start with a SimpleApp object and give it a name. You may also want to start it hidden while you get everything else ready.

```
myapp = simpleapp.App('My First App', start_hidden=True)
```

Next, let's build a nav and a view. The View class is basically a wrapper for tk.Frame - all simple widgets are built to be placed in views. Views take care of most of the geometry and style management for you by choosing common defaults that work for most GUIs.

The Nav class is a flexible navigation bar at the top of your view. Navs range from simple titles to complex page management tools. Check out the Nav class source if you want to learn more!
For this example, we will create a nav with a title.

Note that navs are optional. You don't need a nav to create a view.

```
mynav = simpleviews.Nav(myapp, title='My First SimpleTkGUI View')
myview = simpleviews.SimpleView(myapp, nav=mynav)
```

Generally we won't call the View class directly. We'll use a special type of view, such as a SimpleView. If you'd prefer to build your own views instead of using the ones in the simpleviews module, use the View object as a base, and modify it as you would a standard tk.Frame object (you will want to pass Frame arguments to myview.frame, instead of myview directly).

To see what we've done so far, switch to your view and call the .start() function on your app. If your app is hidden, this will also unhide it.

```
myapp.change_view(myview)
myapp.start()
```

Now we'll want to create some widgets and add them to our view. Like the View class, the SimpleWidget class is a wrapper for the tk widget classes. Unlike views, if you want to change any tkinter properites of these widgets, you can pass those arguments <ins>directly</ins>. SimpleWidgets are children of their tkinter

Let's create a label and a button. SimpleWidgets take a <ins>view</ins> as an argument, not a frame.

```
mylabel = simplewidgets.SimpleLabel(myview, 'This is a SimpleLabel')
mybutton = simplewidgets.SimpleButton(myview, 'This is a SimpleButton', lambda: print('SimpleButton has been pushed!'))
```

Now we'll need to place these in our view. The SimpleView we created earlier accepts a dictionary of rows in its 'build_grid' function. The dictionary key should designate a row, and the value should be your widget:

```
myview.build_grid({
        'row1': mylabel,
        'row2': mybutton,
        })
```

If you want to provide more than one widget per row, pass it in a list and they will be added from left to right. If you want a widget to take up multiple columns, pass the string 'ext' as the widget value.
Here's our code so far:

```
from simpletkgui import *

myapp = App('My First App', start_hidden=True)
mynav = simpleviews.Nav(myapp, title='My First SimpleTkGUI View')
myview = simpleviews.SimpleView(myapp, nav=mynav)

mylabel = simplewidgets.SimpleLabel(myview, 'This is a SimpleLabel')
mybutton = simplewidgets.SimpleButton(myview, 'This is a SimpleButton', lambda: print('SimpleButton has been pushed!'))
myview.build_grid({
        'row1': mylabel,
        'row2': mybutton,
        })

myapp.change_view(myview)
myapp.start()
```

Another view type we have is the GridView. GridView gives us more control over our geometry manager, while still taking care of some of the more monotonous parts.
Let's create a new set of widgets, put them in a GridView object, and link our new view to our old view via our "mybutton" widget on our first menu.

First: create a new view and add a bunch of widgets to it. Let's also give it a nav with a main menu button that returns to our original view.

```
mygridnav = simpleviews.Nav(myapp, title='My First GridView', return_view_text='Main Menu', return_view=myview)
mygridview = simpleviews.GridView(myapp, mygridnav)

mygridlabel = simplewidgets.SimpleLabel(mygridview, 'Here are all of my buttons:')
button1 = simplewidgets.SimpleButton(mygridview, 'Button 1', lambda: print('Button 1 has been pushed!'))
button2 = simplewidgets.SimpleButton(mygridview, 'Button 2', lambda: print('Button 2 has been pushed!'))
button3 = simplewidgets.SimpleButton(mygridview, 'Button 3', lambda: print('Button 3 has been pushed!'))
mycheckbutton = simplewidgets.SimpleCheckbutton(mygridview, 'I approve of these buttons', lambda: print(f'User approval status: {mycheckbutton.read()}'))
```

Now, let's place these in a grid. The grid takes a list of tuples of size 3, which describe its placement within the grid and size. Here's an example of one tuple:

```
((x, y), (width, height), widget)
```

The x and y coordinates are the row and column of the top-left corner of the widget. Let's place our widgets:

```
mygridview.add_widgets([
        ((0, 0), (3, 1), mygridlabel),
        ((0, 1), (1, 1), button1),
        ((1, 1), (1, 1), button2),
        ((2, 1), (1, 1), button3),
        ((0, 2), (3, 3), mycheckbutton)
        ])
mygridview.build_grid()
```

Unlike SimpleView, you must explicitly build your grid. This is because you may want to add more widgets before the geometry manager figures out where to put them.
Finally, let's modify our first SimpleView to bring us to our new GridView:

```
mybutton = simplewidgets.SimpleButton(myview, 'Go To GridView', lambda: myapp.change_view(mygridview))
```

Here is the full code:

```
from simpletkgui import *

myapp = App('My First App', start_hidden=True)
mynav = simpleviews.Nav(myapp, title='My First SimpleTkGUI View')
myview = simpleviews.SimpleView(myapp, nav=mynav)

mylabel = simplewidgets.SimpleLabel(myview, 'This is a SimpleLabel')
mybutton = simplewidgets.SimpleButton(myview, 'Go To GridView', lambda: myapp.change_view(mygridview))
myview.build_grid({
        'row1': mylabel,
        'row2': mybutton,
    })

mygridnav = simpleviews.Nav(myapp, title='My First GridView', return_view_text='Main Menu', return_view=myview)
mygridview = simpleviews.GridView(myapp, mygridnav)

mygridlabel = simplewidgets.SimpleLabel(mygridview, 'Here are all of my buttons:')
button1 = simplewidgets.SimpleButton(mygridview, 'Button 1', lambda: print('Button 1 has been pushed!'))
button2 = simplewidgets.SimpleButton(mygridview, 'Button 2', lambda: print('Button 2 has been pushed!'))
button3 = simplewidgets.SimpleButton(mygridview, 'Button 3', lambda: print('Button 3 has been pushed!'))
mycheckbutton = simplewidgets.SimpleCheckbutton(mygridview, 'I approve of these buttons', lambda: print(f'User approval status: {mycheckbutton.read()}'))

mygridview.add_widgets([
    ((0, 0), (3, 1), mygridlabel),
    ((0, 1), (1, 1), button1),
    ((1, 1), (1, 1), button2),
    ((2, 1), (1, 1), button3),
    ((0, 2), (3, 3), mycheckbutton)
    ])
mygridview.build_grid()

myapp.change_view(myview)
myapp.start()
```

And just like that, you've created your first app using SimpleViews and SimpleWidgets! Hopefully you can see the simplicity of SimpleTkGUI, and how it can save you a lot of time perfecting your layouts, while giving you enough flexibility to fit your needs.

And of course, if SimpleTkGUI ever becomes too limiting, you can always fall back to writing in tkinter directly.

## Further Usage and Reading
Now that you know the basics, check out the source code to understand the customizations and input formats for each SimpleWidget. The general format is to provide a list of inputs, or a dictionary of label: value pairs.
If you want to learn more about changing the default fonts and styles, see the simplestyles module.
*All SimpleWidgets with text have a font argument that you can tweak for your needs. By default, it picks an appropriate font setting from the simplestyles module.*

# FAQ
### Why don't you use ttk styles?
Because I haven't gotten around to tinkering with them. I built the style classes as modularly as possible so I can swap them out with ttk styles eventually, if the limitations of tk styles becomes too much.

### Why is there a custom .read() function on SimpleWidgets? Why don't you just use .get()?
.get() doesn't cover some of the more complex wigets, such as SimpleListbox, so I needed a custom function to handle those. For consistency's sake, I gave each widget its own .read() function. You're welcome to call .get() directly if it fits your usecase.

### How does SimpleMenu work?
SimpleMenu looks complex because tkinter menus are complex. Here is a basic example to help get you started:

```
test_checkbutton = tk.BooleanVar()
test_radiobutton = tk.StringVar()
mymenu = SimpleMenu(myview, {
    'File': {
        'New': {
            'Option 1': lambda: print('User clicked Option 1'),
            'sep': '',
            'Option 2': lambda: print('User clicked Option 2')
        },
        'Open': lambda: print('User clicked Open')
    },
    'Edit': {
        'Option 3': lambda: print('User clicked Option 3'),
        'checkbutton': {
            'label': 'Click on me to toggle the test_checkbutton variable',
            'variable': test_checkbutton
        },
        'Radiobutton Menu': {
            'radiobutton': {
                'choices': {'label1': 'value1', 'label2': 'value2', 'label3': 'value3'},
                'variable': test_radiobutton
            }
        }
    }
}, context_menu=False)
```

To create a context menu (which appears when you right-click a widget), create a SimpleMenu and supply a widget instead of a view. You must also set the context_menu argument to True.
To create accelerators (hotkeys for menu items), identify the menu option using a dictionary, and provide a tuple of strings:

```
menu.add_accelerator({'File': {'New': 'Option 2'}}, ('Ctrl', 'N'))
```