import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap
from matplotlib.colors import to_rgba
import math
#from joblib import Parallel as prl

import sys

import pandas as pd
import seaborn as sns

plt.style.use('dark_background')

__version__ = '3.0.0'

# Helpers (faster if accessed within the class?)

# For working with the condensed distance matrix
# https://stackoverflow.com/questions/13079563/how-does-condensed-distance-matrix-work-pdist
def calc_row_idx(k, n):
    return int(math.ceil((1/2.) * (- (-8*k + 4 *n**2 -4*n - 7)**0.5 + 2*n -1) - 1))
def elem_in_i_rows(i, n):
    return i * (n - 1 - i) + (i*(i + 1))//2
def calc_col_idx(k, i, n):
    return int(n - elem_in_i_rows(i + 1, n) + k)
def condensed_to_square(k, n):
    i = calc_row_idx(k, n)
    j = calc_col_idx(k, i, n)
    return i, j

class Particle():
    DFLT_SIZE  = 10
    def __init__(self, type, color, size=None, pos=None):
        self.color = color
        if size is None:
            self.size = self.DFLT_SIZE
        else:
            self.size = size
            
        if pos is None:
            #self.pos = np.random.uniform(0, World.SIZE, size=(2))
            self.pos = np.random.normal(loc=World.SIZE/2, size=2)%World.SIZE
        else:
            self.pos = pos
        self.type = type
        self.index = None # Will be obtained from the world
        return

class World():
    SIZE = 100
    FIG_SIZE = (6,6)
    PAD = SIZE/1000
    DAMPING = 0.975
    JITTER = SIZE/1e6 # 0.0001

    # Radius and force rules
    #r = SIZE*np.array([0.075, 0.10, 0.125])
    r = SIZE*np.array([0.150, 0.175, 0.200])
    f = (-0.01,0.10)

    # Coefficients for force function
    m0 = -f[0]/r[0]
    m1 = f[1]/(r[1]-r[0])
    m2 = -f[1]/(r[2]-r[1])
    
    def __init__(self, prec=None):
        self.particles = []
        self.pos_arr = None
        self.vel_arr = None

        self.dist_arr = None
        
        self.type_arr = None
        self.size_arr = None
        self.color_arr = None

        # Unique versions of above
        self.colors_unique = []
        self.sizes_unique = []

        self.fig, self.ax = plt.subplots(figsize=World.FIG_SIZE)
        self.scat = plt.scatter([],[])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-World.PAD, World.SIZE+World.PAD)
        self.ax.set_ylim(-World.PAD, World.SIZE+World.PAD)

        if prec == 16:
            self.prec = np.float16
        elif prec == 32:
            self.prec = np.float32
        else:
            self.prec = np.float64

        self.eps = np.finfo(self.prec).eps

        self.ax.set_title(str(self.prec))
        return

    def CreateParticles(self, type, color, n=20, size=None, pos=None):
        for _ in range(n):
            p = Particle(type=type, color=color, size=size, pos=pos)
            p.index = len(self.particles)
            self.particles.append(p)
        
        # Unique entries (in order)
        self.colors_unique.append(color)
        self.sizes_unique.append(size)
        return
    
    def CreateRandomInteractions(self):
        num_types = len(np.unique(self.type_arr))
        self.Laws = np.random.uniform(low=-1, high=1, size=[num_types]*2)
        return
    
    def CustomInteraction(self, reactor, reacts_to, magnitude):
        self.Laws[reactor, reacts_to] = magnitude
        return
    
    def ShowInteractionMatrix(self):
        label_loc = [n+0.5 for n in range(self.num_types)]
        fig, ax = plt.subplots(figsize=(6,6))
        ax.scatter(label_loc, [-0.2]*self.num_types, c=self.colors_unique, clip_on=False, s=self.sizes_unique)
        ax.scatter([-0.2]*self.num_types, label_loc, c=self.colors_unique, clip_on=False, s=self.sizes_unique)
        sns.heatmap(self.Laws, vmin=-1, vmax=1, cmap = 'bwr_r', 
                    cbar=False, annot=True, fmt='.1f',
                    linewidths=0.5, linecolor='k')
        ax.set_xticks([])
        ax.set_yticks([])
        fig.show()
        return

    def InitData(self):
        pos=[]
        col=[]
        sz=[]
        typ=[]
        for p in self.particles:
            pos.append(p.pos)
            col.append(p.color)
            sz.append(p.size)
            typ.append(p.type)
            
        self.pos_arr = np.array(pos, dtype=self.prec)
        self.color_arr = np.array(col)
        self.size_arr = np.array(sz)
        self.type_arr = np.array(typ)

        # Things we'll need occasionally
        self.num_types = len(np.unique(self.type_arr))

        # Things we'll need a lot
        self.num_particles = len(self.pos_arr)
        self.num_combs = math.comb(self.num_particles, 2) # Requires Python > 3.8

        self.CreateRandomInteractions()

        # FOR TESTING - random initial velocities
        self.vel_arr = np.random.normal(size=self.pos_arr.shape).astype(self.prec)

        self.scat.set_offsets(self.pos_arr)
        self.scat.set_color(self.color_arr)
        self.scat.set_sizes(self.size_arr)

        # LOL.
        self.dir_arr = np.zeros([self.num_combs, 2]).astype(self.prec)
        self.dist_arr = (np.sum(self.dir_arr**2, axis=1)**0.5).astype(self.prec)
        
        return self.scat,
    
    def ComputeDistances(self):
        k=0
        for i in range(self.num_particles):
            for j in range(i+1, self.num_particles):
                self.dir_arr[k] = (self.pos_arr[j] - self.pos_arr[i])
                k+=1
        idx = abs(self.dir_arr)>World.SIZE/2
        self.dir_arr[idx] = (World.SIZE - abs(self.dir_arr[idx]))*(-np.sign(self.dir_arr[idx]))
        self.dist_arr = np.sum(self.dir_arr**2, axis=1)**0.5
        return
    
    # Should be static
    def ComputeForce(self, d):
        if d<World.r[0]:
            return World.m0*d+World.f[0]
        elif d<World.r[1]:
            return World.m1*(d-World.r[0])
        elif d<World.r[2]:
            return World.m2*(d-World.r[2])
        else:
            return 0

    def UpdateVel(self):
        self.ComputeDistances()
        idx = np.where(self.dist_arr<World.r[2])[0]

        self.vel_arr *= World.DAMPING
        if World.JITTER:
            self.vel_arr += np.random.normal(scale = World.SIZE*World.JITTER, size=[self.num_particles,2])

        for k in idx:
            i,j, = condensed_to_square(k, self.num_particles)
            f = self.ComputeForce(self.dist_arr[k])
            self.dist_arr[np.where(self.dist_arr == 0)] = self.eps
            base_force = f*(self.dir_arr[k]/self.dist_arr[k])
            if self.dist_arr[k]>World.r[0]:
                self.vel_arr[i,:] += base_force*self.Laws[self.type_arr[i],self.type_arr[j]]
                self.vel_arr[j,:] -= base_force*self.Laws[self.type_arr[j],self.type_arr[i]]
            else:
                self.vel_arr[i,:] += base_force
                self.vel_arr[j,:] -= base_force

        return

    def Move(self,_):
        self.UpdateVel()
        self.pos_arr += self.vel_arr
        self.pos_arr %= World.SIZE
        self.scat.set_offsets(self.pos_arr)
        return self.scat,

    def Go(self, show_interactions=False):

        if show_interactions: 
            self.ShowInteractionMatrix()
        
        self.ani = FuncAnimation(self.fig, 
                                 self.Move,
                                 blit=True, 
                                 interval=1,
                                 cache_frame_data=False)
        plt.show()
        return

seed = int(sys.argv[1])
prec = int(sys.argv[2])

np.random.seed(seed)
print('Prec:', prec, 'Seed:', seed)

if seed is None or seed==-1:
        seed = np.random.randint(1,1000)
w = World(prec=prec)

total_parts = 100
n_types = 3
num_each = int(total_parts/n_types)

for t in range(n_types):
    c = np.random.random(size=4)
    c[-1] = max(min(c[-1], 0.8), 0.4)
    s = np.random.randint(1,5)**4
    w.CreateParticles(type=t, color=c, size=s, n=num_each)

w.InitData()
w.Go(show_interactions=True)