import numpy as np

def absmax(x):
    """Returns the absolute maximum of x."""
    return np.max(np.abs(x))

def rng(x):
    """Returns the (min, max) range of x."""
    return np.min(x), np.max(x)

def nearest_val(x, ys):
    """Returns the value from `ys` closest to `x`."""
    ys = sorted(ys, reverse=True)
    return ys[np.argmin(np.abs(np.asarray(ys) - x))]

def rescale(p):
    pmin, pmax = np.min(p), np.max(p)
    return (p - pmin) / (pmax - pmin)

def get_pressure(phi):
    """Return the pressure coordinate of a GFDL variable."""
    if 'pfull' in phi.dims:
        p = phi.pfull
    else:
        p = phi.phalf
    return p

def normalize(field, dims):
    """Normalise a field over the range [0, 1] along given dimensions."""
    if type(dims) == str:
        dims = (dims, )
    dmax = field.max(dims)
    dmin = field.min(dims)
    return (field - dmin) / (dmax - dmin)