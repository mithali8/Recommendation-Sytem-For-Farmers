import csv

with open('hols.csv', mode='r') as infile:
    reader = csv.reader(infile)
    
    mydict = {rows[0].strip("\ufeff"):rows[2] for rows in reader}
import datetime
from datetime import date 
import holidays 
  
in_holidays = holidays.HolidayBase() 

for i in mydict:
	if(i):
	#i = i.strip("\ufeff")
		in_holidays.append({datetime.datetime.strptime(i, '%Y-%m-%d').strftime('%m/%d/%y'):str(mydict[i])})


#print(in_holidays.get('21-02-2021'))

with open('muhurat.csv', mode='r') as infile2:
    reader2 = csv.reader(infile2)
    
    mydict2 = {rows[0].strip(): "muh" for rows in reader2}
    m_holidays = holidays.HolidayBase() 

for j in mydict2:
	#print(mydict2)
	if(j):
	
		m_holidays.append({datetime.datetime.strptime(j, '%d-%m-%Y').strftime('%m/%d/%y'):str(mydict2[j])})
