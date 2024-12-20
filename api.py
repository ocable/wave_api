import time
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import requests
from rich import print
import numpy as np
import datetime


from peak_detect import peakdet
from tools import wave_energy
from tools import UTC_datetime


from spectral_data import get_spectral_data as fetch_spectral_data
from spectral_data import swell_components as fetch_swell_components
from spectral_data import freqDirection as fetch_direction_data
from spectral_data import wave_summary as fetch_wave_summary
from weather_data import get_weather_data as fetch_weather_data
from wind_data import main as fetch_wind_data
from meterological_data import get_meteorological_data as fetch_meteorological_data
from GFS_model import parse_GFS_model as fetch_GFS_model



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)


# NBDC Buoy ID
portlandBuoyID = 44007



# API ENDPOINTS -------->

@app.route('/time', methods=["GET"])
def get_current_time():
    return {'time': time.time()}

@app.route('/spectraldata', methods=["GET"])
def get_spectral_data_route():
    # NDBC Raw Spectral Data
    raw_spectralData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.data_spec')
    # Spectral data
    seperation, densities, frequencies, periods = fetch_spectral_data(raw_spectralData)

    response = make_response(jsonify({
        'seperation': seperation,
        'densities': densities,
        'frequencies': frequencies,
        'periods': periods
    }))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/significant', methods=["GET"])
def get_significant_wave_data():
    # NDBC Raw Spectral Data
    raw_spectralData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.data_spec')

    # NDBC Raw Directional Data
    raw_directionalData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.swdir')

    # Spectral data
    seperation, densities, frequencies, periods = fetch_spectral_data(raw_spectralData)

    # Directional data
    directions = fetch_direction_data(raw_directionalData, frequencies)

    # Wave summary
    wave_height, sig_period, zero_moment, max_energy_index, primaryDirection, density = fetch_wave_summary(frequencies, densities, directions)

    # Siginficant wave height, period, direction, enrgy
    zero_moment = np.trapezoid(densities, frequencies)
    M2 = np.trapezoid(densities * np.square(frequencies), frequencies)
    sig_wave_height_metric = (4 * np.sqrt(zero_moment))
    sig_wave_height = (4 * np.sqrt(zero_moment)) * 3.280839895
    sig_wave_energy = wave_energy(sig_period, sig_wave_height_metric)

    response = make_response(jsonify({
        'sig_wave_height': sig_wave_height,
        'period': sig_period,
        'direction': primaryDirection,
        'density': density,
        'energy': sig_wave_energy
    }))
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/swellcomponents', methods=["GET"])
def get_swell_components():
    # NDBC Raw Spectral Data
    raw_spectralData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.data_spec')

    # NDBC Raw Directional Data
    raw_directionalData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.swdir')

    # Spectral data
    seperation, densities, frequencies, periods = fetch_spectral_data(raw_spectralData)

    # Results from peak detection
    min_indexes, min_values, max_indexes, max_values = peakdet(densities, 0.05)

    # Directional data
    directions = fetch_direction_data(raw_directionalData, frequencies)

    # Swell components
    components = fetch_swell_components(frequencies, densities, directions, min_indexes, min_values, max_indexes, max_values)

    components_dicts = [component.to_dict() for component in components]

    response = make_response(jsonify(components_dicts))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/wind', methods=["GET"])
def get_wind_data_route():
    # Wind data
    wind_data = fetch_wind_data()
    wind_dicts = [wind.to_dict() for wind in wind_data]

    response = make_response(jsonify(wind_dicts))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/weather', methods=["GET"])
def get_weather_data_route():
    # Weather.gov Data
    raw_weatherData = requests.get(f'https://api.weather.gov/gridpoints/GYX/76,54/forecast')
    # Weather live/forecast
    weather_data = fetch_weather_data(raw_weatherData)
    weather_dicts = [weather.to_dict() for weather in weather_data]

    response = make_response(jsonify(weather_dicts))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/meteorological', methods=["GET"])
def get_meteorogical_data_route():
    # NDBC Raw Meteorological Buoy Data
    raw_meteorogicalData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.txt')
    # Meteorological buoy data
    wind_direction, wind_speed, gust, significant_wave_height, dominant_wave_period, average_wave_period, dominant_wave_direction, sea_level_pressure, air_temperature, sea_surface_temperature, dewpoint, visibility = fetch_meteorological_data(raw_meteorogicalData)
    
    response = make_response(jsonify({
        'wind_direction': wind_direction,
        'wind_speed': wind_speed,
        'gust': gust,
        'significant_wave_height': significant_wave_height,
        'dominant_wave_period': dominant_wave_period,
        'average_wave_period': average_wave_period,
        'dominant_wave_direction': dominant_wave_direction,
        'sea_level_pressure': sea_level_pressure,
        'air_temperature': air_temperature,
        'sea_surface_temperature': sea_surface_temperature,
        'dewpoint': dewpoint,
        'visibility': visibility
    }))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/GFS', methods=["GET"])
def get_GFS_model_route():
    # Date and cycle
    date, cycle = UTC_datetime()
    print(cycle)
    # GFS Model Data
    bull_file = requests.get(f'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{cycle}/wave/station/bulls.t{cycle}z/gfswave.{portlandBuoyID}.bull')
    # GFS Model
    GFS_model = fetch_GFS_model(bull_file)
    GFS_dicts = [GFS.to_dict() for GFS in GFS_model]

    response = make_response(jsonify(GFS_dicts))
    response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == "__main__":
    app.run()