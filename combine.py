import os
import glob
import pandas as pd

import os





def combine(dirname):
	os.chdir("/mnt/c/ch/farmers/" + dirname)
	extension = 'csv'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

	all_filenames = sorted(all_filenames, key = lambda x : int(x.split("_")[1].split(".")[0]))
	#print(all_filenames)
	combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
	#export to csv
	combined_csv.to_csv(dirname + "_combined.csv", index=False, encoding='utf-8-sig')

rootdir = '/mnt/c/ch/farmers'

for subdir, dirs, files in os.walk(rootdir):
	
	
	directories = dirs
	break
for directory in directories[1:]:
	if directory.endswith('2019'):
		#print(directory)
		combine(directory)
			#print(filename)
			#print("\n\n")
