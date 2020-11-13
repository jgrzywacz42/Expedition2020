import os
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cmocean
import gsw
from seabird.cnv import fCNV

def cast_to_xarray(file, stnno):
    cast = fCNV(file)
    
    # get data from cnv file
    depth    = cast['DEPTH']
    temperature = cast['TEMP']
    salinity    = cast['PSAL']
    fluorescence = cast['wetStar']
    
    # put the data in a dictionary
    datadic = { 'depth' : depth, 'temperature' : temperature,
               'salinity' : salinity, 'fluorescence' : fluorescence}
    
    # convert the dictionary to a pandas dataframe
    castdf=pd.DataFrame.from_dict(datadic)
    
    # convert pandas to xarray
    castxr = castdf.set_index('depth').to_xarray()
    
    castxr = castxr.assign_coords({'latitude': xr.DataArray(cast.attributes['LATITUDE']),
                                   'longitude' : xr.DataArray(cast.attributes['LONGITUDE']),
                                 'station':stnno})
    
    return castxr