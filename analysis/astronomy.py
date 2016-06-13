import xarray as xr

def calc_subsolar_spot(data):
    """Calculate the longitude of the subsolar point."""
    # get the TOA SW flux over the equator
    tsurf = -data.flux_sw.sel(phalf=data.phalf.min(), lat=slice(-5,5)).mean('lat')
    # find the longitude of max temperature
    hotlon = data.lon.isel(lon=tsurf.argmax('lon')).values
    # map hotlon back onto  time axis
    hotlon = xr.DataArray(hotlon, coords={'time': data.time}, name='subsolar spot (deg. East)')
    return hotlon