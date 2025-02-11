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

efth = np.array(densities/directions)
freq = np.array(frequencies) 
dir = np.array([0])



# # print(f"Length of efth: {len(efth)}")
# # print(f"Length of freq: {len(freq)}")
# # print(f"Length of dir: {len(dir)}")

efth_expanded = np.tile(efth[:, np.newaxis], (1, len(dir))) # Correct way to tile

efth_expanded /= len(dir)

da = xr.DataArray(
    data=np.expand_dims(efth, 1),
    dims=["freq", "dir"],
    coords=dict(freq=freq, dir=dir),
    name="efth",
)
print(da)


da.spec.hs()

dset = da.to_dataset()

dset.spec.hs()

dset.efth.spec

print(dset.spec)

ds = dset.isel(freq=slice(0, 46), dir=slice(0, 46))

ds.spec.plot(as_period=True, normalised=False, cmap="Spectral_r");
#ds.spec.plot(kind="contour", colors="#af1607", linewidths=0.5);

plt.show()


# dset = read_ndbc_ascii("44007.data_spec.txt")
# print(dset)

# dset.spec.plot(as_period=True, normalised=False, cmap="Spectral_r");
# plt.show()