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

import kmaf
import RonsWindows

# Create a new SimpleWindow
s = RonsWindows.SimpleWindow(title='Animation Controls')

# Add the widgets:
#  - They will be added in order, left to right, then top to bottom.

#  - AddSetting() takes as inputs:
#        label: The text you want to see next to each input box

#        inp_type: The datatype of the setting, e.g. int, str, float

#        default: Either a single value (which will create a tk.Entry box)
#                 or a tuple (which will crate a tk.OptionMenu, with the first value
#                 in the tuple as the default) 
#
#  - By default, the settings will be organized into 2 columns and as
#    many rows as needed. To change the number of columms, provide a value 
#    for num_columns when calling SimpleWindow() above.
#    
#  
#  - The "Go" button will be placed below these rows, centered horizontally.

#    This button is configured by calling the BindGo() function, and passing
#    in a function, followed by keyword arguments equal to the outputs of AddSetting()

k           = s.AddSetting('k (actual) = ', int, 3)
init_method = s.AddSetting('Init. Method = ', str, kmaf.KMeansAnim.INIT_METHODS, input_width=10)
kg          = s.AddSetting('k (guess) = ', int, 3)
seed        = s.AddSetting('Seed = ', int, kmaf.np.random.randint(1000))
n           = s.AddSetting('n = ', int, 100)
cmap        = s.AddSetting('Colormap = ', str, 'rainbow', input_width=10)

# Tell the Go button what to run when pressed
s.BindGo(kmaf.KMeansAnim,
            n_clusters       = k,
            n_clusters_guess = kg,
            n_points         = n,
            method           = init_method,
            seed             = seed,
            cmap             = cmap
         )

# Show the window
s.Deploy()