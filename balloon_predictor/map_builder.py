import datetime
import threading
import time
from typing import List

import folium
import requests

import config
from config import CASTOR_BAY, FURNEUX, VINCENT_SQUARE, COLEMORE, HOURLY_FLIGHT_PROFILE, TITLE, HOURLY_TITLE

from util import Flight, LocationMarker

PREDICTOR_URL = "http://predict.cusf.co.uk/api/v1/"


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
    if "error" in response.json():
        launch.error = response.json()["error"]
    else:
        for marker in response.json()["prediction"][0]["trajectory"] + response.json()["prediction"][1]["trajectory"]:
            launch.markers.append(LocationMarker(marker, launch))
        launch.burst_marker = LocationMarker(response.json()["prediction"][0]["trajectory"][-1], launch)
    flight_list.append(launch)
    print("Thread done")
    return launch


def draw_launch_map(flights):
    m = folium.Map(location=[VINCENT_SQUARE[1], VINCENT_SQUARE[2]], zoom_start=9)
    m.get_root().html.add_child(folium.Element(f"""<h3 align="center" style="font-size:16px"><b>{TITLE}</b></h3>"""))
    for flight in flights:
        if flight.error:
            continue
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
                  icon=folium.features.CustomIcon("static/img/target-8-sm.png", icon_size=(15, 15)),
                  popup=f"Launch site").add_to(m)
    return m


def generate_hourly_flights(location, burst_altitude, ascent_rate, descent_rate, balloon_size):
    print("Generating flights...")
    flights = []
    flight_threads = []
    flight_list:List[Flight] = []
    start = datetime.datetime.now()
    DAYS = 7
    HOUR_GAP = 2
    for index in range(0, int((24/HOUR_GAP) * DAYS)):
        new_datetime = start + datetime.timedelta(hours=index*HOUR_GAP)
        if 18 > new_datetime.hour > 3:
            flights.append(Flight(location, burst_altitude, ascent_rate, descent_rate, f"{new_datetime.strftime('%Y-%m-%dT%H:%M:%S')}Z", location[0], "pink", "red", balloon_size))

    for flight in flights:
        flight_thread = threading.Thread(target=get_flight_route_data, args=(flight, flight_list))
        flight_thread.start()
        print("Thread started!")
        flight_threads.append(flight_thread)
    for flight_thread in flight_threads:
        flight_thread.join()

    flight_list.sort(key=lambda f: f.launch_datetime)
    return draw_hourly_map(flight_list)


def generate_launch_flights():
    print("Generating flights...")

    flight_threads = []
    flight_list = []

    for flight in config.RAW_FLIGHTS:
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