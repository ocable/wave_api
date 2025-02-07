import numpy as np
import xarray as xr
import wavespectra
import requests

from spectral_data import get_spectral_data as fetch_spectral_data
from spectral_data import freqDirection as fetch_direction_data


portlandBuoyID = 44007

# NDBC Raw Spectral Data
raw_spectralData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.data_spec')
# Spectral data
seperation, densities, frequencies, periods = fetch_spectral_data(raw_spectralData)

raw_directionalData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.swdir')
    
# Directional data der
directions, freqs = fetch_direction_data(raw_directionalData)

efth = np.array(densities)
freq = np.array(frequencies)
dir = np.array(directions)


da = xr.DataArray(
    data=np.expand_dims(efth, 1),
    dims=["freq", "dir"],
    coords=dict(freq=freq, dir=dir),
    name="efth",
)

da.spec.hs()

dset = da.to_dataset()

dset.spec.hs()

