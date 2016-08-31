import numpy as np
import scipy.signal
import scipy.interpolate
import xarray as xr

from .util import rng


def resample_latlon(field, nlat=None, nlon=None, lats=None, lons=None, method='interpolate'):
    if nlat is None:
        nlat = len(field.coords['lat'])//2
    if nlon is None:
        nlon = len(field.coords['lon'])//2
    dims = field.coords.dims
    ilat = dims.index('lat')
    ilon = dims.index('lon')
    lat = field.coords['lat'].values
    lon = field.coords['lon'].values
    if lats is None:
        minlat, maxlat = rng(lat)
        newlat = np.linspace(minlat, maxlat, nlat)
    else:
        newlat = np.asarray(lats)
    if lons is None:
        minlon, maxlon = rng(lon)
        newlon = np.linspace(minlon, maxlon, nlon)
    else:
        newlon = np.asarray(lons)
    if method == 'interpolate':
        # resample lon form in fourier space
        lon_scale, newlon = scipy.signal.resample(field.values, nlon, t=lon, axis=ilon)
        # resample lat using interpolator
        f = scipy.interpolate.interp1d(field.coords['lat'].values, lon_scale, axis=ilat)
        rescaled = f(newlat)
        newcoords = [field.coords[d].values for d in dims]
        newcoords[ilat] = newlat
        newcoords[ilon] = newlon
        return xr.DataArray(rescaled, coords=newcoords, dims=dims, name=field.name)
    elif method == 'nearest':
        rescaled = field.sel(lat=newlat, lon=newlon, method='nearest')
        return rescaled
    else:
        raise AttributeError('unknown resampling method %r' % method)