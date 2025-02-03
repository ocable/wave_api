import time
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from rich import print
import numpy as np
import datetime

from flask_apscheduler import APScheduler


from peak_detect import peakdet
from tools import wave_energy

from spectral_data import get_spectral_data as fetch_spectral_data
from spectral_data import swell_components as fetch_swell_components
from spectral_data import freqDirection as fetch_direction_data
from spectral_data import wave_summary as fetch_wave_summary
from weather_data import get_weather_data as fetch_weather_data
from wind_data import main as fetch_wind_data
from meterological_data import get_meteorological_data as fetch_meteorological_data
from GFS_model import parse_GFS_model as fetch_GFS_model
from tools import UTC_datetime

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    JSON_SORT_KEYS = False


app = Flask(__name__)
app.config.from_object(Config())
CORS(app)

 # Initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# NBDC Buoy ID
portlandBuoyID = 44007

# Global variable to store GFS model
# date, cycle = UTC_datetime()
# print(date, cycle)
# bull_file = requests.get(f'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{cycle}/wave/station/bulls.t{cycle}z/gfswave.{portlandBuoyID}.bull')
# global GFS_model
# GFS_model = fetch_GFS_model(bull_file



#Scheduler to fetch GFS model data
@scheduler.task('interval', id='fetch_GFS_forecast', seconds=90, misfire_grace_time=900)
def gfsJob():
    date, cycle = UTC_datetime()
    bull_file = requests.get(f'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{cycle}/wave/station/bulls.t{cycle}z/gfswave.{portlandBuoyID}.bull')
    global GFS_model
    GFS_model = fetch_GFS_model(bull_file)
    print("GFS fetch complete")
    # print(datetime.datetime.now())

 

# API ENDPOINTS -------->
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/spectraldata')
def get_spectral_data_route():
    # NDBC Raw Spectral Data
    raw_spectralData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.data_spec')
    # Spectral data
    seperation, densities, frequencies, periods = fetch_spectral_data(raw_spectralData)
    return {'seperation': seperation, 'densities': densities, 'frequencies': frequencies, 'periods': periods}

@app.route('/significant')
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

    return {'sig_wave_height': sig_wave_height, 'period': sig_period, 'direction': primaryDirection, 'density': density, 'energy': sig_wave_energy}

@app.route('/swellcomponents')
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
    return jsonify(components_dicts)

@app.route('/wind')
def get_wind_data_route():
    # Wind data
    wind_data = fetch_wind_data()

    wind_dicts = [wind.to_dict() for wind in wind_data]
    return jsonify(wind_dicts)

@app.route('/weather')
def get_weather_data_route():
    # Weather.gov Data
    raw_weatherData = requests.get(f'https://api.weather.gov/gridpoints/GYX/76,54/forecast')

    # Weather live/forecast
    weather_data = fetch_weather_data(raw_weatherData)


    weather_dicts = [weather.to_dict() for weather in weather_data]
    return jsonify(weather_dicts)

@app.route('/meteorological')
def get_meteorogical_data_route():
    # NDBC Raw Meteorological Buoy Data
    raw_meteorogicalData = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{portlandBuoyID}.txt')

    # Meteorological buoy data
    wind_direction, wind_speed, gust, significant_wave_height, dominant_wave_period, average_wave_period, dominant_wave_direction, sea_level_pressure, air_temperature, sea_surface_temperature, dewpoint, visibility = fetch_meteorological_data(raw_meteorogicalData)

    return {'wind_direction': wind_direction, 'wind_speed': wind_speed, 'gust': gust, 'significant_wave_height': significant_wave_height, 'dominant_wave_period': dominant_wave_period, 'average_wave_period': average_wave_period, 'dominant_wave_direction': dominant_wave_direction, 'sea_level_pressure': sea_level_pressure, 'air_temperature': air_temperature, 'sea_surface_temperature': sea_surface_temperature, 'dewpoint': dewpoint, 'visibility': visibility}




@app.route('/GFS')
def get_GFS_model_route():
    return jsonify(GFS_model)

if __name__ == "__main__":
    app.run() 

