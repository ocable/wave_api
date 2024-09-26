import math



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




