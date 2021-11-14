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
DEFAULT_LOCATION = FURNEUX

# Burst altitude, assent rate, descent rate, balloon size
HOURLY_FLIGHT_PROFILE = [26000, 4.5, 5, 600]

# Main home page title
TITLE = "Launches from Furneux"

# Title for hourly launches pages
HOURLY_TITLE = "Hourly launches"

DATE1 = "2021-11-20"
DATE2 = "2021-11-21"
DATE3 = "2021-11-22"

RAW_FLIGHTS = [
    Flight(FURNEUX, 20000, 5.8, 5, f"{DATE1}T13:00:00Z", 350),
    Flight(FURNEUX, 26500, 4, 5, f"{DATE1}T13:00:00Z", 600),

    Flight(COLEMORE, 20000, 5.8, 5, f"{DATE1}T13:00:00Z", 350),
    Flight(COLEMORE, 26500, 4, 5, f"{DATE1}T13:00:00Z", 600),

    Flight(FURNEUX, 20000, 5.8, 5, f"{DATE2}T13:00:00Z", 350),
    Flight(FURNEUX, 26500, 4, 5, f"{DATE2}T13:00:00Z", 600),

    Flight(COLEMORE, 20000, 5.8, 5, f"{DATE2}T13:00:00Z", 350),
    Flight(COLEMORE, 26500, 4, 5, f"{DATE2}T13:00:00Z", 600),

    Flight(FURNEUX, 20000, 5.8, 5, f"{DATE3}T13:00:00Z", 350),
    Flight(FURNEUX, 26500, 4, 5, f"{DATE3}T13:00:00Z", 600),

    Flight(COLEMORE, 20000, 5.8, 5, f"{DATE3}T13:00:00Z", 350),
    Flight(COLEMORE, 26500, 4, 5, f"{DATE3}T13:00:00Z", 600),


]