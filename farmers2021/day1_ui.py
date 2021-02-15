from geopy.distance import geodesic 
  
# Loading the lat-long data for Kolkata & Delhi 
myhouse = (12.9335296, 77.5749632) 
yourhouse = (12.2958, 76.6394) 
  
# Print the distance calculated in km 
print(geodesic(myhouse, yourhouse).km) 