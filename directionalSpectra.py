import numpy as np
import xarray as xr
import wavespectra
from wavespectra import read_ndbc_ascii
import requests
import matplotlib.pyplot as plt


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
dir = np.array([0])



efth = np.array(densities)
freq = np.array(frequencies)
dir = np.array(directions)

print(f"shape of efth: {efth.shape}")
print(f"shape of freq: {freq.shape}")
print(f"shape of dir: {dir.shape}")

# Ensure efth is correctly shaped
efth_expanded = np.tile(efth[:, np.newaxis], (1, len(dir))) # Correct way to tile

print(f"shape of efth_expanded: {efth_expanded.shape}") 
print(efth_expanded)

# Convert from m^2/Hz to m^2/Hz/degree
# efth_expanded /= len(dir)

da = xr.DataArray(
    data=efth_expanded,
    dims=["freq", "dir"],
    coords=dict(freq=freq, dir=dir),
    name="efth",
)


dset = da.to_dataset()


ds = dset.isel()

dset.spec.plot(as_period=True, normalised=True, cmap="Spectral_r");
#ds.spec.plot(kind="contour", colors="#af1607", linewidths=0.5);

plt.show()


# dset = read_ndbc_ascii("44007.data_spec.txt")
# print(dset)

# dset.spec.plot(as_period=True, normalised=False, cmap="Spectral_r");
# plt.show()