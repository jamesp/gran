import xarray as xr
import astropy.units



@xr.register_dataarray_accessor('in_units')
class UnitConverter(object):
    custom_units = {
            'hours since': 'hour',
            'days since': 'day',
            'minutes since': 'min',
            'seconds since': 's',
            'degrees_E': 'deg'}

    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        u = xarray_obj.attrs.get('units')
        if u is not None:
            u = self.parse_units(u)
        self._unit = u

    def parse_units(self, unit_string):
        u_obj = None
        try:
            u_obj = astropy.units.Unit(unit_string)
        except ValueError:
            for s in self.custom_units:
                if unit_string.startswith(s):
                    u_obj = astropy.units.Unit(self.custom_units[s])
                    break
        return u_obj

    def __call__(self, new_unit):
        if self._unit is None:
            raise ValueError("No valid units for field")
        new_unit = astropy.units.Unit(new_unit)
        factor = self._unit.to(new_unit)
        newval = self._obj*factor
        newval.attrs['units'] = new_unit.name
        return newval


# @xr.register_dataset_accessor('convert_units')
# class CoordUnitConverter(object):
#     def __init__(self, xarray_obj):
#         self._obj = xarray_obj

#     def __call__(self, **unit_mapping):
#         for field, new_unit in unit_mapping:


def normalize(field, dims):
    """Normalise a field over the range [0, 1] along given dimensions."""
    if type(dims) == str:
        dims = (dims, )
    dmax = field.max(dims)
    dmin = field.min(dims)
    return (field - dmin) / (dmax - dmin)


@xr.register_dataarray_accessor('normalize')
@xr.register_dataset_accessor('normalize')
class NormalizeDataArray(object):
    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def __call__(self, dims):
        return normalize(self._obj, dims)