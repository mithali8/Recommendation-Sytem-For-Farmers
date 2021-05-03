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


from statsmodels.tsa.holtwinters import ExponentialSmoothing
def Croston_HW(crop_data, market, rand, check):
  marketData = marketChoice(crop_data, market) # nan rows are made
  marketData = croston_prep(marketData, market)
  marketData["Modal"] = pd.to_numeric(marketData["Modal"])
  crostonData = Croston(marketData["Modal"],extra_periods=1,alpha=0.4)
  for ind in crostonData.index:
    if crostonData["Demand"][ind] == 0:
      crostonData["Demand"][ind] = crostonData["Forecast"][ind]
  crostonData = crostonData["Demand"]
  # print("crostondata: ", crostonData)
  train_data, test_data = split_test_train(crostonData, 60, 36)
  print("train data :", train_data)
  test_data = test_data[0:len(test_data)-1]
  fit1 = ExponentialSmoothing(train_data,
                            seasonal_periods=rand,   
                            trend='multiplicative', 
                            seasonal='mul', 
                            damped=True).fit(use_boxcox=True)
  frame = fit1.forecast(60)
  pred = pd.DataFrame
  pred = frame 
  res = list(pred[0:60])
  if(check == 1):
    plot_test_pred(frame, test_data)
    
    
    plot_test_pred_train(test_data, train_data, pred[0:len(test_data)])
    metrics(test_data, res)
  
  else:
    return test_data, res

  

beetData = pd.read_csv('capsicum19-20.csv', parse_dates=['Date'], dayfirst=True)
beetData.head()
beetData["weekday"] = beetData["Date"].apply(lambda x: pd.to_datetime(x).date().weekday(), 1)
beetData.head(7)
beetData = beetData.loc[:, ~beetData.columns.str.contains('^Unnamed')]
beetData['Date']= pd.to_datetime(beetData['Date'], dayfirst=True, format = "%d/%m/%Y", errors='coerce')
 
# Check the format of 'Date' column
# beetData.info()
test_data, res = Croston_HW(beetData, "DODDABALLAPUR", 35, 0)
print("test_data: ", test_data)
print("\n")
print("res: ", res)