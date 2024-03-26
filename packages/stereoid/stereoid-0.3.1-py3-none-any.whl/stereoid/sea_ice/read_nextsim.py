__author__ = "Paco Lopez Dekker & Marcel Kleinherenbrink"
__email__ = "F.LopezDekker@tudeft.nl & m.kleinherenbrink@tudelft.nl"

import numpy as np
import scipy as sp
import os

# read full sea-ice model
def read_neXtSIM_npz(datadir,fname):
    # read data from model
    n = np.load(os.path.join(datadir, fname))
    return n # contains a lot of stuff, depending on the input file

# read data from velocity model
def read_from_npz(datadir,fname):
    # read data from model
    u = np.load(os.path.join(datadir, 'u.npy'))
    v = np.load(os.path.join(datadir, 'v.npy'))
    x = np.load(os.path.join(datadir, 'x.npy'))
    y = np.load(os.path.join(datadir, 'y.npy'))
    return u,v,x,y # returns velocities and locations

# read data from Tandem-X velocity
def read_from_mat(datadir,fname):
    # at the moment it does not provide the velocity direction
    # we have to scale the velocity in the scene generator
    vel=sp.io.loadmat(os.path.join(datadir, fname))

    # resolution is 100 meter
    return vel

if __name__ == '__main__':
    datadir =  '/hdd/data/Stereoid/Data/SeaIce/VelocityModel/'
    fname =  '20180507_nextsim_karasea_xyuv.npz'
    data = np.load(os.path.join(datadir, fname))