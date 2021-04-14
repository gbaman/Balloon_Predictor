import datetime
from typing import List

import folium
import requests

PREDICTOR_URL = "http://predict.cusf.co.uk/api/v1/"
VINCENT_SQUARE = ["51.4934", "-0.1351"]
FURNEUX = ["51.9314", "0.0795"]
TITLE = "Launches from Vincent Square and Furneux on the 16th March 2021 with bursts of 13000m, 23000m and 26000m"


class Flight():
    def __init__(self, launch_latitude, launch_longitude, burst_altitude, ascent_rate, descent_rate, launch_datetime, launch_site_name, marker_colour, line_colour):
        self.launch_latitude = launch_latitude
        self.launch_longitude = launch_longitude
        self.burst_altitude = burst_altitude
        self.ascent_rate = ascent_rate
        self.descent_rate = descent_rate
        self.launch_datetime = launch_datetime
        self.launch_site_name = launch_site_name
        self.markers: List[LocationMarker] = []
        self.burst_marker : LocationMarker = None
        self.marker_colour = marker_colour
        self.line_colour = line_colour


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


def get_flight_route_data(launch:Flight):
    launch_longitude = float(launch.launch_longitude)
    if launch_longitude < 0:
        launch_longitude = 360 + launch_longitude
    response = requests.get(PREDICTOR_URL, params={
        "launch_longitude":launch_longitude,
        "launch_latitude":launch.launch_latitude,
        "burst_altitude":launch.burst_altitude,
        "ascent_rate":launch.ascent_rate,
        "descent_rate":launch.descent_rate,
        "launch_datetime":launch.launch_datetime,
        "launch_altitude":"0",
        "profile":"standard_profile",
        "version":"1"
    })
    for marker in response.json()["prediction"][0]["trajectory"] + response.json()["prediction"][1]["trajectory"]:
        launch.markers.append(LocationMarker(marker, launch))
    launch.burst_marker = LocationMarker(response.json()["prediction"][0]["trajectory"][-1], launch)
    return launch


# No longer used
def get_all_flights() -> List[List[LocationMarker]]:
    flights = []
    current_datetime = datetime.datetime.utcnow()
    while current_datetime < datetime.datetime.utcnow() + datetime.timedelta(days=3):
        print(f"Requesting for {current_datetime.isoformat('T') + 'Z'}")
        new_markers = get_flight_route_data(longitude, latitude, 23000, 5, 5, current_datetime.isoformat("T") + "Z")
        flights.append(new_markers)
        current_datetime = current_datetime + datetime.timedelta(hours=4)
    return flights


def draw_map(flights):
    m = folium.Map(location=[VINCENT_SQUARE[0], VINCENT_SQUARE[1]], zoom_start=9)
    m.get_root().html.add_child(folium.Element(f"""<h3 align="center" style="font-size:16px"><b>{TITLE}</b></h3>"""))
    for flight in flights:
        points = []
        for point in flight.markers:
            points.append((point.latitude, point.longitude))
        folium.PolyLine(points, color=flight.line_colour, weight=2.5, opacity=1, ).add_to(m)
        for point in flight.markers:
            folium.CircleMarker((point.latitude, point.longitude), radius=1, popup=f"{point.launch_details.launch_site_name}<br>Burst : {point.launch_details.burst_altitude}m<br>Altitude : {round(point.altitude)}m<br>Time : {point.time}",tooltip=f"{round(point.altitude)}m", color=flight.marker_colour).add_to(m)
        folium.Marker((flight.markers[0].latitude, flight.markers[0].longitude),icon=folium.features.CustomIcon("static/img/target-1-sm.png", icon_size=(10, 10)), popup=f"Launch Site<br>Burst_Height:{flight.burst_altitude}m<br>Time : {flight.markers[0].time}").add_to(m)
        folium.Marker((flight.burst_marker.latitude, flight.burst_marker.longitude), icon=folium.features.CustomIcon("static/img/pop-marker.png", icon_size=(20, 20)), popup=f"Burst<br>Burst_Height:{flight.burst_altitude}m<br>Time : {flight.burst_marker.time}").add_to(m)
        folium.Marker((flight.markers[-1].latitude, flight.markers[-1].longitude),icon=folium.features.CustomIcon("static/img/target-8-sm.png", icon_size=(10, 10)), popup=f"Landing_Site<br>Burst_Height:{flight.burst_altitude}m<br>Time:{flight.markers[-1].time}").add_to(m)

    return m

def generate_flights():
    #flights = get_all_flights()
    flights = []
    flights.append(get_flight_route_data(Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 26000, 5, 5, "2021-04-16T11:00:00Z", "Vincent Square", "red", "orange")))
    flights.append(get_flight_route_data(Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 23000, 5, 5, "2021-04-16T11:00:00Z", "Vincent Square", "red", "orange")))
    flights.append(get_flight_route_data(Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 13000, 5, 5, "2021-04-16T11:00:00Z", "Vincent Square", "red", "orange")))
    flights.append(get_flight_route_data(Flight(FURNEUX[0], FURNEUX[1], 26000, 5, 5, "2021-04-16T14:00:00Z", "Furneux", "blue", "purple")))
    flights.append(get_flight_route_data(Flight(FURNEUX[0], FURNEUX[1], 23000, 5, 5, "2021-04-16T14:00:00Z", "Furneux", "blue", "purple")))
    flights.append(get_flight_route_data(Flight(FURNEUX[0], FURNEUX[1], 13000, 5, 5, "2021-04-16T14:00:00Z", "Furneux", "blue", "purple")))
    return draw_map(flights)