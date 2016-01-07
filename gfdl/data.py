# A collection of helpers for joining and analysing GFDL data output

import glob
import os

import pandas as pd
import numpy as np
import xray

P = os.path.join

def read_namelist(namelist):
    import f90nml
    return f90nml.read(namelist)


def join_datasets(datasets, fields=None, avg_over=None):
    """Concatenate a set of monthly datasets.
        datasets: A list or generator of datasets.
        fields:  Choose a subset of fields. (For large datasets, if you do not choose a limited
            number of fields, RAM usage grows to become untenable.)
        avg_over: Reduce the dataset size by averaging over a chosen dimension e.g. `('lon', 'lonb')`
            will average all fields by longitude
    """
    ext_data = []
    for d in datasets:
        d.load()
        if fields:
            drop_fields = [f for f in d.data_vars.keys() if f not in fields]
            d = d.drop(drop_fields)
        if avg_over:
            d = d.mean(avg_over)
        ext_data.append(d)

    if avg_over and 'time' in avg_over:
        # the time dimension has been reduced, replace with 'month' dimension
        dim = pd.Index(range(1, len(ext_data)+1), name='month')
    else:
        dim = 'time'
    return xray.concat(ext_data, dim=dim)

def get_run_filenames(data_path, dirglob='run*', filename='atmos_daily.nc'):
    """Creates a list of run files from a data directory."""
    matches = sorted(glob.glob(P(data_path, dirglob)))
    for m in matches:
        if os.path.isdir(m):
            f = P(m, filename)
            yield f

def datasets(filenames):
    """Iterate over a list of datasets."""
    for f in filenames:
        with xray.open_dataset(f, decode_times=False) as data:
            data.filename = f
            yield data
            data.close()
