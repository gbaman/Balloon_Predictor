import datetime
from typing import List


class Flight():
    def __init__(self, launch_site, burst_altitude, ascent_rate, descent_rate, launch_datetime, launch_site_name, marker_colour, line_colour, balloon_size):
        self.launch_site = launch_site[0]
        self.launch_latitude = launch_site[1]
        self.launch_longitude = launch_site[2]
        self.burst_altitude = burst_altitude
        self.ascent_rate = ascent_rate
        self.descent_rate = descent_rate
        self.launch_datetime = launch_datetime
        self.launch_site_name = launch_site_name
        self.markers: List[LocationMarker] = []
        self.burst_marker : LocationMarker = None
        self.marker_colour = marker_colour
        self.line_colour = line_colour
        self.balloon_size = balloon_size
        self.error = None


class LocationMarker():
    def __init__(self, data, launch_details: Flight):
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