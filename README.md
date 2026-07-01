ctool is a simple function to estimate the continuum of an emission line spectrum. 

This software is provided as-is, with no warranty.

  
INSTALLATION

using setup.py:
----------
python setup.py install

Using pip:
----------
Pip is not currently supported. 

Basic usage:
-------------
```python
from ctool.cestimate import calc_cont
cont = calc_cont(wavelength, fluxdensity)
```

Function signature:
-------------------
```python
calc_cont(wave, flux, niter=5, boxsize=95, exclude=None, threshold=0.998, 
          offset=0, spike_threshold=None, emission=True)
```

Parameters:
-----------
- **wave** (array): Wavelength array for the spectrum
- **flux** (array): Flux density array for the spectrum
- **niter** (int, default=5): Number of iterative refinement steps. More iterations allow better convergence to the true continuum, especially for spectra with many or closely-spaced emission/absorption features.
- **boxsize** (int, default=95): Size of the median filter window. **This is the most important parameter to tune** for your specific spectrum. Larger values produce smoother continua and are appropriate for broader features; smaller values track finer continuum variations. Should be odd and larger than the width of the narrowest features you want to remove.
- **exclude** (list of lists, default=None): List of wavelength ranges to exclude from continuum fitting, formatted as `[[w1_start, w1_end], [w2_start, w2_end], ...]`. Useful for masking broad absorption or emission bands that should not influence the continuum fit.
- **threshold** (float, default=0.998): Ratio threshold for identifying continuum-like points during iteration. For emission spectra, points where `smoothed > continuum * threshold` are considered continuum. Values closer to 1.0 are more conservative (fewer points considered continuum); values farther from 1.0 are more aggressive.
- **offset** (float, default=0): Constant offset applied to the final continuum estimate. Useful for manual adjustments or vertical shifting.
- **spike_threshold** (float, default=None): If specified, removes negative spikes (for emission spectra) or positive spikes (for absorption spectra) with prominence above this threshold before fitting. Uses `scipy.signal.find_peaks` to identify spikes. Useful for removing cosmic rays or bad pixels.
- **emission** (bool, default=True): Set to `True` for emission line spectra (features above continuum) or `False` for absorption line spectra (features below continuum). This flips the logic of the algorithm appropriately.

Returns:
--------
- **cont** (array): Estimated continuum flux array, same shape as input flux

Examples:
---------

**Basic emission line spectrum:**
```python
import numpy as np
from ctool.cestimate import calc_cont

wave = np.linspace(1, 10, 1000)
flux = np.ones_like(wave) + np.random.normal(0, 0.01, wave.shape)
# Add emission line
flux[450:550] += 2 * np.exp(-((wave[450:550] - 5.5)**2) / 0.01)

cont = calc_cont(wave, flux, boxsize=95)
```

**Absorption line spectrum:**
```python
cont = calc_cont(wave, flux, emission=False, boxsize=51)
```

**Excluding broad bands:**
```python
# Exclude regions around 3.3 and 6.2 microns
cont = calc_cont(wave, flux, exclude=[[3.2, 3.4], [6.0, 6.4]], boxsize=95)
```

**Removing spikes and adjusting parameters:**
```python
cont = calc_cont(wave, flux, boxsize=75, niter=10, 
                 spike_threshold=5.0, threshold=0.995)
```

Tips:
-----
- **Tuning boxsize**: Start with a value ~2-3x the width of your typical emission/absorption feature in array indices. If the continuum follows features too closely, increase boxsize. If it misses real continuum variations, decrease boxsize.
- **Handling noisy spectra**: Increase `niter` to 7-10 for better convergence
- **Removing artifacts**: Use `spike_threshold` to automatically remove cosmic rays or bad pixels before fitting 
