from flask import Flask, render_template

import config
import map_builder
import balloon_graphs
from config import LOCATIONS, DEFAULT_LOCATION, HOURLY_FLIGHT_PROFILE

app = Flask(__name__)

@app.context_processor
def generate_nav_bar():
    return_dict = {"nav_bar":[[["Main map", "/"]]],
            "title":"Balloon predictor"}
    return_dict["nav_bar"].append([["Balloon graphs", "/graphs/ascent/5"]])
    hourly_locations = []
    for location in LOCATIONS:
        hourly_locations.append([location[0], f"/hourly/{location[0].lower().replace(' ', '_')}"])
    return_dict["nav_bar"].append(hourly_locations)
    return return_dict


@app.route("/")
def home():
    flight_list, map_data = map_builder.generate_launch_flights()
    return render_template("map.html", map_data=map_data, raw_flights=flight_list)


@app.route("/hourly")
@app.route("/hourly/<location_name>")
@app.route("/hourly/<location_name>/<burst_altitude>/<ascent_rate>/<descent_rate>/<balloon_size>")
def hourly_location(location_name=DEFAULT_LOCATION[0], burst_altitude=HOURLY_FLIGHT_PROFILE[0], ascent_rate=HOURLY_FLIGHT_PROFILE[1], descent_rate=HOURLY_FLIGHT_PROFILE[2], balloon_size=HOURLY_FLIGHT_PROFILE[3]):
    found_location = None
    locations_str = ""
    for location in LOCATIONS:
        location_lower = location[0].lower().replace(" ", "_")
        locations_str = f"{locations_str}<br>- {location_lower}"
        if location_lower == location_name.lower():
            map_data = map_builder.generate_hourly_flights(location, burst_altitude, ascent_rate, descent_rate, balloon_size)._repr_html_()
            return render_template("hourly_map.html", map_data=map_data, raw_flights=config.create_raw_flights())
    return f"Error - Location {found_location} does not exist. Available locations can be found below. {locations_str}"


@app.route("/graphs/ascent")
@app.route("/graphs/ascent/<ascent_rate>")
@app.route("/graphs/ascent/<ascent_rate>/<weight>")
def generate_balloon_graphs(ascent_rate=5, weight=None):
    graphs = []
    weights_tuple = (500, 1000, 1500, 2000, 2500, 3000)
    if weight:
        weights_tuple = (int(weight),)
    graphs.append(balloon_graphs.create_balloon_gas_graph(target_ascent_rate=float(ascent_rate), weights=weights_tuple))
    graphs.append(balloon_graphs.create_balloon_altitude_graph(target_ascent_rate=float(ascent_rate), weights=weights_tuple))
    return render_template("graphs.html", graphs=graphs)


if __name__ == '__main__':
    app.run()