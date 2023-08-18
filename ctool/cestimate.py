import copy
import numpy as np
import matplotlib.pylab as plt
from scipy.signal import medfilt,savgol_filter

def calc_cont(wave,flux, niter=5, boxsize=95, exclude=None):

    cont = copy.deepcopy(flux)
    for ii in np.arange(niter):
        smooth = medfilt(cont,boxsize)
        csubs = np.where(smooth>cont*0.99)
        cont = np.interp(wave,wave[csubs],cont[csubs])
    cont = savgol_filter(cont,boxsize*3,polyorder=2,mode='mirror')
    return cont
