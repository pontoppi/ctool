import copy
import numpy as np
import matplotlib.pylab as plt
from scipy.signal import medfilt,savgol_filter

def calc_cont(wave,flux, niter=5, boxsize=95, exclude=None, threshold=0.998, offset=0, spike_threshold=None):

    flux_tmp=copy.deepcopy(flux)

    #Remove negative spikes from consideration
    if(spike_threshold is not None):
        bad_pix, _ = find_peaks(-1*flux_tmp, prominence=spike_threshold)
        flux_tmp[bad_pix] = np.nan

    #Exclude regions    
    if(exclude is not None):
        for myexclude in exclude:  #Exclude regions from fitting
            localbool=((wave>myexclude[0]) & (wave<myexclude[1]))
            flux_tmp[localbool]=np.nan   
            
    #Perform continuum determination        
    cont = copy.deepcopy(flux_tmp)            
    for ii in np.arange(niter):
        smooth = medfilt(np.array(cont,dtype=float),boxsize)
        csubs = np.where(smooth>cont*threshold)   
        cont = np.interp(wave,wave[csubs],cont[csubs])

    cont = savgol_filter(cont,boxsize*3,polyorder=2,mode='mirror')
    
    #Apply offset
    cont+=offset
    
    return cont
