import tkinter as tk
from tkinter import messagebox
import kmaf

class SimpleWindow():
    '''A window with a settings area and a Go button'''

    LBL_ANCHOR  = tk.E
    INP_ANCHOR  = tk.W

    LBL_H       = 2
    PADX        = 10

    def __init__(self, geometry='400x150', title='A Simple Window'):
        self.main = tk.Tk()
        self.main.geometry(geometry) # Resize and center automatically later
        self.main.title(title)

        # Partition the window into a row for the settings and a row for the go button
        self.interface = tk.Frame(self.main)
        self.interface.rowconfigure(0, weight=1)
        self.interface.rowconfigure(1, weight=1)

        # The settings frame will be a subset of the interface frame,
        # and start with a single row
        self.settings = tk.Frame(self.interface)
        self.settings.rowconfigure(0, weight=1)

        # The go button will go in the second row of the interface
        go = tk.Button(self.interface, text="Let's go!", command=self.Go, height=3)
        go.grid(row=1, sticky=tk.S)
        return
    
    def Go(self):
        print('Go where?')
        return
    
    def AddEntry(self, label, default, width=5):
        '''Add label and tk.Entry to the settings frame',
           and store a reference to the value in a dictionary.

           The values provided for 'label' should be unique
           '''


        return
    
    def GetEntry(label):
        
        return

    def Deploy(self):
        self.interface.pack(padx=20, pady=20)
        self.main.mainloop()
        return


s = SimpleWindow()
s.Deploy()