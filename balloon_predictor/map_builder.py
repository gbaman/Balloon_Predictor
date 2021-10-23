import datetime
import threading
import time
from typing import List

import folium
import requests

from config import CASTOR_BAY, FURNEUX, VINCENT_SQUARE, COLEMORE

PREDICTOR_URL = "http://predict.cusf.co.uk/api/v1/"
#TITLE = "Launches from Vincent Square, Furneux and Colemore Common on the 4th and 5th July 2021"
TITLE = "Launches from Vincent Square, Furneux and Colemore Common on the 8th July 2021"
HOURLY_TITLE = "Hourly launches"

DATE1 = "2021-07-05"
DATE2 = "2021-10-30"


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


raw_flights = [
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 27000, 5, 5, f"{DATE1}T03:30:00Z", "Vincent Square", "red", "orange", 600),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 20000, 4, 5, f"{DATE1}T03:30:00Z", "Vincent Square", "red", "orange", 350),
    #Flight(FURNEUX[0], FURNEUX[1], 27000, 5, 5, f"{DATE1}T10:30:00Z", "Furneux", "blue", "purple", 600),
    #Flight(FURNEUX[0], FURNEUX[1], 20000, 4, 5, f"{DATE1}T10:30:00Z", "Furneux", "blue", "purple", 350),
    #Flight(FURNEUX[0], FURNEUX[1], 30000, 5, 5, f"{DATE1}T10:30:00Z", "Furneux", "blue", "purple", 1000),

    #Flight(COLEMORE[0], COLEMORE[1], 27000, 5, 5, f"{DATE1}T10:30:00Z", "Colemore", "yellow", "purple", 600),
    #Flight(COLEMORE[0], COLEMORE[1], 20000, 4, 5, f"{DATE1}T10:30:00Z", "Colemore", "yellow", "purple", 350),
    #Flight(COLEMORE[0], COLEMORE[1], 30000, 5, 5, f"{DATE1}T10:30:00Z", "Colemore", "yellow", "purple", 1000),

    Flight(VINCENT_SQUARE, 26000, 5, 5, f"{DATE2}T10:30:00Z", "Vincent Square", "pink", "orange", 600),
    Flight(VINCENT_SQUARE, 26000, 4, 5, f"{DATE2}T10:30:00Z", "Vincent Square", "green", "orange", 600),
    Flight(VINCENT_SQUARE, 26000, 3, 5, f"{DATE2}T10:30:00Z", "Vincent Square", "purple", "orange", 350),
    Flight(VINCENT_SQUARE, 26000, 2, 5, f"{DATE2}T10:30:00Z", "Vincent Square", "orange","orange", 200),

    #Flight(FURNEUX, 27000, 5, 5, f"{DATE2}T10:30:00Z", "Furneux", "green", "purple", 600),
    #Flight(FURNEUX, 20000, 4, 5, f"{DATE2}T10:30:00Z", "Furneux", "purple", "purple", 350),
    #Flight(FURNEUX, 12700, 3, 5, f"{DATE2}T10:30:00Z", "Furneux", "orange", "purple", 200),
    #Flight(FURNEUX, 30000, 5, 5, f"{DATE2}T10:30:00Z", "Furneux", "red", "purple", 1000),

    #Flight(COLEMORE, 27000, 5, 5, f"{DATE2}T10:30:00Z", "Colemore", "green", "purple", 600),
    #Flight(COLEMORE, 20000, 4, 5, f"{DATE2}T10:30:00Z", "Colemore", "purple", "purple", 350),
    #Flight(COLEMORE, 12700, 3, 5, f"{DATE2}T10:30:00Z", "Colemore", "orange", "purple", 200),
    #Flight(COLEMORE, 30000, 5, 5, f"{DATE2}T10:30:00Z", "Colemore", "red", "purple", 1000),

    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 26295, 2, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "blue", "red", 600),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 25698, 3, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "purple", "red", 600),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 24838, 4, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "green", "red", 600),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 19559, 2, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "blue", "red", 350),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 19048, 3, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "green", "red", 350),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 18313, 4, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "purple", "red", 350),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 13244, 2, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "blue","red", 200),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 12721, 3, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "green","red", 200),
    #Flight(VINCENT_SQUARE[0], VINCENT_SQUARE[1], 11969, 4, 5, f"{DATE2}T03:45:00Z", "Vincent Square", "purple","red", 200),

]


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


def get_flight_route_data(launch:Flight, flight_list):
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
    flight_list.append(launch)
    print("Thread done")
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


def draw_launch_map(flights):
    m = folium.Map(location=[VINCENT_SQUARE[1], VINCENT_SQUARE[2]], zoom_start=9)
    m.get_root().html.add_child(folium.Element(f"""<h3 align="center" style="font-size:16px"><b>{TITLE}</b></h3>"""))
    for flight in flights:
        points = []
        for point in flight.markers:
            points.append((point.latitude, point.longitude))
        folium.PolyLine(points, color=flight.line_colour, weight=2.5, opacity=1, ).add_to(m)
        for point in flight.markers:
            folium.CircleMarker((point.latitude, point.longitude), radius=1, popup=f"{point.launch_details.launch_site_name}<br>Burst : {point.launch_details.burst_altitude}m<br>Altitude : {round(point.altitude)}m<br>Time:{point.time}<br>Balloon size : {flight.balloon_size}g<br>Ascent Rate : {flight.ascent_rate}m/s",tooltip=f"{round(point.altitude)}m<br>Date : {point.date}", color=flight.marker_colour).add_to(m)
        folium.Marker((flight.markers[0].latitude, flight.markers[0].longitude),icon=folium.features.CustomIcon("static/img/target-1-sm.png", icon_size=(10, 10)), popup=f"Launch Site<br>Burst_Height:{flight.burst_altitude}m<br>Time:{flight.markers[0].time}<br>Balloon size : {flight.balloon_size}g<br>Date : {flight.markers[0].date}").add_to(m)
        folium.Marker((flight.burst_marker.latitude, flight.burst_marker.longitude), icon=folium.features.CustomIcon("static/img/pop-marker.png", icon_size=(20, 20)), popup=f"Burst<br>Burst_Height:{flight.burst_altitude}m<br>Time:{flight.burst_marker.time}<br>Balloon size : {flight.balloon_size}g<br>Date : {flight.burst_marker.date}").add_to(m)
        folium.Marker((flight.markers[-1].latitude, flight.markers[-1].longitude),icon=folium.features.CustomIcon("static/img/target-8-sm.png", icon_size=(10, 10)), popup=f"Landing Site<br>Burst_Height:{flight.burst_altitude}m<br>Time:{flight.markers[-1].time}<br>Balloon size : {flight.balloon_size}g<br>Date : {flight.markers[-1].date}<br>Ascent Rate : {flight.ascent_rate}m/s").add_to(m)

    return m


def draw_hourly_map(flights):
    m = folium.Map(location=[flights[0].launch_latitude, flights[0].launch_longitude], zoom_start=9)
    m.get_root().html.add_child(folium.Element(f"""<h3 align="center" style="font-size:16px"><b>{HOURLY_TITLE} - {flights[0].launch_site}</b></h3>"""))
    points = []
    for flight in flights:
        points.append((flight.markers[-1].latitude, flight.markers[-1].longitude))
        folium.Marker((flight.markers[-1].latitude, flight.markers[-1].longitude),
                      icon=folium.features.CustomIcon("static/img/target-1-sm.png", icon_size=(10, 10)),
                      popup=f"<b>Landing Site</b><br>Burst_Height:{flight.burst_altitude}m<br>Time:{flight.markers[-1].time}<br>Date:{flight.markers[-1].full_date}<br>Balloon size : {flight.balloon_size}g<br>Ascent Rate : {flight.ascent_rate}m/s").add_to(m)
    folium.PolyLine(points, color=flight.line_colour, weight=1.2, opacity=1, ).add_to(m)
    folium.Marker((flight.markers[0].latitude, flight.markers[0].longitude),
                  icon=folium.features.CustomIcon("static/img/target-8-sm.png", icon_size=(10, 10)),
                  popup=f"Launch site").add_to(m)
    return m


def generate_hourly_flights(location):
    print("Generating flights...")
    flights = []
    flight_threads = []
    flight_list:List[Flight] = []
    start = datetime.datetime.now()
    DAYS = 7
    HOUR_GAP = 2
    for index in range(0, int((24/HOUR_GAP) * DAYS)):
        new_datetime = start + datetime.timedelta(hours=index*HOUR_GAP)
        if 18 > new_datetime.hour > 6:
            flights.append(Flight(location, 26000, 5, 5, f"{new_datetime.strftime('%Y-%m-%dT%H:%M:%S')}Z", location[0], "pink", "red", 600))

    for flight in flights:
        flight_thread = threading.Thread(target=get_flight_route_data, args=(flight, flight_list))
        flight_thread.start()
        print("Thread started!")
        flight_threads.append(flight_thread)
    for flight_thread in flight_threads:
        flight_thread.join()

    flight_list.sort(key=lambda f: f.launch_datetime)
    return draw_hourly_map(flight_list)


    print()


def generate_launch_flights():
    print("Generating flights...")

    flight_threads = []
    flight_list = []

    for flight in raw_flights:
        flight_thread = threading.Thread(target=get_flight_route_data, args=(flight, flight_list))
        #flight_thread.daemon = True
        flight_thread.start()
        print("Thread started!")
        #time.sleep(0.3)
        flight_threads.append(flight_thread)
    for flight_thread in flight_threads:
        flight_thread.join()

    print("All threads done")
    return draw_launch_map(flight_list)