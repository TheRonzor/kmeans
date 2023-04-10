##########################################################################
#  The author of this code claims no rights or responsibilities for it.  #
#  The code is provided as is, with the hope that you will enjoy and/or  #
#  learn from it.                                                        #
#                                                                        #
#  I would also like to share a blessing with you that was shared with   #
#  me through another random piece of code, long ago in a far away land: #
#                                                                        #
#      May you do good and not evil                                      #
#      May you find forgiveness for yourself and forgive others          #
#      May you share freely, never taking more than you give.            #
#                                                                        #
##########################################################################

import tkinter as tk
from tkinter import messagebox
from traceback import print_exc

class SimpleWindow():
    '''A window with a settings area and a Go button'''

    LBL_ANCHOR          = tk.E  # Labels are anchored to the east
    INP_ANCHOR          = tk.W  # Input boxes are anchored to the west

    DFLT_LBL_WIDTH      = 5     # Default width of labels
    DFLT_INP_WIDTH      = 5     # Default width of inputs

    LBL_H               = 2     # Height of labels and inputs
    PADX                = 10    # Default x padding between things

    # Keys for settings dictionary
    SD_LABEL            = 'label'
    SD_INPUT            = 'input'
    SD_VALUE            = 'value'
    SD_TYPE             = 'type'

    def __init__(self,
                 geometry='500x150', 
                 title='A Simple Window', 
                 num_columns = 2
                 ):
        self.main = tk.Tk()
        self.main.geometry(geometry)

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
        self.settings.grid(row=0)

        # To keep track of which row and column
        self.current_row = 0
        self.current_column = 0
        self.num_columns = num_columns

        # Dictionary to store all the settings
        self.settings_dict = {}

        # The go button will go in the second row of the interface
        go = tk.Button(self.interface, text="Let's go!", command=self.Go, height=3)
        go.grid(row=1, sticky=tk.S)
        return
    
    def BindGo(self, fun, **kwargs):
        self.go_fun = fun
        self.kwargs = kwargs
        return
    
    def AddSetting(self, label, inp_type, default, label_width=DFLT_LBL_WIDTH, input_width=DFLT_INP_WIDTH):
        '''Add label and tk.Entry to the settings frame',
           and store a reference to the value in a dictionary.

           The values provided for 'label' should be unique, since they'll be the keys in the dictionary.

           For tk.Entry boxes, supply a single value for default
           for tk.OptionMenu, provide a tuple, with the default as the first element
        '''

        if type(default) != tuple:
            self.settings_dict[label] = {
                                         self.SD_LABEL: tk.Label(self.settings, text = label, height = self.LBL_H), #width=label_width),
                                         self.SD_INPUT: tk.Entry(self.settings, width = input_width),
                                         self.SD_TYPE: inp_type
                                        }
            self.settings_dict[label][self.SD_INPUT].insert(0, default)
        else:
            self.settings_dict[label] = {
                                         self.SD_LABEL: tk.Label(self.settings, text = label, height = self.LBL_H), #width=label_width),
                                         self.SD_VALUE: tk.StringVar(),
                                         self.SD_TYPE: inp_type
                                        }
            self.settings_dict[label][self.SD_VALUE].set(default[0])
            self.settings_dict[label][self.SD_INPUT] = tk.OptionMenu(self.settings, self.settings_dict[label][self.SD_VALUE], *default)
        
        # Grid settings
        self.settings_dict[label][self.SD_LABEL].grid(row=self.current_row, 
                                                      column=self.current_column*2, 
                                                      padx=self.PADX,
                                                      sticky = self.LBL_ANCHOR)
        
        self.settings_dict[label][self.SD_INPUT].grid(row=self.current_row, 
                                                      column=self.current_column*2+1, 
                                                      padx=self.PADX, 
                                                      sticky = self.INP_ANCHOR)

        self.current_column+=1
        if self.current_column == self.num_columns:
            self.current_column = 0
            self.current_row+=1
            self.settings.rowconfigure(self.current_row, weight=1)
        
        return label
    
    def GetSetting(self, label):
        s = self.settings_dict[label]
        t = s[self.SD_TYPE]
        tkt = type(s[self.SD_INPUT])

        if tkt == tk.Entry:
            return t(s[self.SD_INPUT].get())
        elif tkt == tk.OptionMenu:
            return t(s[self.SD_VALUE].get())
        else:
            raise NotImplementedError('Support for', tkt, 'not implemented.')
        
    def CenterMain(self):
        """Center the main window. Should still set the initial geometry ahead of time, and only call after all widgets have been added.
            Solution from:
            https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        """

        self.main.attributes('-alpha', 0.0)
        self.main.update_idletasks()
        width = self.main.winfo_width()
        frm_width = self.main.winfo_rootx() - self.main.winfo_x()
        win_width = width + 2 * frm_width
        height = self.main.winfo_height()
        titlebar_height = self.main.winfo_rooty() - self.main.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.main.winfo_screenwidth() // 2 - win_width // 2
        y = self.main.winfo_screenheight() // 2 - win_height // 2
        self.main.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.main.deiconify()
        self.main.attributes('-alpha', 1.0)
        
        return

    def Deploy(self):
        self.interface.pack(padx=20, pady=20)
        self.CenterMain()
        self.main.mainloop()
        return
    
    def Go(self):
        try:
            local_kwargs = {}
            for key, value in self.kwargs.items():
                local_kwargs[key] = self.GetSetting(value)
            self.go_fun(**local_kwargs)
        except Exception as e:
            print(print_exc())
            messagebox.showerror(title='Error', message=str(e))
        return