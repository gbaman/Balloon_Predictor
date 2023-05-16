# Balloon Predictor configuration file
from util import Flight

# Launch sites
VINCENT_SQUARE = ["Vincent Square", "51.4934", "-0.1351"]
CASTOR_BAY = ["Castor bay", "54.50579488", "-6.4330024"]
FURNEUX = ["Furneux", "51.9314", "0.0795"]
COLEMORE = ["Colemore Common", "51.0622", "-1.0097"]
CHURCHILL = ["Churchill College", "52.2137", "0.0966"]

# All locations added to a Python list
LOCATIONS = [VINCENT_SQUARE, CASTOR_BAY, FURNEUX, COLEMORE, CHURCHILL]

# Default location used for hourly predictions
DEFAULT_LOCATION = CHURCHILL

# Burst altitude, assent rate, descent rate, balloon size
HOURLY_FLIGHT_PROFILE = [26000, 4.5, 5, 600]

# Main home page title
TITLE = "Launches from Cambridge University"

# Title for hourly launches pages
HOURLY_TITLE = "Hourly launches"

BASE_DATE = "2023-05-"


def create_raw_flights():
    RAW_FLIGHTS = []
    for date in [21, 22, 27, 28]:
        for burst, asent, balloon_type, notes in [[25000 , 5, 600, "1500g payload"],
                                                  [26500, 5, 600, "1000g payload"],
                                                  [18873, 5, 300, "1500g payload"],
                                                  [20700, 5, 300, "1000g payload"]
                                                  ]:
            RAW_FLIGHTS.append(Flight(CHURCHILL, burst, asent, 5, f"{BASE_DATE}{str(date).zfill(2)}T05:00:00Z", balloon_type, notes))
    return RAW_FLIGHTS
