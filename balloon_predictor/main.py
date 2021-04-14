from flask import Flask, render_template
import map_builder

app = Flask(__name__)

@app.route("/")
def home():
    return map_builder.generate_flights()._repr_html_()

if __name__ == '__main__':
    app.run()