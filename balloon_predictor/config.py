# Balloon Predictor configuration file
from util import FlightManual, FlightBalloon
from burst_calc import BalloonEnum

# Launch sites
VINCENT_SQUARE = ["Vincent Square", "51.4934", "-0.1351"]
CASTOR_BAY = ["Castor bay", "54.50579488", "-6.4330024"]
FURNEUX = ["Furneux", "51.9314", "0.0795"]
COLEMORE = ["Colemore Common", "51.0622", "-1.0097"]
CHURCHILL = ["Churchill College", "52.2137", "0.0966"]

# All locations added to a Python list
LOCATIONS = [VINCENT_SQUARE, CASTOR_BAY, FURNEUX, COLEMORE, CHURCHILL]

# Default location used for hourly predictions
DEFAULT_LOCATION = VINCENT_SQUARE

# Burst altitude, assent rate, descent rate, balloon size
HOURLY_FLIGHT_PROFILE = [26000, 4.5, 5, 600]

# Main home page title
TITLE = "Vincent Square launches"

# Title for hourly launches pages
HOURLY_TITLE = "Hourly launches"

BASE_DATE = "2023-06-"


def create_raw_flights():

    RAW_FLIGHTS = []
    for date in [24, 25]:
        RAW_FLIGHTS.append(FlightBalloon(VINCENT_SQUARE, balloon=BalloonEnum.H600, payload_mass=1700, descent_rate=5, launch_datetime=f"{BASE_DATE}{str(date).zfill(2)}T04:45:00Z", target_ascent_rate=4.2))
        RAW_FLIGHTS.append(FlightBalloon(VINCENT_SQUARE, balloon=BalloonEnum.H800, payload_mass=1700, descent_rate=5, launch_datetime=f"{BASE_DATE}{str(date).zfill(2)}T04:45:00Z", target_ascent_rate=4.2))

    return RAW_FLIGHTS
