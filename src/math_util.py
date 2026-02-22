# Add a metric for total miles traveled (using a simple haversine formula for distance between lat/lng points)
from math import radians, cos, sin, asin, sqrt
import pandas as pd

def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of Earth in miles
    return c * r

def calculate_total_miles(df: pd.DataFrame) -> float:
    total_miles = 0.0
    for i in range(1, len(df)):
        total_miles += haversine(
            df.loc[i-1, "longitude"], df.loc[i-1, "latitude"],
            df.loc[i, "longitude"], df.loc[i, "latitude"]
        )
    return total_miles