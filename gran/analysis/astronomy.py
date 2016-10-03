import numpy as np
import xarray as xr

import gran.domain

def calc_subsolar_spot(data):
    """Calculate the longitude of the subsolar point."""
    # get the TOA SW flux over the equator
    tsurf = -data.flux_sw.sel(phalf=data.phalf.min(), lat=slice(-5,5)).mean('lat')
    # find the longitude of max temperature
    hotlon = data.lon.isel(lon=tsurf.argmax('lon')).values
    # map hotlon back onto  time axis
    hotlon = xr.DataArray(hotlon, coords={'time': data.time}, name='subsolar spot (deg. East)')
    return hotlon


def phase_curve(temp, domain):
    """Calculate the integrated phase curve for an exoplanet.

    Phase curve assuming we are in the equatorial plane.
    This means we sum the projection onto a circle for each longitude.

    T(lon0) = INTEGRAL[lat, lon]( T(lon - lon0) dA )

    Parameters
    ----------
    temp : xarray.DataArray
        The 2D model field of temperature. This could be
        effective temperature at TOA, outgoing radiation, or a shallow water height field.
    domain : xarray.DataSet
        The Dataset or domain.  Needed for calculating integral area.

    Returns
    -------
    phase_curve: xarray.DataArray
    The integrated emission by longitude `lon0` = lon - lon_s.
    """
    # calculate a matrix of cos(lon - lon0) for all lon0
    rad  = np.pi / 180
    radlon = domain.lon * rad
    lon0 = radlon.copy(deep=True)
    lon0.name = 'lon0'
    lon0 = lon0.rename({'lon': 'lon0'})

    plon = np.cos(radlon - lon0)
    plon.values[plon.values < 0] = 0     # adjust for max(cos(lon - lon0), 0.0)

    coslat = np.cos(domain.lat * rad)
    dA = gran.domain.calculate_dA(domain)

    pc = (temp*dA*coslat*plon).sum(('lat', 'lon'))
    return pc

def calc_phase_offset(curve):
    """Calculate the longitudinal offset of the peak of a phase curve.
    """
    mval = curve.argmax('lon0')
    v = curve.lon0.isel(lon0=mval)
    mval.values = v
    return mval
