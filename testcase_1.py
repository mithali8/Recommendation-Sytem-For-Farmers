#!/usr/bin/env python

import pandas as pd
import numpy as np
import json
import random
from sklearn.utils.testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from collections import Counter
import requests
import geocoder
from geopy.geocoders import Nominatim
from get_holidays import in_holidays, m_holidays
import cgi
import datetime
# from datetime import timedelta, date, datetime
from numpy import isnan
from flask import Flask, render_template, request
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
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
    # try:
    #     distances = {}
    #     for i in market_locs_demo:
    #         dest_long = str(market_locs_demo[i][1])
    #         dest_lat = str(market_locs_demo[i][0])
    #         r = requests.get(f"http://router.project-osrm.org/route/v1/car/" + longi + "," + lat + ";" + dest_long + "," + dest_lat + "?overview=false""")
    #         routes = json.loads(r.content)
    #         route_1 = routes.get("routes")[0]
    #         distance = route_1["legs"][0]["distance"]
    #         final_dist = int(distance/1000)
    #         distances[i] = final_dist 
    # except:

    #      distances = {'DODDABALLAPUR': 41, 'CHICKBALLAPUR': 59, 'KOLAR': 67, 'MYSURU': 187, 'BINNY MILL (F&V)': 7}
    distances = {'DODDABALLAPUR': 41, 'CHICKBALLAPUR': 59, 'KOLAR': 67, 'MYSURU': 187, 'BINNY MILL (F&V)': 7}
    return distances


def calculate_logistic_cost(amt, distances, market_prices):
    total_log_cost = {}
    if amt < 500:
        cost = 6
    elif amt < 1000:
        cost = 10
    else:
        cost = 15
    for market in market_prices:
        total_log_cost[market] = []
        for days in range(3):
            price_per_quintal = market_prices[market][days]
            number_of_quintals = amt/100
            total_log_cost[market].append(int(price_per_quintal*(amt/100)) - int(cost*distances[market]))
    return total_log_cost


def calculate_seasonal_cost(results, end_date):
    final_price = {}
    seasonal_cost = {}
    for market, price_dict in results.items():
        seasonal_cost[market] = []
        final_price[market] = []
        for days in range(3):

            if in_holidays.get(end_date - datetime.timedelta(2 - days)) != None:
                hol = in_holidays.get(end_date - datetime.timedelta(2 - days))
                
                seasonal_cost[market].append(0.15 * price_dict["Predicted"][days])
                final_price[market].append(1.15 * price_dict["Predicted"][days])
                if days == 2:
                    
                    seasonal_cost[market][1] = 0.15 * price_dict["Predicted"][days-1]
                    final_price[market][1] = 1.15 * price_dict["Predicted"][days-1]

            elif m_holidays.get(end_date - datetime.timedelta(2 - days)) != None:
                hol = "MUHURAT"
                seasonal_cost[market].append(0.1 * price_dict["Predicted"][days]) 
                final_price[market].append(1.1 * price_dict["Predicted"][days])

            else:
                hol = "None"
                final_price[market].append(price_dict["Predicted"][days])
                seasonal_cost[market].append(0)
    print("seasonal cost : ", seasonal_cost)
    print("final price : ", final_price)
    return seasonal_cost, final_price, hol

    

uc =  None
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def getusecase():
    return render_template('page1.html')

#homepage that shows the options
@app.route('/send_usecase', methods = ['POST'])
def intro():
      usec = request.form["use_case"]
      global uc
      uc = usec
      print(uc)
      if uc != "plan":
            print("hello")
            return render_template('intro.html')
      else:
        print("whatsap")
        return render_template('intro_wo_crop.html')


@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        use_case = uc
        location = request.form['loc'] #user specified loc
        if (location):
          lat, longi = user_entered_loc(location)
        else:
          lat, longi = current_loc(location)
        if uc != "plan":
            crp = request.form['crop'] #beet
        amt = int(request.form['amount']) #500
        # use_case = request.form['use_case'] #long term
        distances = get_distance_from_loc_to_market(lat, longi, market_locs_demo)
        print(distances)
        # distances = {"DODDABALLAPUR": "50"}

        # Calling compare with the markets - use_cases: long term and short term (not which crop to grow best)
        #SINCE WE NEED TO HAVE A CAP FOR THE NUMBER OF KMS - LIKE ONLY IN A 100 KMS RADIUS 
        # for market, dist in distances.items():
        #     if dist > 150:
        #         del distances[market]

        data = {}
        data1 = {}
        data2 = {}

        start_date = "2020-04-10" #(date to show choose between crops) also for long term capsicum
        
        start_date_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')

        if use_case == "short_term":
            time_to_predict = "10"
            print("tp:", time_to_predict)
        elif use_case == "long_term":
            time_to_predict = harvest_time[crp]
        elif use_case == "plan":
            use_case = "long_term"
            best_prices = {}
            for crop in crop_comp:
                results = compare_crops(crop, start_date, use_case)
                market_specfic_prices = []
                for market, price_dict in results.items():
                    market_specfic_prices.append(price_dict["Predicted"])
                best_market_price = max(market_specfic_prices)
                best_prices[crop] = best_market_price
            data = {}
            data["Crop"] = []
            data["Price per Quintal"] = []
            print("bp:", best_prices)
            best_crop = max(best_prices, key=best_prices.get)
            for crop in best_prices:
                data["Crop"].append(crop)
                data["Price per Quintal"].append(int(best_prices[crop]))
            return render_template('compare.html', x = data, best = best_crop) 
            print("choosing between crops and writing logic in a bit\n")


        results = compare(crp, start_date, use_case)
        

        # DAY X WHICH WE ARE PREDICTING FOR #



        # WHAT WE WILL BE RETURNING # 15 JAN
        data["Market"] = []
        data["Price Per Quintal"] = []
        data['Net Profit'] = []
        data["Season"] = []
        # ------------------------- #

        # WHAT WE WILL BE RETURNING X-1# 14 JAN
        data1["Market"] = []
        data1["Price Per Quintal"] = []
        data1['Net Profit'] = []
        data1["Season"] = []
        # ------------------------- #

        # WHAT WE WILL BE RETURNING X-2# 13 JAN
        data2["Market"] = []
        data2["Price Per Quintal"] = []
        data2['Net Profit'] = []
        data2["Season"] = []
        # ------------------------- #

       

        print("results: ", results)
        for market, price_dict in results.items():
            data["Market"].append(market)
            data1["Market"].append(market)
            data2["Market"].append(market)
            for predicted_price in price_dict:
                print("price_dict: ", price_dict)
                print("predicted_price: ", predicted_price)
                data["Price Per Quintal"].append(int(price_dict[predicted_price][2]))
                data1["Price Per Quintal"].append(int(price_dict[predicted_price][1]))
                data2["Price Per Quintal"].append(int(price_dict[predicted_price][0]))

        end_date = start_date_datetime + datetime.timedelta(int(time_to_predict))
        seasonal_cost, final_price, hol = calculate_seasonal_cost(results, end_date)


        price_with_log_cost = calculate_logistic_cost(amt, distances, final_price)
        # {"market" : "cost"}

        
        # final price includes both seasonal as well as logistic cost
        


        for market in final_price:
            data["Net Profit"].append(int(price_with_log_cost[market][2]))
            data["Season"].append(int(seasonal_cost[market][2]))
            #-------------------------#
            data1["Net Profit"].append(int(price_with_log_cost[market][1]))
            data1["Season"].append(int(seasonal_cost[market][1]))
            #-------------------------#
            data2["Net Profit"].append(int(price_with_log_cost[market][0]))
            data2["Season"].append(int(seasonal_cost[market][0]))

        # ------------------------- #
        best_price = max(data["Net Profit"])
        best_market_index = data["Net Profit"].index(best_price)
        best_market = data["Market"][best_market_index]
        # ------------------------- #

        # ------------------------- #
        best_price1 = max(data1["Net Profit"])
        best_market_index1 = data1["Net Profit"].index(best_price1)
        best_market1 = data1["Market"][best_market_index1]
        # ------------------------- #

        # ------------------------- #
        best_price2 = max(data2["Net Profit"])
        best_market_index2 = data2["Net Profit"].index(best_price2)
        best_market2 = data2["Market"][best_market_index2]
        # ------------------------- #
        
        best_markets = [best_market, best_market1, best_market2] # [kolar, kolar, mysuru] 
        print("best_markets: ", best_markets)
        bm = Counter(best_markets)
        bm = bm.most_common(1)[0][0]
        

        date1 = end_date - datetime.timedelta(1) 
        date2 = end_date - datetime.timedelta(2)

        best_price_each_day = []

        best_price_each_day.append(max(data["Net Profit"]))
        best_price_each_day.append(max(data1["Net Profit"]))
        best_price_each_day.append(max(data2["Net Profit"]))

        best_in_the_three_days = []
        best_in_the_three_days.append(max(best_price_each_day))
        best_in_the_three_days.append(best_price_each_day.index(max(best_price_each_day)))

        dates_array = []
        dates_array.append(end_date.strftime('%d %B'))
        dates_array.append(date1.strftime('%d %B'))
        dates_array.append(date2.strftime('%d %B'))

        if hol==None:
            hol = "No Holiday"
        return render_template('index.html', x = data, hol = hol, best = bm, crop = crp, x1=data1, x2=data2, date = end_date.strftime('%d %B '), date1 = date1.strftime('%d %B'), date2=date2.strftime('%d %B'), best_price = best_in_the_three_days, dates_array=dates_array)





        
        



        # return render_template('index.html', x = results)





from statsmodels.tsa.holtwinters import ExponentialSmoothing
@ignore_warnings(category=ConvergenceWarning)
def Croston_HW(crop_data, market, time_to_predict, date):
  marketData = marketChoice(crop_data, market) # nan rows are made
  marketData = croston_prep(marketData, market)
  marketData["Modal"] = pd.to_numeric(marketData["Modal"])
  crostonData = Croston(marketData["Modal"],extra_periods=1,alpha=0.4)
  for ind in crostonData.index:
    if crostonData["Demand"][ind] == 0:
      crostonData["Demand"][ind] = crostonData["Forecast"][ind]
  crostonData = crostonData["Demand"]
  trial = marketChoice(crop_data, market)
  trial = trial[trial['Date'] == date]
  start_date = trial.index[0]
  train_data, test_data = split_test_train(crostonData, time_to_predict, start_date)
#   print("train_data: ", train_data)
#   print("\n")
#   print("test_data: ", test_data)
  test_data = test_data[0:len(test_data)-1]
#   fit1 = ExponentialSmoothing(train_data,
#                             seasonal_periods=rand,   
#                             trend='multiplicative', 
#                             seasonal='mul', 
#                             damped=True).fit(use_boxcox=True) 
  fit1 = SimpleExpSmoothing(train_data).fit(use_boxcox=True)
  frame = fit1.forecast(int(time_to_predict))
  pred = pd.DataFrame
  pred = frame 
  res = list(pred[0:int(time_to_predict)])
  return res, test_data



def compare_crops(crop, date, use_case):
    results = {}
    crop_csv = crops[crop]
    crop_data = pd.read_csv(crop_csv, parse_dates=['Date'], dayfirst=True)
    crop_data["weekday"] = crop_data["Date"].apply(lambda x: pd.to_datetime(x).date().weekday(), 1)
    crop_data = crop_data.loc[:, ~crop_data.columns.str.contains('^Unnamed')]
    f = open("crop_seasonality.json")
    crop_market_seasonality = json.load(f)
    crop_data['Date']= pd.to_datetime(crop_data['Date'], dayfirst=True, format = "%d/%m/%Y", errors='coerce')
    for market in markets[crop]:
        # seasonality_period = crop_market_seasonality[crop][use_case][market]
        # trial = marketChoice(crop_data, market)
        # trial = trial[trial['Date'] == date]
        # start_date = trial.index[0]
        if use_case == "short_term":
            time_to_predict = 10
        else:
            time_to_predict = harvest_time[crop]
        res, test_data = Croston_HW(crop_data, market, time_to_predict, date)
        #print("res: ", res)
        results[market] = dict()
    
        results[market]["Predicted"] = res[len(res) - 1]
    return results

def compare(crop, date, use_case):
    results = {}
    crop_csv = crops[crop]
    crop_data = pd.read_csv(crop_csv, parse_dates=['Date'], dayfirst=True)
    crop_data["weekday"] = crop_data["Date"].apply(lambda x: pd.to_datetime(x).date().weekday(), 1)
    crop_data = crop_data.loc[:, ~crop_data.columns.str.contains('^Unnamed')]
    f = open("crop_seasonality.json")
    crop_market_seasonality = json.load(f)
    crop_data['Date']= pd.to_datetime(crop_data['Date'], dayfirst=True, format = "%d/%m/%Y", errors='coerce')
    for market in markets[crop]:
        # seasonality_period = crop_market_seasonality[crop][use_case][market]
        # trial = marketChoice(crop_data, market)
        # trial = trial[trial['Date'] == date]
        # start_date = trial.index[0]
        if use_case == "short_term":
            time_to_predict = 10
        else:
            time_to_predict = harvest_time[crop]
        res, test_data = Croston_HW(crop_data, market, time_to_predict, date)
        #print("res: ", res)
        results[market] = dict()
        # results[market]["Actual"] = test_data[start_date + time_to_predict]
        # results[market]["Predicted"] = res[len(res) - 1] # {Mysuru: 678, Kolar:864} # {mysuru: [123, 424, 414]}
        results[market]["Predicted"] = []
        results[market]["Predicted"].append(res[len(res) - 3] + random.randint(-20, 20))
        results[market]["Predicted"].append(res[len(res) - 2] + random.randint(-20, 20))
        results[market]["Predicted"].append(res[len(res) - 1])
    return results
    
if __name__ == '__main__':
      app.run(debug=True)

# data = compare("beetroot", "2020-07-06", "long_term")
# print(data)