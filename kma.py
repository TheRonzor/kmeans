#   May you do good and not evil
#   May you find forgiveness for yourself and forgive others
#   May you share freely, never taking more than you give.

import sys
import math
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import to_rgba
from sklearn.datasets import make_blobs as mb
from sklearn.preprocessing import MinMaxScaler as MMS
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')

__version__ = '0.0.1'

class KMeansAnim():
    FIG_SIZE    = (4,4)
    ALPHA_DATA  = 0.9
    ALPHA_CENT  = 0.6
    SIZE_DATA   = 20
    SIZE_CENT   = 100
    DT = 0.2

    def __init__(self, 
                 n_points           = 100, 
                 n_clusters         = 3, 
                 n_clusters_guess   = None, 
                 seed               = 42):
        
        # Initialize PRNG
        self.seed = seed
        self.rng = np.random.RandomState(self.seed)
        
        # Initialize data
        self.n_points   = n_points
        self.n_clusters = n_clusters
        
        # Default guess is the clairvoyant one, since my AI is the best AI ;-)
        if n_clusters_guess is None:
            self.n_clusters_guess = self.n_clusters
        else:
            self.n_clusters_guess = n_clusters_guess
        
        # Create the data
        self.data, self.y = mb(n_samples    = self.n_points, 
                               centers      = self.n_clusters, 
                               n_features   = 2,  
                               random_state = self.rng)
        
        
        # Rescale data to be in the unit square
        self.data = MMS().fit_transform(self.data)

        # Create the centroids
        self.CreateCentroids()

        # Combine data and centroids into a single arrray
        self.X = np.concatenate([self.data, self.centroids])

        # Color all the points white at first
        self.color_arr = np.ones([len(self.X),4])
        self.color_arr[:,-1] = self.ALPHA_DATA
        
        # Set the colors for the centroids, but make them transparant (opaque for testing)
        self.color_arr[self.n_points:, :-1] = self.cluster_colors
        self.color_arr[self.n_points:, -1] = self.ALPHA_CENT
        
        # Set the sizes for data and centroids
        self.size_arr = [self.SIZE_DATA]*self.n_points + [self.SIZE_CENT]*self.n_clusters_guess

        # Initialize the figure
        self.fig, self.ax = plt.subplots(figsize=KMeansAnim.FIG_SIZE)
        self.scat = plt.scatter(self.X[:,0], self.X[:,1], ec='k')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-0.1,1.1)
        self.ax.set_ylim(-0.1,1.1)
        
        self.scat.set_color(self.color_arr)
        self.scat.set_sizes(self.size_arr)

        return
    
    def CreateCentroids(self, method='from_data'):
        if method == 'naive':
            self.centroids = self.rng.random(size=(self.n_clusters, 2))
        elif method == 'from_data':
            self.centroids = self.data[self.rng.choice(self.data.shape[0], replace=False, size=self.n_clusters_guess)]
        elif method == 'k++':
            raise(NotImplementedError())
        self.cluster_colors = get_cmap('rainbow')(np.linspace(0, 1, self.n_clusters_guess))[:,:-1]
        print(self.cluster_colors)
        return 

    def ShowInitialData(self):
        print('Called ShowInitialData')
        sleep(self.DT)
        print('Exit ShowInitialData')
        return self.scat,

    def UpdateClusterLabels(self):
        distances = []
        for c in self.centroids:
            d = np.sum((self.data - c)**2,axis=1)
            distances.append(d)
        self.labels = np.argmin(np.array(distances).T,axis=1)
        return

    def Update(self, frame_number):
        if frame_number == 0:
            print('f1')
            self.UpdateClusterLabels()
        elif frame_number == 1:
            print('f2')
            self.X += 0.01
            self.X %= 1
        else:
            print('fN')
            self.X += 0.01
            self.X %= 1
        self.scat.set_offsets(self.X)
        return self.scat,

    def Go(self):
        self.ani = FuncAnimation(self.fig, 
                                 self.Update,
                                 blit=False, 
                                 interval=1000,
                                 cache_frame_data=True)
        plt.show()
        return

k = KMeansAnim()
k.Go()