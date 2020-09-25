import pandas as pd 
import os
def convert(filename):
    read_file = pd.read_html(filename)
    df = pd.DataFrame(read_file[0])
    df.to_csv (filename + ".csv",  
                  index = None, 
                  header=True)
                
    


import os
rootdir = '/mnt/c/ch/farmers'

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.endswith('.xls'):
			filename = os.path.join(subdir, file)
			convert(filename)
			print(filename)
			print("\n\n")
		# print(file)