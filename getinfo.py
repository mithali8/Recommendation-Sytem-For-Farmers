from selenium import webdriver
import unittest
import time
from selenium.webdriver.support.ui import Select
import shutil
import os


def beans():
	if(os.path.isdir("/mnt/c/ch/farmers/beans2019") == False):
		os.mkdir("beans2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('BEANS')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "beans2019/beans_" + str(i) + ".xls"
		shutil.move(source, destination) 
		 
	time.sleep(30)

def cucumber():
	if(os.path.isdir("/mnt/c/ch/farmers/cucumber2019") == False):
		os.mkdir("cucumber2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('CUCUMBAR')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "cucumber2019/cuc_" + str(i) + ".xls"
		shutil.move(source, destination) 
	 
	time.sleep(30)

def carrot():
	if(os.path.isdir("/mnt/c/ch/farmers/carrot2019") == False):
		os.mkdir("carrot2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('CARROT')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "carrot2019/carr_" + str(i) + ".xls"
		shutil.move(source, destination) 
		
	time.sleep(30)

def cabbage():
	if(os.path.isdir("/mnt/c/ch/farmers/cabbage2019") == False):
		os.mkdir("cabbage2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('CABBAGE')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "cabbage2019/cabb_" + str(i) + ".xls"
		shutil.move(source, destination) 
		
	time.sleep(30)

def lf():
	if(os.path.isdir("/mnt/c/ch/farmers/lf2019") == False):
		os.mkdir("lf2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('LADIES FINGER')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "lf2019/lf_" + str(i) + ".xls"
		shutil.move(source, destination) 
		 
	time.sleep(30)

def raddish():
	if(os.path.isdir("/mnt/c/ch/farmers/raddish2019") == False):
		os.mkdir("raddish2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('RADDISH')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "raddish2019/radd_" + str(i) + ".xls"
		shutil.move(source, destination) 
		
	time.sleep(30)

def beetroot():
	if(os.path.isdir("/mnt/c/ch/farmers/beet2019") == False):
		os.mkdir("beet2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('BEETROOT')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "beet2019/beet_" + str(i) + ".xls"
		shutil.move(source, destination) 
		
	time.sleep(30)

def tomato():
	if(os.path.isdir("/mnt/c/ch/farmers/tomato2019") == False):
		os.mkdir("tomato2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('TOMATO')
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	variety.select_by_value(str(5))
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "tomato2019/tom_" + str(i) + ".xls"
		shutil.move(source, destination) 
		
	time.sleep(30)

def capsicum():
	if(os.path.isdir("/mnt/c/ch/farmers/capsicum2019") == False):
		os.mkdir("capsicum2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('CAPSICUM')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "capsicum2019/caps_" + str(i) + ".xls"
		shutil.move(source, destination) 
		 
	time.sleep(30)

def greenc():
	if(os.path.isdir("/mnt/c/ch/farmers/greenc2019") == False):
		os.mkdir("greenc2019") 
	
	year = Select(driver.find_element_by_id('_ctl0_content5_ddlyear'))
	commodity = Select(driver.find_element_by_id('_ctl0_content5_ddlcommodity'))
	variety = Select(driver.find_element_by_id('_ctl0_content5_lstvariety'))
	year.select_by_visible_text('2020')
	commodity.select_by_visible_text('GREEN CHILLY')
	#variety.select_by_visible_text('Beans (Whole)')
	for i in range(13,25):
		month = Select(driver.find_element_by_id('_ctl0_content5_ddlmonth'))
		month.select_by_value(str(i-12))
		rep = driver.find_element_by_id("_ctl0_content5_viewreport")
		rep.click()
		get_cont = driver.find_element_by_id("_ctl0_content5_butexport")
		get_cont.click()
		time.sleep(5)
		source = os.path.abspath("/mnt/c/Users/aish2/Downloads/DateVarietyWiseReport_22_09_2020.xls")
		destination = "greenc2019/greenc_" + str(i) + ".xls"
		shutil.move(source, destination) 
		
	time.sleep(30)

	
if __name__ == '__main__':
	baseURL = "https://www.krishimaratavahini.kar.nic.in/reports/DateVarietyWiseReport.aspx"
	driver = webdriver.Chrome("/mnt/c/ch/farmers/chromedriver.exe")
	driver.get(baseURL)
	#beans()
	cucumber()
	#carrot()
	#cabbage()
	#greenc()
	#lf()
	#beetroot()
	#raddish()
	#capsicum()
	#tomato()

