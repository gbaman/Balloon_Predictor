from flask import Flask, render_template
import map_builder

app = Flask(__name__)

@app.route("/")
def home():
    map_data = map_builder.generate_flights()._repr_html_()
    return render_template("map.html", map_data=map_data, raw_flights=map_builder.raw_flights)

if __name__ == '__main__':
    app.run()