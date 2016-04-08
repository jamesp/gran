"""Analysis of GFDL FMS output

Most analysis functions are based on the data being loaded into
python using the xarray library.

For example, opening many run files and calculating
the mass streamfunction across them:

    import xarray
    from execlim.analysis import mass_streamfunction

    filenames = ['run%d/daily.nc' for m in range(1,25)]
    d = xarray.open_dataset(filenames, chunks={'time': 10, 'lon': 128//4, 'lat': 64//2})

    d['mass_sf'] = mass_streamfunction(d)
    # plot with pressure on y axis, increasing downward
    d.mass_sf.mean('time').plot.contourf('lat', 'pfull', levels=12, yincrease=False)
"""


from execlim.analysis.util import *
from execlim.analysis.mass_streamfunction import mass_streamfunction
from execlim.analysis.epv import ertelPV