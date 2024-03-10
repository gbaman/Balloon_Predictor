# Balloon Predictor configuration file
from util import FlightManual, FlightBalloon
from burst_calc import BalloonEnum

# Main home page title
TITLE = "Vincent Square launches"

# Title for hourly launches pages
HOURLY_TITLE = "Hourly launches"


# Launch sites - Add your own launch site below
VINCENT_SQUARE = ["Vincent Square", "51.4934", "-0.1351"]
CASTOR_BAY = ["Castor bay", "54.50579488", "-6.4330024"]
FURNEUX = ["Furneux", "51.9314", "0.0795"]
COLEMORE = ["Colemore Common", "51.0622", "-1.0097"]
CHURCHILL = ["Churchill College", "52.2137", "0.0966"]

# All locations added to a Python list - Make sure to add any custom launch site to this list!
LOCATIONS = [VINCENT_SQUARE, CASTOR_BAY, FURNEUX, COLEMORE, CHURCHILL]

# Default location used for hourly predictions
DEFAULT_LOCATION = VINCENT_SQUARE

# Burst altitude, assent rate, descent rate, balloon size
HOURLY_FLIGHT_PROFILE = [26000, 4.5, 5, BalloonEnum.H600]


def create_raw_flights():

    RAW_FLIGHTS = []
    # Add your flights below
    # 2 types of flights are supported.
    # The first (and recommended) is a FlightBalloon object. This will automatically calculate the burst altitude, helium needed etc by using the same data on the Habhub burst predictor. Must include a payload weight.
    # See BalloonEnum class in burst_calc.py for available balloon sizes.
    RAW_FLIGHTS.append(FlightBalloon(launch_site=VINCENT_SQUARE, balloon=BalloonEnum.H600, payload_mass=1700, descent_rate=5, launch_datetime=f"2023-06-20T04:45:00Z", target_ascent_rate=5))

    # The second option is a FlightManual object. This allows specifying the burst altitude to do the calculations manually.
    RAW_FLIGHTS.append(FlightManual(launch_site=COLEMORE, burst_altitude=30000, ascent_rate=5, descent_rate=5, launch_datetime=f"2023-06-21T04:45:00Z", balloon=BalloonEnum.H600))

    return RAW_FLIGHTS
