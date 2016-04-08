import numpy as np
import xarray

def mass_streamfunction(data, a=6317.0e3, g=9.8):
    """Calculate the mass streamfunction for the atmosphere.

    Based on a vertical integral of the meridional wind.
    Ref: Physics of Climate, Peixoto & Oort, 1992.  p158.

    `a` is the radius of the planet (default Earth 6317km).
    `g` is surface gravity (default Earth 9.8m/s^2).

    Returns an xarray DataArray of mass streamfunction.
    """
    vbar = data.vcomp.mean('lon')
    c = 2*np.pi*a*np.cos(vbar.lat*np.pi/180) / g
    return c*np.cumsum(vbar, axis=vbar.dims.index('pfull'))


if __name__ == '__main__':
    # example calculating EPV for a GFDL dataset
    d = xarray.open_dataset('/scratch/jp492/gfdl_data/ref_earth/ref_earth_grey/run20/daily.nc',
        decode_times=False)
    d['mass_sf'] = mass_streamfunction(d)
    print d.mass_sf
    d.close()