import numpy as np
import xarray

def mass_streamfunction(data, v='vcomp', a=6317.0e3, g=9.8):
    """Calculate the mass streamfunction for the atmosphere.

    Based on a vertical integral of the meridional wind.
    Ref: Physics of Climate, Peixoto & Oort, 1992.  p158.

    Parameters
    ----------
    data :  xarray.DataSet
        GCM output data
    v : str, optional
        The name of the meridional flow field in `data`.  Default: 'vcomp'
    a : float, optional
        The radius of the planet. Default: Earth 6317km
    g : float, optional
        Surface gravity. Default: Earth 9.8m/s^2

    Returns
    -------
    streamfunction : xarray.DataArray
        The meridional mass streamfunction.
    """
    vbar = data[v].mean('lon')
    c = 2*np.pi*a*np.cos(vbar.lat*np.pi/180) / g
    # take a diff of half levels, and assign to pfull coordinates
    dp = xarray.DataArray(data.phalf.diff('phalf').values*100, coords=[('pfull', data.pfull)])
    return c*np.cumsum(vbar*dp, axis=vbar.dims.index('pfull'))


if __name__ == '__main__':
    # example calculating EPV for a GFDL dataset
    d = xarray.open_dataset('/scratch/jp492/gfdl_data/ref_earth/ref_earth_grey/run20/daily.nc',
        decode_times=False)
    d['mass_sf'] = mass_streamfunction(d)
    print d.mass_sf
    d.close()