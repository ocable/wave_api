import requests
import re
import matplotlib.pyplot as plt
import datetime
from pytz import timezone


portlandBuoyID = 44007



def parse_GFS_model(bull_file):
    entries = []
    tz = timezone('US/Eastern')

    if bull_file.status_code == 200:
        raw_data = bull_file.text.split('\n')

        for i in range(7, len(raw_data) - 9):

            first_line = re.findall(r'\d+\.\d+|\d+', raw_data[i])

            if len(first_line) == 4:
                 
                day = first_line[0]
                hour = first_line[1]
                significant_wave_height = first_line[2]
                num_swell_components = first_line[3]

                dict = { "timestamp": datetime.datetime.now(tz), "day": day, "hour": hour, "significant_wave_height": significant_wave_height, "num_swell_components": num_swell_components }

                entries.append(dict)



            elif len(first_line) == 7:
                 
                day = first_line[0]
                hour = first_line[1]
                significant_wave_height = first_line[2]
                num_swell_components = first_line[3]
                comp1_height = first_line[4]
                comp1_period = first_line[5]
                comp1_dir = first_line[6]

                dict = { "timestamp": datetime.datetime.now(tz), "day": day, "hour": hour, "significant_wave_height": significant_wave_height, "num_swell_components": num_swell_components, "comp1_height": comp1_height, "comp1_period": comp1_period, "comp1_dir": comp1_dir }

                entries.append(dict)
            
            elif len(first_line) == 10:
                 
                day = first_line[0]
                hour = first_line[1]
                significant_wave_height = first_line[2]
                num_swell_components = first_line[3]
                comp1_height = first_line[4]
                comp1_period = first_line[5]
                comp1_dir = first_line[6]
                comp2_height = [7]
                comp2_period = [8]
                comp2_dir = [9]

                dict = { "timestamp": datetime.datetime.now(tz), "day": day, "hour": hour, "significant_wave_height": significant_wave_height, "num_swell_components": num_swell_components, "comp1_height": comp1_height, "comp1_period": comp1_period, "comp1_dir": comp1_dir, "comp2_height": comp2_height, "comp2_period": comp2_period, "comp2_dir": comp2_dir }

                entries.append(dict)

            else:
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

                dict = { "timestamp": datetime.datetime.now(tz), "day": day, "hour": hour, "significant_wave_height": significant_wave_height, "num_swell_components": num_swell_components, "comp1_height": comp1_height, "comp1_period": comp1_period, "comp1_dir": comp1_dir, "comp2_height": comp2_height, "comp2_period": comp2_period, "comp2_dir": comp2_dir, "comp3_height": comp3_height, "comp3_period": comp3_period, "comp3_dir": comp3_dir }

                entries.append(dict)
                 

    else:
        print(f"Request failed with status code {bull_file.status_code}")

    return entries
