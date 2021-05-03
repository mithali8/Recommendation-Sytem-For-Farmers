import pandas as pd
import numpy as np
import json
from sklearn.utils.testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
import requests
import geocoder
from geopy.geocoders import Nominatim
from get_holidays import in_holidays
import cgi
import datetime
from datetime import timedelta, date

dest_long = str(13)
dest_lat = str(77)

lat = str(13.1362)
longi = str(78.1291)

r = requests.get(f"http://router.project-osrm.org/route/v1/car/" + longi + "," + lat + ";" + dest_long + "," + dest_lat + "?overview=false""")
routes = json.loads(r.content)
route_1 = routes.get("routes")[0]
distance = route_1["legs"][0]["distance"]
final_dist = int(distance/1000)