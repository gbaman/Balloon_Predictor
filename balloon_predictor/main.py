from flask import Flask, render_template

import config
import map_builder
from config import LOCATIONS, DEFAULT_LOCATION, HOURLY_FLIGHT_PROFILE

app = Flask(__name__)

@app.context_processor
def generate_nav_bar():
    return_dict = {"nav_bar":[[["Main map", "/"]]],
            "title":"Balloon predictor"}
    hourly_locations = []
    for location in LOCATIONS:
        hourly_locations.append([location[0], f"/hourly/{location[0].lower().replace(' ', '_')}"])
    return_dict["nav_bar"].append(hourly_locations)
    return return_dict


@app.route("/")
def home():
    map_data = map_builder.generate_launch_flights()._repr_html_()
    return render_template("map.html", map_data=map_data, raw_flights=config.RAW_FLIGHTS)


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
            return render_template("hourly_map.html", map_data=map_data, raw_flights=config.RAW_FLIGHTS)
    return f"Error - Location {found_location} does not exist. Available locations can be found below. {locations_str}"

if __name__ == '__main__':
    app.run()