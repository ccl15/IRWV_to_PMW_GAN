import xarray as xr
import numpy as np
from datetime import datetime, timedelta



def load_nc(fn):
    with xr.open_dataset(fn) as ds:
        IR = ds['IR1'].values
        WV = ds['WV2'].values
        lons = ds['lon'].values
        lats = ds['lat'].values
        attrs = {}   
        attrs['TC_ID'] = ds.attrs['TC_ID'] 
        attrs['TC_lon'] = ds.attrs['TC_lon (deg)'] 
        attrs['TC_lat'] = ds.attrs['TC_lat (deg)']
        attrs['datetime'] = ds.attrs['TC_date (yymmddhh)']
        attrs['basin'] = 'WPAC'  # input nc don't have basin. Modify when processed different basin
        attrs['Vmax'] = ds.attrs['TC_Vmax (kt)']
        img = np.nan_to_num(np.dstack((IR,WV)))[np.newaxis,...]
    return img, lons, lats, attrs


def save_nc(fn, IRWV, pred, lons, lats, attrs):
    IRWV[IRWV<1] = np.nan
    ds = xr.Dataset(
        {'IR':(('lon','lat'), IRWV[...,0]),
         'WV':(('lon','lat'), IRWV[...,1]),
         'PMW85_f':(('lon','lat'), pred)
        },
        coords = {
            'lat':lats,
            'lon':lons
        },
        attrs = attrs
    )
    ds.to_netcdf(fn)
