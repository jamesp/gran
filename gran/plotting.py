import os
import warnings

import numpy as np
import matplotlib.pyplot as plt
from xarray.plot.utils import _load_default_cmap

from execlim.util import nearest_val, absmax

seq_cmap = _load_default_cmap()
div_cmap = plt.cm.RdBu_r

def neutral_levels(array, nlevels=13, zero_fac=0.05, max_fac=0.95):
    """Create a set of colour levels with a white region +/-zero_fac*100% either side of zero.
        `zero_fac` sets the extent of the white region either side of zero as a fraction of the array max.
        `max_fac` sets the extent of the levels as a fraction of the array max.
        """
    m = absmax(array.values)
    nlev = (nlevels-1)//2
    levels = np.concatenate([np.linspace(-max_fac, -zero_fac, nlev), np.linspace(zero_fac, max_fac, nlev)])
    return levels*m

def sensible_tick_labels(levels, numticks=9):
    """Create nicely-rounded tick values given a set of colour levels."""
    rounders = [1, 2, 3, 5, 10]
    levels = np.asarray(levels)
    erp = np.ceil(np.log10(absmax(levels))) - 1
    mul = nearest_val(absmax(levels*10**(-erp)), [1,2,3,5,10])
    return np.linspace(-1, 1, numticks)*(10**erp)*mul

def plot_matrix(rows, cols, plot_fn,
                    figsize=(12, 12),
                    labelpad=5,
                    col_label='{}',
                    row_label='{}'):
    """Plot a two-dimensional matrix of charts, each chart generated
    by the plot_fn(row, col, ax) function."""
    nr = len(rows)
    nc = len(cols)
    fig, axs = plt.subplots(nr, nc)
    fig.set_figwidth(figsize[0])
    fig.set_figheight(figsize[1])

    for ax, col in zip(axs[0], cols):
        ax.annotate(col_label.format(col), xy=(0.5, 1), xytext=(0, labelpad),
                    xycoords='axes fraction', textcoords='offset points',
                    size='large', ha='center', va='baseline')

    for ax, row in zip(axs[:,0], rows):
        ax.annotate(row_label.format(row), xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - labelpad, 0),
                    xycoords=ax.yaxis.label, textcoords='offset points',
                    size='large', ha='right', va='center')

    for i, r in enumerate(rows):
        for k, c in enumerate(cols):
            ax = axs[i][k]
            plotted = plot_fn(row=r, col=c, ax=ax)
            if plotted is False:
                # no data, hide the axes set
                ax.set_axis_off()
                ax.set_frame_on(False)
    return fig, axs

def plot_lat_press(array, ax, divergent=True):
    """Plot latitude-pressure for a given array onto given axes."""
    k = [k for k in array.dims if k not in ('pfull', 'lat')]
    if k:
        # reduce the other coordinates
        dat = array.mean(k).load()
    else:
        dat = array.load()

    if divergent:
        lev = neutral_levels(dat, nlevels=15, max_fac=1.0, zero_fac=0.05)
        cmap = div_cmap
    else:
        lev = 15
        cmap = seq_cmap

    p = dat.plot.contourf(x='lat', y='pfull', levels=lev, ax=ax)

    if divergent:
        p.colorbar.set_ticks(sensible_tick_labels(lev, numticks=7))
    p.colorbar.set_label('')
    ax.set_yscale('log')
    ax.set_ylim(dat.pfull.max(), dat.pfull.min())
    ax.set_xlabel('')
    ax.set_ylabel('')

def plot_lat_lon(array, ax, divergent=True):
    k = [k for k in array.dims if k not in ('lon', 'lat')]
    if k:
        # reduce the other coordinates
        dat = array.mean(k).load()
    else:
        dat = array.load()

    if divergent:
        lev = neutral_levels(dat, nlevels=15, max_fac=1.0, zero_fac=0.05)
        cmap = div_cmap
    else:
        lev = 15
        cmap = seq_cmap

    p = dat.plot.contourf(x='lon', y='lat', levels=lev, ax=ax, cmap=cmap)

    if divergent:
        p.colorbar.set_ticks(sensible_tick_labels(lev, numticks=7))
    p.colorbar.set_label('')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_yticks([-90, -45, -30, 0, 30, 45, 90])



def save_figure(fig, filename, overwrite=False):
    if os.path.isfile(filename) and not overwrite:
        warnings.warn("File %r already exists. Not overwriting" % filename)
    else:
        fig.savefig(filename, bbox_inches='tight')