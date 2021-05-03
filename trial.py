import requests
import json
# call the OSMR API
# r = requests.get(f"http://router.project-osrm.org/route/v1/car/{lon_1},{lat};{lon_2},{lat_2}?overview=false""")
# r = requests.get(f"http://router.project-osrm.org/route/v1/car/77.594566,12.971599;77.5358,12.9354?overview=false""")
# r = requests.get(f"http://router.project-osrm.org/route/v1/car/75.8069,12.3375;77.5946,12.9716?overview=false""")


# r = requests.get(f"http://router.project-osrm.org/route/v1/car/77.5578,13.0108;77.5961,12.9716?overview=false""")

# r = requests.get(f"http://router.project-osrm.org/route/v1/car/77.5578,13.0108;77.5358,12.9354?overview=false""")

r = requests.get(f"http://router.project-osrm.org/route/v1/car/78.1291,13.1362;76.6394,12.2958?overview=false""")

# then you load the response using the json libray
# by default you get only one alternative so you access 0-th element of the `routes`
routes = json.loads(r.content)
route_1 = routes.get("routes")[0]
# print(route_1)
print(routes)


# 208 kms actually between Kolar to Mysore

# 13.1362° N, 78.1291° E - KOLAR
# 12.2958° N, 76.6394° E - MYSURU







# 10054
# lat,long
# 12.971599,77.594566 - blore
# 12.295810,76.639381 - mysore
# 287383.6

# coorg - 12.3375, 75.8069
# blore - 12.9716, 77.5946

# source = "13.0108, 77.5578" - aishu
# 12.9716° N, 77.5961° E


# dest = "12.9354, 77.5358"