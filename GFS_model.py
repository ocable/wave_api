import requests
import re
import matplotlib.pyplot as plt
import datetime
from pytz import timezone


portlandBuoyID = 44007





class GFS_forecast_hour:
    def __init__(self, cycle, day, hour, significant_wave_height, num_swell_components, comp1_height, comp1_period, comp1_dir, comp2_height, comp2_period, comp2_dir, comp3_height, comp3_period, comp3_dir):
        self.cycle = cycle
        self.day = day
        self.hour = hour
        self.significant_wave_height = significant_wave_height
        self.num_swell_components = num_swell_components
        self.comp1_height = comp1_height
        self.comp1_period = comp1_period
        self.comp1_dir = comp1_dir
        self.comp2_height = comp2_height
        self.comp2_period = comp2_period
        self.comp2_dir = comp2_dir
        self.comp3_height = comp3_height
        self.comp3_period = comp3_period
        self.comp3_dir = comp3_dir

    def to_dict(self):
        return {
            "cycle": self.cycle,
            "day": self.day,
            "hour": self.hour,
            "significant_wave_height": self.significant_wave_height,
            "num_swell_components": self.num_swell_components,
            "comp1_height": self.comp1_height,
            "comp1_period": self.comp1_period,
            "comp1_dir": self.comp1_dir,
            "comp2_height": self.comp2_height,
            "comp2_period": self.comp2_period,
            "comp2_dir": self.comp2_dir,
            "comp3_height": self.comp3_height,
            "comp3_period": self.comp3_period,
            "comp3_dir": self.comp3_dir
        }


entries = []


def parse_GFS_model(bull_file):
    cycle = 00
    current_date_utc = datetime.datetime.now(timezone('US/Eastern'))
    # Format the date in YYYYMMDD format
    time = int(current_date_utc.strftime("%H%M%S"))

    if time < 93000:
        cycle = 0
    elif time > 93000 and time < 153100:
        cycle = 6
    elif time > 153100 and time < 213600:
        cycle = 12
    else:
        cycle = 18
    
    if bull_file.status_code == 200:
        raw_data = bull_file.text.split('\n')

        for i in range(7, len(raw_data) - 9):

            first_line = re.findall(r'\d+\.\d+|\d+', raw_data[i])

            if len(first_line) == 4:
                cycle = cycle
                day = first_line[0]
                hour = first_line[1]
                significant_wave_height = first_line[2]
                num_swell_components = first_line[3]
                comp1_height = []
                comp1_period = []
                comp1_dir = []
                comp2_height = []
                comp2_period = []
                comp2_dir = []
                comp3_height = []
                comp3_period = []
                comp3_dir = []

                entry = GFS_forecast_hour(cycle, day, hour, significant_wave_height, num_swell_components, comp1_height, comp1_period, comp1_dir, comp2_height, comp2_period, comp2_dir, comp3_height, comp3_period, comp3_dir)

                entries.append(entry)



            elif len(first_line) == 7:
                cycle = cycle
                day = first_line[0]
                hour = first_line[1]
                significant_wave_height = first_line[2]
                num_swell_components = first_line[3]
                comp1_height = first_line[4]
                comp1_period = first_line[5]
                comp1_dir = first_line[6]
                comp2_height = []
                comp2_period = []
                comp2_dir = []
                comp3_height = []
                comp3_period = []
                comp3_dir = []

                entry = GFS_forecast_hour(cycle, day, hour, significant_wave_height, num_swell_components, comp1_height, comp1_period, comp1_dir, comp2_height, comp2_period, comp2_dir, comp3_height, comp3_period, comp3_dir)

                entries.append(entry)
            
            elif len(first_line) == 10:
                cycle = cycle
                day = first_line[0]
                hour = first_line[1]
                significant_wave_height = first_line[2]
                num_swell_components = first_line[3]
                comp1_height = first_line[4]
                comp1_period = first_line[5]
                comp1_dir = first_line[6]
                comp2_height = []
                comp2_period = []
                comp2_dir = []
                comp3_height = []
                comp3_period = []
                comp3_dir = []

                entry = GFS_forecast_hour(cycle, day, hour, significant_wave_height, num_swell_components, comp1_height, comp1_period, comp1_dir, comp2_height, comp2_period, comp2_dir, comp3_height, comp3_period, comp3_dir)

                entries.append(entry)

            else:
                cycle = cycle
                day = first_line[0]
                hour = first_line[1]
                significant_wave_height = first_line[2]
                num_swell_components = first_line[3]
                comp1_height = first_line[4]
                comp1_period = first_line[5]
                comp1_dir = first_line[6]
                comp2_height = first_line[7]
                comp2_period = first_line[8]
                comp2_dir = first_line[9]
                comp3_height = first_line[10]
                comp3_period = first_line[11]
                comp3_dir = first_line[12]

                entry = GFS_forecast_hour(cycle, day, hour, significant_wave_height, num_swell_components, comp1_height, comp1_period, comp1_dir, comp2_height, comp2_period, comp2_dir, comp3_height, comp3_period, comp3_dir)

                entries.append(entry)
                 

    else:
        print(f"Request failed with status code {bull_file.status_code}")

    return entries