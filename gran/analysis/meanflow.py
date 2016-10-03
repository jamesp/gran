def mean_and_eddy(field, dim='lon'):
    """Decompose a field into it's averaged mean state and an eddy."""
    mean = field.mean(dim)
    return mean, field - mean


def eddy_kinetic_energy(u, v):
    """Calculate the total Eddy Kinetic Energy, per unit area of surface"""
    pcoord = 'pfull' if 'pfull' in u.dims else 'phalf'
    ubar, uprime = mean_and_eddy(u)
    vbar, vprime = mean_and_eddy(v)
    eke = 0.5*(uprime**2 + vprime**2).sum(pcoord)
    eke.name = 'eke'
    #eke.long_name = 'eddy kinetic energy'
    return eke
