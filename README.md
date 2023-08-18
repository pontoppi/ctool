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
>from ctool.cestimate import calc_cont
>cont = calc_cont(wavelength,fluxdensity)

Note that you may have to optimize the smoothing parameter <boxsize>. Also be aware that this
currently just works with narrow lines. A future version may add support to exlcude broader regions
with wide lines or bands. 