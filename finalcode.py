import pandas as pd
import numpy as np
import json
from sklearn.utils.testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
import requests
import geocoder
from geopy.geocoders import Nominatim
from get_holidays import in_holidays, m_holidays
import cgi
import datetime
# from datetime import timedelta, date, datetime
from numpy import isnan
from flask import Flask, render_template, request
#our own data structures

from marketLocations import market_locs_demo
from markets import markets
from crops import crops
from crops_harvest_time import harvest_time
# from crop_seasonality import crop_market_seasonality
from helper import fill_weekdays, nan_rows, croston_prep, marketChoice, Croston, split_test_train, plot_test_pred, plot_test_pred_train
from crop_compare import crop_comp


#HELPER FUNCTIONS WE CAN SHIFT TO ANOTHER CLASS
def user_entered_loc(location):
    try:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(str(location))
        lat = str(location.latitude)
        longi = str(location.longitude)
    except:
        lat, longi = current_loc(location)
    return lat, longi

def current_loc(location):
    g = geocoder.ip('me')
    latlng = g.latlng
    lat = str(latlng[0])
    longi = str(latlng[1])
    return lat, longi

def get_distance_from_loc_to_market(lat, longi, market_locs_demo):
    distances = {'DODDABALLAPUR': 41, 'CHICKBALLAPUR': 59, 'KOLAR': 67, 'MYSURU': 187}
    for i in market_locs_demo:
        dest_long = str(market_locs_demo[i][1])
        dest_lat = str(market_locs_demo[i][0])
        # r = requests.get(f"http://router.project-osrm.org/route/v1/car/" + longi + "," + lat + ";" + dest_long + "," + dest_lat + "?overview=false""")
        # routes = json.loads(r.content)
        # route_1 = routes.get("routes")[0]
        # distance = route_1["legs"][0]["distance"]
        # final_dist = int(distance/1000)
        # distances[i] = final_dist #doddaballapur: 85 kms (from user entered loc), mysore: 65 kms 
    return distances


def calculate_logistic_cost(amt, distances, market_prices):
    total_log_cost = {}
    if amt < 500:
        cost = 6
    elif amt < 1000:
        cost = 10
    else:
        cost = 15
    for market, price_dict in market_prices.items():
        price_per_quintal = price_dict["Predicted"]
        number_of_quintals = amt/100
        total_log_cost[market] = int(price_per_quintal*(amt/100)) - int(cost*distances[market])
    return total_log_cost

def calculate_seasonal_cost(results, end_date):
    final_price = {}
    seasonal_cost = {}
    for market, price_dict in results.items():
        if in_holidays.get(end_date) != None or in_holidays.get(end_date - datetime.timedelta(1)) != None:
            seasonal_cost[market] = 0.15 * price_dict["Predicted"]
            final_price[market] = 1.15 * price_dict["Predicted"]
        elif m_holidays.get(end_date) != None:
            seasonal_cost[market] = 0.1 * price_dict["Predicted"]
            final_price[market] = 1.1 * price_dict["Predicted"]
        else:
            final_price[market] = price_dict["Predicted"]
            seasonal_cost[market] = 0
    return seasonal_cost, final_price

    

app = Flask(__name__)

#homepage that shows the options
@app.route('/', methods = ['GET'])
def intro():
      return render_template('intro.html')

@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        location = request.form['loc'] #user specified loc 
        if (location):
          lat, longi = user_entered_loc(location)
        else:
          lat, longi = current_loc(location)
        crp = request.form['crop'] #beet
        amt = int(request.form['amount']) #500
        use_case = request.form['use_case'] #long term
        distances = get_distance_from_loc_to_market(lat, longi, market_locs_demo)
        print(distances)
        # distances = {"DODDABALLAPUR": "50"}

        # Calling compare with the markets - use_cases: long term and short term (not which crop to grow best)
        #SINCE WE NEED TO HAVE A CAP FOR THE NUMBER OF KMS - LIKE ONLY IN A 100 KMS RADIUS 
        # for market, dist in distances.items():
        #     if dist > 150:
        #         del distances[market]

        data = {}

        # start_date = "2020-07-06" #(date to show choose between crops) also for long term capsicum
        start_date = "2020-02-11"
        # start_date = "2020-03-01"
        start_date_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')

        if use_case == "short_term":
            time_to_predict = "10"
        elif use_case == "long_term":
            time_to_predict = harvest_time[crp]
        elif use_case == "plan":
            use_case = "long_term"
            best_prices = {}
            for crop in crop_comp:
                results = compare(crop, start_date, use_case)
                market_specfic_prices = []
                for market, price_dict in results.items():
                    market_specfic_prices.append(price_dict["Predicted"])
                best_market_price = max(market_specfic_prices)
                best_prices[crop] = best_market_price
            data = {}
            data["Crop"] = []
            data["Price per Quintal"] = []
            best_crop = max(best_prices, key=best_prices.get)
            for crop in best_prices:
                data["Crop"].append(crop)
                data["Price per Quintal"].append(int(best_prices[crop]))
            return render_template('compare.html', x = data, best = best_crop) 
            print("choosing between crops and writing logic in a bit\n")


        results = compare(crp, start_date, use_case)
        
        # WHAT WE WILL BE RETURNING #
        data["Market"] = []
        data["Price Per Quintal"] = []
        data['Net Profit'] = []
        data["Season"] = []
        # ------------------------- #

        for market, price_dict in results.items():
            data["Market"].append(market)
            for predicted_price in price_dict:
                data["Price Per Quintal"].append(int(price_dict[predicted_price]))

        end_date = start_date_datetime + datetime.timedelta(int(time_to_predict))
        seasonal_cost, final_price = calculate_seasonal_cost(results, end_date)

        price_with_log_cost = calculate_logistic_cost(amt, distances, results)
        # {"market" : "cost"}

        
        # final price includes both seasonal as well as logistic cost
        


        for market in final_price:
            data["Net Profit"].append(int(final_price[market]))
            data["Season"].append(int(seasonal_cost[market]))

        best_price = max(data["Net Profit"])
        best_market_index = data["Net Profit"].index(best_price)
        best_market = data["Market"][best_market_index]

        return render_template('index.html', x = data, best = best_market)





        
        



        # return render_template('index.html', x = results)





from statsmodels.tsa.holtwinters import ExponentialSmoothing
@ignore_warnings(category=ConvergenceWarning)
def Croston_HW(crop_data, market, rand, time_to_predict, start_date):
  marketData = marketChoice(crop_data, market) # nan rows are made
  marketData = croston_prep(marketData, market)
  marketData["Modal"] = pd.to_numeric(marketData["Modal"])
  crostonData = Croston(marketData["Modal"],extra_periods=1,alpha=0.4)
  for ind in crostonData.index:
    if crostonData["Demand"][ind] == 0:
      crostonData["Demand"][ind] = crostonData["Forecast"][ind]
  crostonData = crostonData["Demand"]
  train_data, test_data = split_test_train(crostonData, time_to_predict, start_date)
#   print("train_data: ", train_data)
#   print("\n")
#   print("test_data: ", test_data)
  test_data = test_data[0:len(test_data)-1]
  fit1 = ExponentialSmoothing(train_data,
                            seasonal_periods=rand,   
                            trend='multiplicative', 
                            seasonal='mul', 
                            damped=True).fit(use_boxcox=True) 
  frame = fit1.forecast(int(time_to_predict))
  pred = pd.DataFrame
  pred = frame 
  res = list(pred[0:int(time_to_predict)])
  return res, test_data



def compare(crop, date, use_case):
    results = {}
    crop_csv = crops[crop]
    crop_data = pd.read_csv(crop_csv, parse_dates=['Date'], dayfirst=True)
    crop_data["weekday"] = crop_data["Date"].apply(lambda x: pd.to_datetime(x).date().weekday(), 1)
    crop_data = crop_data.loc[:, ~crop_data.columns.str.contains('^Unnamed')]
    f = open("crop_seasonality.json")
    crop_market_seasonality = json.load(f)
    crop_data['Date']= pd.to_datetime(crop_data['Date'], dayfirst=True, format = "%d/%m/%Y", errors='coerce')
    for market in markets:
        seasonality_period = crop_market_seasonality[crop][use_case][market]
        trial = marketChoice(crop_data, market)
        trial = trial[trial['Date'] == date]
        start_date = trial.index[0]
        if start_date == 36:
            seasonality_period = 35 
        if use_case == "short_term":
            time_to_predict = 10
        else:
            time_to_predict = harvest_time[crop]
        res, test_data = Croston_HW(crop_data, market, seasonality_period,time_to_predict, start_date)
        results[market] = dict()
        # results[market]["Actual"] = test_data[start_date + time_to_predict]
        results[market]["Predicted"] = res[len(res) - 1] 
    return results
    
if __name__ == '__main__':
      app.run(debug=True)

# data = compare("beetroot", "2020-07-06", "long_term")
# print(data)