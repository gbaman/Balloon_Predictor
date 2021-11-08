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

DATE1 = "2021-11-13"
DATE2 = "2021-11-14"

RAW_FLIGHTS = [
    Flight(FURNEUX, 20000, 5.8, 5, f"{DATE1}T13:30:00Z", "Furneux", "pink", "orange", 350),
    Flight(FURNEUX, 20000, 5.8, 5, f"{DATE1}T11:30:00Z", "Furneux", "green", "orange", 350),

    Flight(FURNEUX, 20000, 5.8, 5, f"{DATE2}T13:30:00Z", "Furneux", "purple", "orange", 350),
    Flight(FURNEUX, 20000, 5.8, 5, f"{DATE2}T11:30:00Z", "Furneux", "orange","orange", 350),
    Flight(FURNEUX, 26000, 4, 5, f"{DATE2}T13:30:00Z", "Furneux", "red","grey", 600),
]