'''import requests, json 


  
# enter your api key here 

api_key ='AIzaSyCU41kJdnR0Iv7HnPjfOryYab-BZ7r4J1U'
  
#source = "13.0108, 77.5578"

#dest = "12.9354, 77.5358"

source = "dehradun"
dest = "haridwar" 
# url variable store url  
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
print("here") 
# Get method of requests module 
# return response object 
r = requests.get(url + 'origins = ' + source +
                   '&destinations = ' + dest +
                   '&key = ' + api_key) 
print(r)
                     
# json method of response object 
# return json format result 
x = r.json() 
  
# by default driving mode considered 
  
# print the value of x 
print(x) '''

import requests
import json
import geocoder

g = geocoder.ip('me')
latlng = g.latlng
lat = str(latlng[0])
longi = str(latlng[1])

#13.2957° N, 77.5364° E - doddabalz
#12.9924° N, 78.1768° E
# 12.6518° N, 77.2086°

dest_long = "77.2086"
dest_lat = "12.6518"

r = requests.get(f"http://router.project-osrm.org/route/v1/car/" + longi + "," + lat + ";" + dest_long + "," + dest_lat + "?overview=false""")

# then you load the response using the json libray
# by default you get only one alternative so you access 0-th element of the `routes`
routes = json.loads(r.content)
route_1 = routes.get("routes")[0]
# print(route_1)
distance = route_1["legs"][0]["distance"]
final_dist = int(distance/1000)
print(final_dist)
