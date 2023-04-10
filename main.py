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

# Add the widgets
#  -They will be added in order, left to right, then top to bottom.
#  -For more columns, pass num_columns to SimpleWindow() above, the default is 2.
#  -Since there are 6 settings below, that means we'll have a 3 row x 2 column grid.
#  -The "Go" button will be placed below these rows, in the middle.

k           = s.AddSetting('k (actual) = ', int, 3)
init_method = s.AddSetting('Init. Method = ', str, kmaf.KMeansAnim.INIT_METHODS, input_width=10)
kg          = s.AddSetting('k (guess) = ', int, 3)
seed        = s.AddSetting('Seed = ', int, kmaf.np.random.randint(1000))
n           = s.AddSetting('n = ', int, 100)
cmap        = s.AddSetting('Colormap = ', str, 'rainbow', input_width=10)

# Pass in the function, the names of the parameters the function is expecting,
# and the variables above that correspond to each of the parameters
#
# This tells the interface what function to call, and which parameters to provide it when the Go button is pressed.
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