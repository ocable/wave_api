import math
import datetime
from pytz import timezone




def wave_energy(period, height):
    # Density of seawater
    density = 1028.13

    # Gravity
    gravity = 9.81

    # Energy in Joules
    energy_joules = (1 / (16 * math.pi)) * density * gravity**2 * height**2 * period**2

    # Energy in kJ
    energy_kj = energy_joules / 1000

    return energy_kj




def UTC_datetime():
    cycle = 00
    current_date_utc = datetime.datetime.now(timezone('US/Eastern'))
    # Format the date in YYYYMMDD format
    formatted_date_utc = current_date_utc.strftime("%Y%m%d")
    time = int(current_date_utc.strftime("%H%M%S"))

    if time < 93000:
        cycle = "00"
    elif time > 93000 and time < 153100:
        cycle = "06"
    elif time > 153100 and time < 213600:
        cycle = "12"
    else:
        cycle = "18"

    return formatted_date_utc, cycle

