#   May you do good and not evil
#   May you find forgiveness for yourself and forgive others
#   May you share freely, never taking more than you give.


        ##############################
        # The Fun and Fancy Version! #
        ##############################


import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from sklearn.datasets import make_blobs as mb
from matplotlib.animation import FuncAnimation
from sklearn.preprocessing import MinMaxScaler as MMS

plt.style.use('dark_background')

__version__ = '0.0.1'

class KMeansAnim():
    FIG_SIZE    = (8,8)
    
    # Marker settings
    ALPHA_DATA  = 0.6
    ALPHA_CENT  = 0.9
    SIZE_DATA   = 20
    SIZE_CENT   = 500

    DT          = 0.01   # For sleep()
    DX          = 0.1    # Old idea
    TOL         = 1e-12  # Old idea

    # Transition curve
    SIGMOID_A   = 0.5       # Timing (1)
    SIGMOID_K   = 3         # Sharpness (2)
    SIGMOID_RES = 15        # Number of points
    SIGMOID_MIN = 0.01
    SIGMOID_MAX = 1.00
    
    def __init__(self, 
                 n_points           = 750, 
                 n_clusters         = 3, 
                 n_clusters_guess   = None, 
                 method             = 'from_data',
                 seed               = None):
        
        # Initialize settings
        self.n_points   = n_points
        self.n_clusters = n_clusters
        
        if n_clusters_guess is None:
            # Default guess is the clairvoyant one, since my AI is the best AI ;-)
            self.n_clusters_guess = self.n_clusters
        else:
            self.n_clusters_guess = n_clusters_guess
        
        if seed is None:
            self.seed = np.random.randint(1000)
        else:
            self.seed = seed
        
        self.rng = np.random.RandomState(self.seed)

        # Create the data
        self.data, self.y = mb(n_samples    = self.n_points, 
                               centers      = self.n_clusters, 
                               n_features   = 2,  
                               random_state = self.rng)
        self.data = MMS().fit_transform(self.data) # Rescale data to be in the unit square

        # Create the centroids
        if method == 'naive':
            self.centroids = self.rng.random(size=(self.n_clusters, 2))
        elif method == 'from_data':
            self.centroids = self.data[self.rng.choice(self.data.shape[0], replace=False, size=self.n_clusters_guess)]
        elif method == 'k++':
            raise(NotImplementedError())
        self.cluster_colors = get_cmap('rainbow')(np.linspace(0, 1, self.n_clusters_guess))[:,:-1] # Everything except the alpha

        # Initialize a placeholder for new centroids, out of range
        #self.new_centroids = -np.ones(shape=[self.n_clusters_guess, 2])
        self.new_centroids = self.centroids.copy()

        # Transition curve for animations
        self.sigmoid = 1/(1+(1/np.linspace(self.SIGMOID_MIN,self.SIGMOID_MAX, self.SIGMOID_RES)**self.SIGMOID_A-1)**self.SIGMOID_K)
        self.path_pos = self.SIGMOID_RES-1

        # Initialize the figure objects
        self.fig, self.ax = plt.subplots(figsize=self.FIG_SIZE)

        self.scat_data = plt.scatter([], [], ec='k', alpha = self.ALPHA_DATA, s = self.SIZE_DATA)
        self.scat_cent = plt.scatter([], [], ec='w', s = self.SIZE_CENT, marker='*', linewidths=1.5)

        # Initialize the color arrays
        self.color_data = np.ones([len(self.data),3])
        self.color_cent = self.cluster_colors

        # Make the centroids invisible for now
        self.scat_cent.set_alpha(0)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-0.01,1.01)
        self.ax.set_ylim(-0.01,1.01)
        return

    def ShowInitialData(self):
        # Unused, get rid of it
        return self.scat_data, self.scat_cent,

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
            self.hold = True
            self.steps = 0
        #elif frame_number == 1:
            #self.UpdateClusters()
            #self.first = True
        else:
            if self.path_pos == self.SIGMOID_RES-1:
                self.steps += 1
                self.ax.set_title('Iteration: ' + str(self.steps))
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
            self.ax.set_title('We are done after ' + str(self.steps) + ' iterations.')
            self.ani.event_source.stop() 
        
        return self.scat_data, self.scat_cent, 

    def Go(self):
        self.ani = FuncAnimation(self.fig, 
                                 self.Update,
                                 #init_func = self.ShowInitialData,
                                 blit = False,  # Can't seem to get blitting to work with titles, even if using ax.text inside the plot area :-(
                                 interval = 33,
                                 cache_frame_data = True)
        plt.show()
        return

k = KMeansAnim()
k.Go()