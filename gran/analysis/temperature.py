import xarray as xr

def temp_gradient(temp, eq_lat=10, pole_lat=80):
    """Calculate the temperature gradient from equator to pole."""
    pole_temp = temp.where(np.abs(temp.lat) > pole_lat).mean(('lat'))
    eq_temp   = temp.where(np.abs(temp.lat) < eq_lat).mean(('lat'))
    return eq_temp - pole_temp

def calc_hotspot(data):
    """Calculate the longitude of the equatorial hotspot."""
    # get the equator temperature
    tsurf = data.temp.sel(pfull=data.pfull.max(), lat=slice(-5,5)).mean('lat')
    # find the longitude of max temperature
    hotlon = data.lon.isel(lon=tsurf.argmax('lon')).values
    # map hotlon back onto  time axis
    hotlon = xr.DataArray(hotlon, coords={'time': data.time}, name='hotspot (deg. East)')
    return hotlon

