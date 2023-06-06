import datetime
from typing import List
import random
import datetime
from dateutil import parser
import burst_calc

COLOURS = ["red", "blue", "green", "purple", "orange", "darkred", "darkblue", "darkgreen", "cadetblue", "gray", "black"]


def get_next_weather_time():
    current_time = datetime.datetime.now(datetime.timezone.utc)
    if current_time.hour > 19:
        return "Next weather at "


class FlightManual():
    def __init__(self, launch_site, burst_altitude, ascent_rate, descent_rate, launch_datetime, balloon_size, notes=""):
        self.launch_site = launch_site[0]
        self.launch_latitude = launch_site[1]
        self.launch_longitude = launch_site[2]
        self.burst_altitude = burst_altitude
        self.ascent_rate = ascent_rate
        self.descent_rate = descent_rate
        self.launch_datetime = launch_datetime
        self.launch_datetime_obj = parser.parse(launch_datetime)
        self.launch_site_name = launch_site[0]
        self.markers: List[LocationMarker] = []
        self.burst_marker : LocationMarker = None
        self.balloon_size = balloon_size
        self.error = None
        self.marker_colour = random.choice(COLOURS)
        self.line_colour = random.choice(list(set(COLOURS) - set(self.marker_colour)))
        self.notes = notes
        self.landing_time = ""


class FlightBalloon():
    def __init__(self, launch_site, balloon: burst_calc.BalloonEnum, payload_mass, descent_rate, launch_datetime, notes="", target_burst_altitude=None, target_ascent_rate=None):
        ascent_rate, burst_altitude, time_to_burst, neck_lift, launch_volume, launch_litres, launch_cf, warnings = burst_calc.calc_update(balloon, payload_mass, target_ascent_rate, target_burst_altitude)
        self.launch_site = launch_site[0]
        self.launch_latitude = launch_site[1]
        self.launch_longitude = launch_site[2]
        self.burst_altitude = burst_altitude
        self.ascent_rate = ascent_rate
        self.descent_rate = descent_rate
        self.launch_datetime = launch_datetime
        self.launch_datetime_obj = parser.parse(launch_datetime)
        self.launch_site_name = launch_site[0]
        self.markers: List[LocationMarker] = []
        self.burst_marker : LocationMarker = None
        self.balloon_size = balloon.value.name
        self.error = None
        self.marker_colour = random.choice(COLOURS)
        self.line_colour = random.choice(list(set(COLOURS) - set(self.marker_colour)))
        self.notes = notes
        self.landing_time = ""



class LocationMarker():
    def __init__(self, data, launch_details: FlightManual):
        self.longitude = float(data["longitude"])
        if self.longitude > 180.0:
            self.longitude = self.longitude - 360.0
        self.datetime = data["datetime"]
        self.latitude = data["latitude"]
        self.altitude = data["altitude"]
        self.launch_details = launch_details

    @property
    def time(self):
        if "." in self.datetime:
            dt_object = datetime.datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=1)
        else:
            dt_object = datetime.datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=1)
        return f'{dt_object.strftime("%H:%M:%S")} BST'

    @property
    def date(self):
        if "." in self.datetime:
            dt_object = datetime.datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=1)
        else:
            dt_object = datetime.datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=1)
        return f'{dt_object.strftime("%a %d")}'

    @property
    def full_date(self):
        if "." in self.datetime:
            dt_object = datetime.datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=1)
        else:
            dt_object = datetime.datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=1)
        return f'{dt_object.strftime("%a %d %b")}'