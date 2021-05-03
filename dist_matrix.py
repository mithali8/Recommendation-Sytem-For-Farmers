# importing required libraries 
import requests, json 

source = "dehradun"
dest = "haridwar"

# enter your api key here 
api_key ='AIzaSyA7PAfP8Ktje4rGEsfSGRWeLv-Kugnz9dc'

# Take source as input 
# source = "13.0108, 77.5578"

# dest = "12.9354, 77.5358"

# 13.0108° N, 77.5578° E
# 12.9354° N, 77.5358° E


# Take destination as input 


# url variable store url 
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'

# Get method of requests module 
# return response object 
r = requests.get(url + 'origins = ' + source +
				'&destinations = ' + dest +
				'&key = ' + api_key) 
					
# json method of response object 
# return json format result 
x = r.json() 

# by default driving mode considered 

# print the value of x 
print(x) 

# importing googlemaps module 
# import googlemaps 

# # Requires API key 
# gmaps = googlemaps.Client(key='AIzaSyA7PAfP8Ktje4rGEsfSGRWeLv-Kugnz9dc') 

# # Requires cities name 
# my_dist = gmaps.distance_matrix('Delhi','Mumbai')['rows'][0]['elements'][0] 

# # Printing the result 
# print(my_dist) 

