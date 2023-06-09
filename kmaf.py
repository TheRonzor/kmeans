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


        ##############################
        #         K-means            #
        # The Fun and Fancy Version! #
        ##############################

# This code runs an animated example of K-means.
# It is specifically designed for demonstration purposes,
# and is not intended for any actual analysis!

import numpy as np                                          # It's pronounced num-pee
from time import sleep                                      # because even computers need to slow down sometimes
import matplotlib.pyplot as plt                             # we're making pictures
from matplotlib.cm import get_cmap                          # get_cmap returns a colormap object which can be used to easily generate colors
from sklearn.datasets import make_blobs as mb               # this function makes blobs of data
from matplotlib.animation import FuncAnimation              # animation driver, it's kind of weird
from sklearn.preprocessing import MinMaxScaler as MMS       # all of the action will happen in the unit square

plt.style.use('dark_background')                            # it looks better in the dark

__version__ = '1.0.1'                                       # I might remember to update the version number occasionally

class KMeansAnim():
    FIG_SIZE    = (8,8)
    
    # Marker settings
    #  Data
    ALPHA_DATA  = 0.6
    SIZE_DATA   = 20

    #  Centroids
    ALPHA_CENT      = 0.9
    SIZE_CENT       = 500

    # Initialization choices for centroids
    INIT_METHODS    = (
                        'k++',               # k-means++
                        'Uniform',           # select uniformly from data
                        'Naive'              # any point in the plot area (unit square)
                        )

    # Transition curve for animation, (1/f) where f = 1 + (1/x^a - 1)^k
    SIGMOID_A   = 1.6       # "Timing"
    SIGMOID_K   = 2.4       # "Sharpness"
    SIGMOID_RES = 30        # Number of points
    SIGMOID_MIN = 0.01      # Not zero
    SIGMOID_MAX = 1.00      # Definitely one

    DT          = 1.00      # For sleeps, in seconds. So the animation doesn't run too fast.
    
    def __init__(self, 
                 n_points           = 420, 
                 n_clusters         = 42, 
                 n_clusters_guess   = None, 
                 method             = INIT_METHODS[0],
                 seed               = None,
                 cmap               = 'rainbow'):
        
        # Initialize cluster settings
        self.n_points   = n_points
        self.n_clusters = n_clusters
        
        if n_clusters_guess is None:
            # Default guess is the clairvoyant one
            self.n_clusters_guess = self.n_clusters
        else:
            self.n_clusters_guess = n_clusters_guess
        
        # Initialize PRNG
        if seed is None:
            self.seed = np.random.randint(1000)
        else:
            self.seed = seed
        print('Running with seed: ', self.seed)
        self.rng = np.random.RandomState(self.seed)

        # Create the data
        self.CreateData()

        # Create the centroids
        self.CreateCentroids(method)
        self.cluster_colors = get_cmap(cmap)(np.linspace(0, 1, self.n_clusters_guess))[:,:-1] # Everything except the alpha

        # Initialize a placeholder for new centroids
        self.new_centroids = self.centroids.copy()

        # Transition curve for animations
        self.sigmoid = 1/(1+(1/np.linspace(self.SIGMOID_MIN, self.SIGMOID_MAX, self.SIGMOID_RES)**self.SIGMOID_A-1)**self.SIGMOID_K)
        self.path_pos = self.SIGMOID_RES-1

        # Initialize the figure
        self.CreateFigure()

        # Run the animation
        self.Go()
        return
    
    def CreateData(self):
        self.data, self.y = mb(n_samples    = self.n_points, 
                               centers      = self.n_clusters, 
                               n_features   = 2,  
                               random_state = self.rng)
        self.data = MMS().fit_transform(self.data) # Rescale data to be in the unit square for these examples
        return

    def CreateCentroids(self, method):
        if method == 'Naive':
            self.centroids = self.rng.random(size=(self.n_clusters_guess, 2))
        elif method == 'Uniform':
            self.centroids = self.data[self.rng.choice(self.data.shape[0], replace=False, size=self.n_clusters_guess)]
        elif method == 'k++':
            # Select first centroid uniformly from the data
            self.centroids = self.data[self.rng.choice(self.data.shape[0]), :].reshape(1,-1)
            while self.centroids.shape[0] < self.n_clusters_guess:
                # Initialize distance array
                d = np.zeros(shape=[self.data.shape[0], self.centroids.shape[0]])
                
                # Compute squared distance from each point to each centroid
                for i, c in enumerate(self.centroids):
                    d[:,i] = np.sum((self.data-c)**2,axis=1)
                
                # Minimum squared distance for each point
                p = np.min(d, axis=1)
                
                # Select the next centroid from the data with probability proportional
                # to the squared distance to the closest centroid
                idx = self.rng.choice(len(self.data), p=p/sum(p))
                new_centroid = self.data[idx,:].reshape(1,-1)
                self.centroids = np.concatenate([self.centroids, new_centroid], axis=0)
        else:
            raise ValueError('Unknown initialization method:', method)
        return
    
    def CreateFigure(self):
        self.fig, self.ax = plt.subplots(figsize=self.FIG_SIZE)

        # Initialize empty plots with display settings for data and centroids
        self.scat_data = plt.scatter([], [], ec='k', alpha = self.ALPHA_DATA, s = self.SIZE_DATA)
        self.scat_cent = plt.scatter([], [], ec='w', s = self.SIZE_CENT, marker='*', linewidths=1.5)

        # Initialize the color arrays
        self.color_data = np.ones([len(self.data),3])
        self.color_cent = self.cluster_colors

        # Make the centroids invisible at first
        self.scat_cent.set_alpha(0)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-0.01,1.01)
        self.ax.set_ylim(-0.01,1.01)
        return
    
    def UpdateClusters(self):
        distances = []
        for c in self.centroids:
            d = np.sum((self.data - c)**2,axis=1)
            distances.append(d)
        self.labels = np.argmin(np.array(distances).T,axis=1)

        for label in np.unique(self.labels):
            idx = np.where(self.labels == label)
            self.color_data[idx, :] = self.cluster_colors[label, :]
        self.scat_data.set_color(self.color_data)
        return
    
    def UpdateCentroids(self):
        for i in range(self.n_clusters_guess):
            idx = self.labels == i
            if sum(idx) == 0:
                # Throw any unused centroids out of frame
                self.new_centroids[i,:] = [5,5]
            else:
                self.new_centroids[i,:] = np.mean(self.data[idx,:], axis=0)
        return
    
    def MoveAlongCentroidPath(self):
        self.path_pos += 1
        self.centroids = self.centroid_path[self.path_pos, :]
        return
    
    def CreateCentroidPath(self):
        self.path_pos = 0
        self.centroid_path = self.centroids + np.array([si*(self.new_centroids - self.centroids) for si in self.sigmoid])
        return
    
    def CheckIfDone(self):
        return np.max(np.abs(self.centroids - self.new_centroids)) == 0

    def Update(self, frame_number):
        if frame_number == 0:
            self.scat_cent.set_facecolor(self.color_cent)
            self.scat_cent.set_alpha(self.ALPHA_CENT)
            self.scat_data.set_offsets(self.data)
            self.steps = 0
            self.hold = True
        else:
            if self.path_pos == self.SIGMOID_RES-1:
                self.steps += 1
                self.ax.set_title('Iteration: ' + str(self.steps))
                sleep(self.DT)
                self.UpdateClusters()
                self.UpdateCentroids()
                self.CreateCentroidPath()
            else:
                self.MoveAlongCentroidPath()
                self.hold=True

        self.scat_cent.set_offsets(self.centroids)

        if self.hold:
            self.hold = False
        elif self.CheckIfDone():
            self.ax.set_title('We are done after ' + str(self.steps-1) + ' iteration(s).')
            self.ani.event_source.stop() 
        
        return self.scat_data, self.scat_cent, 

    def Go(self):
        self.ani = FuncAnimation(self.fig, 
                                 self.Update,
                                 blit = False,  # Can't seem to get blitting to work when the figure has titles, even if using ax.text inside the plot area as many have recommended :-(
                                 interval = 10,
                                 cache_frame_data = True)
        plt.show()
        return

# In case we want to run it like a script.
if __name__ == '__main__':
    k = KMeansAnim()