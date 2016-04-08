"""Ertel Potential Vorticity functions for xarray datasets (http://xarray.pydata.org/en/stable/).

To use, you must first compile the fortran file epv.f90:

    $ cd ShareCode/execlim/analysis
    $ f2py -m -c _epv epv.f90
"""
import numpy as np
import xarray

from execlim.analysis import get_pressure
import _epv

__all__ = ['theta', 'ertelPV']

rad  = np.pi / 180.0

def theta(d, p0=None, field_name='temp'):
    """Calculate potential temperature for an xarray dataset.
    Returns a DataArray `pot_temp`."""
    Rd = 287.0
    Cp = 1004.0
    K = Rd / Cp
    if p0 is None:
        p0 = d.phalf.max()
    t = d[field_name]
    p = get_pressure(t)
    theta =  t * (p0 / p) ** K
    theta.name = 'pot_temp'
    return theta

def ertelPV(d, field_names={}):
    """Calculates ertelPV for an xarray dataset d.
    Dataset must have `ucomp`, `vcomp`, `temp` fields.
    Alternate field names can be passed as a dict
    e.g. {'ucomp': 'my_ucomp'}.
    returns a dataarray `ertelPV`."""
    u = d[field_names.get('ucomp', 'ucomp')]
    v = d[field_names.get('vcomp', 'vcomp')]
    t = d[field_names.get('temp', 'temp')]
    p = get_pressure(t)
    if u.indexes.keys() != ['time', p.name, 'lat', 'lon']:
        # data is in the wrong order, reorganise
        u = u.transpose('time', p.name, 'lat', 'lon')
        v = v.transpose('time', p.name, 'lat', 'lon')
        t = t.transpose('time', p.name, 'lat', 'lon')
    th = theta(d)
    lat = u.lat.data
    lon = u.lon.data
    nt, nz, ny, nx = u.data.shape
    rel_vort = _epv.rel_vort(u.data, v.data, lat*rad, lon*rad, nt, nz, ny, nx)
    e = _epv.epv(u, v, th, rel_vort, p, lat*rad, lon*rad, nt, nz, ny, nx)
    epv = xarray.DataArray(e, coords=u.coords, name='ertelPV')
    return epv



if __name__ == '__main__':
    # example calculating EPV for a GFDL dataset
    d = xarray.open_dataset('/scratch/jp492/gfdl_data/ref_earth/ref_earth_grey/run20/daily.nc',
        decode_times=False)
    d['epv'] = ertelPV(d)
    print d.epv
    d.close()