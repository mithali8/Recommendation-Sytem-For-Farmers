
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
from numpy import isnan

def fill_weekdays(marketData):
	for i,j in marketData.iterrows():
		if(isnan(marketData.loc[i, 'weekday'])):
			marketData.loc[i,"weekday"] = (marketData.loc[i-1,"weekday"]+1)%7
	return marketData

def nan_rows(marketData):
	nanIndices = list()
	for i, j in marketData.iterrows():
			if pd.isnull(j['Modal']):
				nanIndices.append(i)
	return nanIndices

def croston_prep(marketData, market):
	marketData["Market"] = marketData["Market"].fillna(market)
	marketData["Min"] = marketData["Min"].fillna(0)
	marketData["Max"] = marketData["Max"].fillna(0)
	marketData["Modal"] = marketData["Modal"].fillna(0)
	return marketData

def marketChoice(data, market):
	marketData = pd.DataFrame()
	marketData = data[data['Market'] == market]
	marketData = marketData.drop(["Grade", "Arrivals", "Unit"], axis=1)
	marketData.set_index('Date', inplace=True)
	marketData = marketData.asfreq('D') 
	marketData = marketData.reset_index()
	marketData = fill_weekdays(marketData)
	# to_remove = holiday[market]
	# marketData = marketData[marketData["weekday"] != to_remove]
	return marketData

#@title #Croston's Model { display-mode: "form" }
def Croston(ts,extra_periods=1,alpha=0.4):
		d = np.array(ts) # Transform the input into a numpy array
		cols = len(d) # Historical period length
		d = np.append(d,[np.nan]*extra_periods) # Append np.nan into the demand array to cover future periods
		
		#level (a), periodicity(p) and forecast (f)
		a,p,f = np.full((3,cols+extra_periods),np.nan)
		q = 1 #periods since last demand observation
		
		# Initialization
		first_occurence = np.argmax(d[:cols]>0)
		a[0] = d[first_occurence]
		p[0] = 1 + first_occurence
		f[0] = a[0]/p[0]
# Create all the t+1 forecasts
		for t in range(0,cols):        
				if d[t] > 0:
						a[t+1] = alpha*d[t] + (1-alpha)*a[t] 
						p[t+1] = alpha*q + (1-alpha)*p[t]
						f[t+1] = a[t+1]/p[t+1]
						q = 1           
				else:
						a[t+1] = a[t]
						p[t+1] = p[t]
						f[t+1] = f[t]
						q += 1
			 
		# Future Forecast 
		a[cols+1:cols+extra_periods] = a[cols]
		p[cols+1:cols+extra_periods] = p[cols]
		f[cols+1:cols+extra_periods] = f[cols]
											
		df = pd.DataFrame.from_dict({"Demand":d,"Forecast":f,"Period":p,"Level":a,"Error":d-f})
		return df

def split_test_train(data, cultivation_time, start_date):
	x = start_date
	print("start_date", start_date)
	# x = len(data) - cultivation_time
	train_data = data[:x]
	test_data = data[x:]
	return train_data, test_data

from matplotlib import pyplot as plt
def plot_test_pred(frame, test_data):
	#plt.plot(frame, legend=True, label = "Predicted", color='red') # predicted
	#plt.plot(test_data, legend= True, label = "Test", color='green') # actual
	frame.plot(legend=True, label = "Predicted", color='red')
	test_data.plot(legend= True, label = "Test", color='green')
	plt.xlabel("Day Number")
	plt.ylabel("Modal Price")
	plt.show()

def plot_test_pred_train(test_data, train_data, pred):
	train_data.plot(legend=True,label='TRAIN')
	test_data.plot(legend=True,label='TEST',figsize=(12,8))
	pred.plot(legend=True,label='Prediction',figsize=(12,8))
	plt.ylabel("Modal price per Quintal")
	plt.xlabel("Days")