import requests
import re
import math
from peak_detect import peakdet
import numpy as np
from tools import wave_energy

class SwellComponent:
    def __init__(self, wave_height, wave_height_trapz, period, max_energy, frequency_index, angle, energy):
        self.wave_height = wave_height
        self.wave_height_trapz = wave_height_trapz
        self.period = period
        self.max_energy = max_energy
        self.frequency_index = frequency_index
        self.angle = angle
        self.energy = energy

    def to_dict(self):
        return {
            "wave_height": self.wave_height,
            "wave_height_trapz": self.wave_height_trapz,
            "period": self.period,
            "max_energy": self.max_energy,
            "frequency_index": self.frequency_index,
            "angle": self.angle,
            "energy": self.energy
        }



# Parses Raw Spectral Data from NDBC request
def get_spectral_data (raw_spectralData): 
    
    if raw_spectralData.status_code == 200:
        #splits raw_spectralData by line
        raw_data = raw_spectralData.text.split('\n')

        # Exctracts first number with decimal point (seperation freq)
        seperation = re.findall(r'\d+\.\d+', raw_data[1])[0]

        all_nums = re.findall(r'\d+\.\d+(?!\s*\(\d+\.\d+\))', raw_data[1])[1:]

        frequencies = re.findall(r'\(([^)]+)\)', raw_data[1])

        densities = []

        for i, num in enumerate(all_nums):
            if i % 2 == 0:
                densities.append(float(num))


        frequencies = [float(frequency) for frequency in frequencies]
        periods = [1 / float(frequency) for frequency in frequencies]

    else:
        print(f"Request failed with status code {raw_spectralData.status_code}")

    return seperation, densities, frequencies, periods


# Direction data
def freqDirection (raw_directionalData, frequencies):
    if raw_directionalData.status_code == 200:
        #splits raw_spectralData by line
        raw_data = raw_directionalData.text.split('\n')

        all_nums = re.findall(r'\d+\.\d+', raw_data[1])

        freqs = re.findall(r'\(([^)]+)\)', raw_data[1])

        directions = []

        for i, num in enumerate(all_nums):
            if i % 2 == 0:
                directions.append(float(num))



    return directions


# Outputs wave summary data
def wave_summary(frequencies, densities, directions):

    max_energy_index = -1
    max_energy = -1.0
    zero_moment = 0.0

    for i in range(0, len(frequencies)):
        bandwidth = 0.01
        if i > 0:
            bandwidth = abs(frequencies[i] - frequencies[i-1])
        else:
            bandwidth = abs(frequencies[i+1] - frequencies[i])

        zero_moment += densities[i] * bandwidth

        if densities[i] > max_energy:
            max_energy = densities[i]
            max_energy_index = i

    wave_height = (4.0 * math.sqrt(zero_moment)) * 3.280839895
    period = 1.0 / frequencies[max_energy_index]
    primaryDirection = directions[max_energy_index]
    density = densities[max_energy_index]
    # primary_swell.compass_direction = degree_to_direction(primary_swell.direction)

    
    return wave_height, period, zero_moment, max_energy_index, primaryDirection, density





# Outputs swell component data
def swell_components(frequencies, densities, directions, min_indexes, min_values, max_indexes, max_values):


    components = []
    prev_index = 0

    for i in range(0, len(max_values)):
        min_index = prev_index
        if i >= len(min_indexes):
            min_index = len(frequencies)
        else:
            min_index = min_indexes[i]

        zero_moment = 0.0
        for j in range(prev_index, min_index):
            bandwidth = 0.01
            if j > 0:
                bandwidth = abs(frequencies[j] - frequencies[j-1])
            else:
                bandwidth = abs(frequencies[j+1] - frequencies[j])

            zero_moment += densities[j] * bandwidth

            # zero moment of component with intergral over range given by peak detect
            zero_trapz = np.trapz(densities[prev_index:min_index], frequencies[prev_index:min_index])

        
        wave_height = (4.0 * math.sqrt(zero_moment)) * 3.280839895
        wave_height_metric = 4.0 * math.sqrt(zero_moment)
        wave_height_trapz = (4.0 * math.sqrt(zero_trapz)) * 3.280839895
        period = 1.0 / frequencies[max_indexes[i]]
        angle = directions[max_indexes[i]]
        max_energy = max_values[i]
        frequency_index = max_indexes[i]
        energy = wave_energy(period, wave_height_metric)

        component = SwellComponent(wave_height, wave_height_trapz, period, max_energy, frequency_index, angle, energy)

        components.append(component)

        prev_index = min_index

    components.sort(key=lambda x: x.max_energy, reverse=True)

    return components