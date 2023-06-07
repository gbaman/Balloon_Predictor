# Balloon burst calculator
# Based off https://github.com/projecthorus/cusf-burst-calc/blob/master/js/calc.js

import math
from enum import Enum


class GasEnum(Enum):
    HE = 0.1786
    H = 0.0899
    CH4 = 0.6672
    BOC = 0.21076


class Balloon:
    def __init__(self, name, burst_diameter, cd, standard=True):
        self.name = name
        self.burst_diameter = burst_diameter
        self.cd = cd
        self.standard = standard


class BalloonEnum(Enum):
    K200 = Balloon("K200", 3.00, 0.25)
    K300 = Balloon("K300", 3.78, 0.25)
    K350 = Balloon("K350", 4.12, 0.25)
    K450 = Balloon("K450", 4.72, 0.25)
    K500 = Balloon("K500", 4.99, 0.25)
    K600 = Balloon("K600", 6.02, 0.30)
    K700 = Balloon("K700", 6.53, 0.30)
    K800 = Balloon("K800", 7.00, 0.30)
    K1000 = Balloon("K1000", 7.86, 0.30)
    K1200 = Balloon("K1200", 8.63, 0.25)
    K1500 = Balloon("K1500", 9.44, 0.25)
    K2000 = Balloon("K2000", 10.54, 0.25)
    K3000 = Balloon("K3000", 13.00, 0.25)
    H100 = Balloon("H100", 2.00, 0.25, False)
    H200 = Balloon("H200", 3.00, 0.25)
    H300 = Balloon("H300", 3.80, 0.25, False)
    H350 = Balloon("H350", 4.10, 0.25)
    H400 = Balloon("H400", 4.50, 0.25, False)
    H500 = Balloon("H500", 5.00, 0.25, False)
    H600 = Balloon("H600", 5.80, 0.30)
    H750 = Balloon("H750", 6.50, 0.30, False)
    H800 = Balloon("H800", 6.80, 0.30)
    H950 = Balloon("H950", 7.20, 0.30, False)
    H1000 = Balloon("H1000", 7.50, 0.30)
    H1200 = Balloon("H1200", 8.50, 0.25, False)
    H1500 = Balloon("H1500", 9.50, 0.25, False)
    H1600 = Balloon("H1600", 10.50, 0.25, False)
    H2000 = Balloon("H2000", 11.00, 0.25, False)
    H3000 = Balloon("H3000", 12.50, 0.25, False)
    P100 = Balloon("P100", 1.6, 0.25)
    P350 = Balloon("P350", 4.0, 0.25)
    P600 = Balloon("P600", 5.8, 0.30)
    P800 = Balloon("P800", 6.6, 0.30)
    P900 = Balloon("P900", 7.0, 0.30)
    P1200 = Balloon("P1200", 8.0, 0.25)
    P1600 = Balloon("P1600", 9.5, 0.25)
    P2000 = Balloon("P2000", 10.2, 0.25)


def find_rho_g(gas):
    rho_g = 0

    if gas == 'he':
        rho_g = 0.1786
    elif gas == 'h':
        rho_g = 0.0899
    elif gas == 'ch4':
        rho_g = 0.6672
    elif gas == 'boc':
        rho_g = 0.21076
    return rho_g


def calc_update(balloon: BalloonEnum, payload_mass_g, target_ascent_rate=None, target_burst_altitude=None, gas="he", air_density=1.2050, air_density_model=7238.3, gravitational_acceleration=9.80665):

    # Get input values and check them
    mp_set = 0
    tar_set = False
    tba_set = False
    warnings = []
    if target_ascent_rate:
        tar_set = True
    elif target_burst_altitude:
        tba_set = True
    else:
        raise Exception("Target burst or target_ascent rate must be set!")

    # Get constants and check them
    gas_density = find_rho_g(gas)
    balloon_diameter = balloon.value.burst_diameter
    balloon_cd = balloon.value.cd
    balloon_name = balloon.value.name

    #if sanity_check_constants(gas_density, air_density, air_density_model, Gravitational_acceleration, balloon_diameter, balloon_cd):
    #    return

    # Do some maths
    balloon_name = float(balloon_name[1:]) / 1000.0
    payload_mass_g = payload_mass_g / 1000.0

    ascent_rate = 0
    burst_altitude = 0
    time_to_burst = 0
    neck_lift = 0
    launch_radius = 0
    launch_volume = 0

    burst_volume = (4.0/3.0) * math.pi * math.pow(balloon_diameter / 2.0, 3)

    if tba_set:
        launch_volume = burst_volume * math.exp((-target_burst_altitude) / air_density_model)
        launch_radius = math.pow((3*launch_volume)/(4*math.pi), (1/3))
    elif tar_set:
        a = gravitational_acceleration * (air_density - gas_density) * (4.0 / 3.0) * math.pi
        b = -0.5 * math.pow(target_ascent_rate, 2) * balloon_cd * air_density * math.pi
        c = 0
        d = - (payload_mass_g + balloon_name) * gravitational_acceleration

        f = (((3*c)/a) - (math.pow(b, 2) / math.pow(a,2)) / 3.0)
        g = (((2*math.pow(b,3))/math.pow(a,3)) -
             ((9*b*c)/(math.pow(a,2))) + ((27*d)/a)) / 27.0
        h = (math.pow(g,2) / 4.0) + (math.pow(f,3) / 27.0)

        if h <= 0:
            raise Exception("expect exactly one real root")

        R = (-0.5 * g) + math.sqrt(h)
        S = math.pow(R, 1.0/3.0)
        T = (-0.5 * g) - math.sqrt(h)
        U = math.pow(T, 1.0/3.0)
        launch_radius = (S+U) - (b/(3*a))

    launch_area = math.pi * math.pow(launch_radius, 2)
    launch_volume = (4.0/3.0) * math.pi * math.pow(launch_radius, 3)
    density_difference = air_density - gas_density
    gross_lift = launch_volume * density_difference
    neck_lift = (gross_lift - balloon_name) * 1000
    total_mass = payload_mass_g + balloon_name
    free_lift = (gross_lift - total_mass) * gravitational_acceleration
    ascent_rate = math.sqrt(free_lift / (0.5 * balloon_cd * launch_area * air_density))
    volume_ratio = launch_volume / burst_volume
    burst_altitude = -(air_density_model) * math.log(volume_ratio)
    time_to_burst = (burst_altitude / ascent_rate) / 60.0

    if math.isnan(ascent_rate):
        return 0, 0, 0, 0, 0, 0, 0, ["Altitude unreachable for this configuration."]

    if balloon_diameter >= 10 and ascent_rate < 4.8:
        return 0, 0, 0, 0, 0, 0, 0, ["Configuration suggests a possible floater."]

    ascent_rate = "{:.2f}".format(ascent_rate)
    burst_altitude = str(int(burst_altitude))
    time_to_burst = str(int(time_to_burst))
    neck_lift = str(int(neck_lift))
    launch_litres = "{:.0f}".format(launch_volume * 1000)
    launch_cf = "{:.1f}".format(launch_volume * 35.31)
    launch_volume = "{:.2f}".format(launch_volume)

    return ascent_rate, burst_altitude, time_to_burst, neck_lift, launch_volume, launch_litres, launch_cf, warnings