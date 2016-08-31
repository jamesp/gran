def get_pressure(phi):
    """Return the pressure coordinate of a variable."""
    if 'pfull' in phi.coords.keys():
        p = phi.pfull
    else:
        p = phi.phalf
    return p