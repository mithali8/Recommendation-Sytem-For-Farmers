import pandas as pd
import numpy as np
import os



def clean_up(name):
	markets = ['BANGARPET', 'BINNY MILL (F&V)', 'C.R.NAGAR', 'CHICKBALLAPUR', 'DODDABALLAPUR', 'KOLAR', 'MYSURU', 'RAMANAGARA', 'CHANNAPATNA' ]

	df = pd.read_csv("/mnt/c/ch/farmers/combined-datasets/" + name) 

	df = df.fillna(method='ffill')
	df.drop(df[df['Market'] == ("Sub Total" or "Grand Total")].index, inplace = True) 
	df = df[df['Market'].isin(markets)]
	df.set_index(["Market"], inplace = True, append = True, drop = True) 
	   
	# resetting index 
	df.reset_index(inplace = True) 
	df = df.drop(['level_0'], axis = 1)
	df.to_csv("combined-datasets/" + name.split("_")[0] + "_cleaned.csv")

rootdir = "/mnt/c/ch/farmers/combined-datasets"
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
			clean_up(file)


