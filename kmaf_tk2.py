import tkinter as tk
from tkinter import messagebox
import kmaf


class Setting():
    # Not sure if it's worth going this far...
    def __init__(self, name, default, options=None):
        pass
        return



class SimpleWindow():
    '''A window with a settings area and a Go button'''

    LBL_ANCHOR          = tk.E
    INP_ANCHOR          = tk.W

    LBL_H               = 2
    PADX                = 10

    DFLT_INP_WIDTH      = 5

    SD_LABEL            = 'label'
    SD_INPUT            = 'input'

    def __init__(self, geometry='400x150', title='A Simple Window'):
        self.main = tk.Tk()
        self.main.geometry(geometry) # Resize and center automatically later [_]
        self.main.title(title)

        # Partition the window into a row for the settings and a row for the go button
        # We'll call this partition the interface
        self.interface = tk.Frame(self.main)
        self.interface.rowconfigure(0, weight=1) # The Settings grid goes in this row
        self.interface.rowconfigure(1, weight=1) # The GO button gets its own row

        # The settings frame is a subset of the interface frame,
        # and starts with a single row (we'll add more rows as needed as we add widgets)
        self.settings = tk.Frame(self.interface)
        self.settings.rowconfigure(0, weight=1)

        # Dictionary to store all the settings
        self.settings_dict = {}

        # The go button will go in the second row of the interface
        go = tk.Button(self.interface, text="Let's go!", command=self.Go, height=3)
        go.grid(row=1, sticky=tk.S)
        return
    
    def Go(self):
        print('Go where? Pass me a function my friend.')
        return
    
    def AddSetting(self, label, default, width=5):
        '''Add label and tk.Entry to the settings frame',
           and store a reference to the value in a dictionary.

           The values provided for 'label' should be unique, since they'll be the keys in the dictionary.

           default can be a single value (implying this should be a tk.Entry)
           or a list/tuple/etc (implying this should be a tk.OptionMenu).

           If the latter, the key/index of the default value should also be supplied
        '''

        self.settings_dict[label] = {self.SD_LABEL: tk.Label(self.settings, text = label, height = self.LBL_H),
                                     self.SD_INPUT: tk.Entry(self.settings, width = self.DFLT_INP_WIDTH)
                                    }
        
        #
        # Need row and column logic in grid
        # fill the row first, then go to the next column
        # so, specify row and/or column counts in __init__ if that makes sense
        #
        self.settings_dict[label].grid()



        return
    
    def GetSetting(label):
        
        return

    def Deploy(self):
        self.interface.pack(padx=20, pady=20)
        self.main.mainloop()
        return


s = SimpleWindow()
s.Deploy()