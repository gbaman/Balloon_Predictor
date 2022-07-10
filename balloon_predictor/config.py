# Balloon Predictor configuration file
from util import Flight

# Launch sites
VINCENT_SQUARE = ["Vincent Square", "51.4934", "-0.1351"]
CASTOR_BAY = ["Castor bay", "54.50579488", "-6.4330024"]
FURNEUX = ["Furneux", "51.9314", "0.0795"]
COLEMORE = ["Colemore Common", "51.0622", "-1.0097"]

# All locations added to a Python list
LOCATIONS = [VINCENT_SQUARE, CASTOR_BAY, FURNEUX, COLEMORE]

# Default location used for hourly predictions
DEFAULT_LOCATION = VINCENT_SQUARE

# Burst altitude, assent rate, descent rate, balloon size
HOURLY_FLIGHT_PROFILE = [26000, 4.5, 5, 600]

# Main home page title
TITLE = "Launches from Vincent Square"

# Title for hourly launches pages
HOURLY_TITLE = "Hourly launches"

BASE_DATE = "2022-07-"


def create_raw_flights():
    RAW_FLIGHTS = []
    for date in [11]:
        for burst, asent, balloon_type, notes in [[27308 , 5.1, 2500, "2500g payload"], [27300, 4.3, 1000, "3000g payload"], [27248, 3.8, 1000, "3300g payload"], [25000, 4.3, 3000, "3000g payload : Cutdown 25km"], [15000, 5.63, 350, ""]]:
            RAW_FLIGHTS.append(Flight(VINCENT_SQUARE, burst, asent, 5, f"{BASE_DATE}{str(date).zfill(2)}T05:00:00Z", balloon_type, notes))
    return RAW_FLIGHTS
