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
