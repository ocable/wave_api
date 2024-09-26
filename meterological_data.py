

# Parses Raw Meteorogical Data from NDBC request

def get_meteorological_data (raw_meteorogicalData):
    if raw_meteorogicalData.status_code == 200:
        raw_data = raw_meteorogicalData.text.split('\n')
        current_data = raw_data[3].split()

        wind_direction = current_data[5]
        wind_speed = current_data[6]
        gust = current_data[7]
        significant_wave_height = current_data[8]
        dominant_wave_period = current_data[9]
        average_wave_period = current_data[10]
        dominant_wave_direction = current_data[11]
        sea_level_pressure = current_data[12]
        air_temperature = current_data[13]
        sea_surface_temperature = current_data[14]
        dewpoint = current_data[15]
        visibility = current_data[16] # limited from 0 to 1.6 nmi

    else: 
        print(f"Request failed with status code {raw_meteorogicalData.status_code}")

    return wind_direction, wind_speed, gust, significant_wave_height, dominant_wave_period, average_wave_period, dominant_wave_direction, sea_level_pressure, air_temperature, sea_surface_temperature, dewpoint, visibility

