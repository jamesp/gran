# A collection of helpers for joining and analysing GFDL data output

import os

import numpy as np
import xray

P = os.path.join

def read_namelist(namelist):
	import f90nml
	return dict(f90nml.read(namelist))


def run_data_list(filename, run_range, data_dir):
	"""Returns a list of files from a GFDL run that are spread over several folders.
	e.g.
	>>> run_list('atmos_daily.nc', range(15, 18), data_dir)
	['data/run15/atmos_daily.nc', 'data/run16/atmos_daily.nc', 'data/run17/atmos_daily.nc']
	"""
	return [P(data_dir, 'run%d' % n, filename) for n in run_range]


def join_datasets(filenames, fields=None, avg_over=None):
    """Concatenate a list of files into one xray dataset.
        fields:  Choose a subset of the data fields. (For large datasets, if you do not choose a limited
            number of fields, RAM usage grows to become untenable.)
        avg_over: Reduce the dataset size by averaging over a chosen dimension e.g. `('lon', 'lonb')`
            will average all fields by longitude
    """
    ext_data = []
    for m in filenames:
        run_data = xray.open_dataset(m)
        if fields:
            drop_fields = [f for f in run_data.data_vars.keys() if f not in fields]
            run_data = run_data.drop(drop_fields)
        if avg_over:
            run_data = run_data.mean(avg_over)
        ext_data.append(run_data)

    if avg_over and 'time' in avg_over:
        # the time dimension has been reduced, replace with 'month' dimension
        dim = pd.Index(name='month', data=months)
    else:
        dim = 'time'
    return xray.concat(ext_data, dim=dim)


