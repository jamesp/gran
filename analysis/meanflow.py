def mean_and_eddy(field, mean_coord='lon'):
    """Decompose a field into it's longitudinally averaged mean state and an eddy."""
    mean = field.mean(mean_coord)
    return mean, field - mean

def eddy_kinetic_energy(dataset):
    """Calculate the total Eddy Kinetic Energy, per unit area of surface"""
    pcoord = 'pfull' if 'pfull' in dataset.ucomp.coords.keys() else 'phalf'
    ubar, uprime = mean_and_eddy(dataset.ucomp)
    vbar, vprime = mean_and_eddy(dataset.vcomp)
    eke = 0.5*(uprime**2 + vprime**2).sum(pcoord)
    eke.name = 'eke'
    #eke.long_name = 'eddy kinetic energy'
    return eke
