from flask import Flask, render_template
import map_builder
from config import LOCATIONS, DEFAULT_LOCATION

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
    return render_template("map.html", map_data=map_data, raw_flights=map_builder.raw_flights)


@app.route("/hourly")
def hourly():
    map_data = map_builder.generate_hourly_flights(DEFAULT_LOCATION)._repr_html_()
    return render_template("map.html", map_data=map_data, raw_flights=map_builder.raw_flights)


@app.route("/hourly/<location_name>")
def hourly_location(location_name):
    found_location = None
    locations_str = ""
    for location in LOCATIONS:
        location_lower = location[0].lower().replace(" ", "_")
        locations_str = f"{locations_str}<br>- {location_lower}"
        if location_lower == location_name:
            map_data = map_builder.generate_hourly_flights(location)._repr_html_()
            return render_template("hourly_map.html", map_data=map_data, raw_flights=map_builder.raw_flights)
    return f"Error - Location {found_location} does not exist. Available locations can be found below. {locations_str}"

if __name__ == '__main__':
    app.run()