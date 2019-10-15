import sys
import requests
import csv
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
# from pyvirtualdisplay import Display
resultData={"data" : []}

def getdata():
	try:
		# display = Display(visible=0, size=(800, 600))
		# display.start()
		driver = webdriver.Chrome(executable_path='chromedriver')
		driver.get('https://www.exploit-db.com')                     #Request to url
		time.sleep(5)
		for page in range(0,10):
			data=driver.find_element_by_xpath('//*[@id="exploits-table_wrapper"]/div[2]/div')    #Get selenium object of whole table structure
			tableData=data.find_elements_by_tag_name('tr')                                       #Get All table rows information

			for iter in range(0,len(tableData)-1):
				try:
					link=tableData[iter].find_element_by_xpath('//*[@id="exploits-table"]/tbody/tr['+str(iter+1)+']/td[5]/a').get_attribute('href') # getting here title link
					time.sleep(2)
					driver2 = webdriver.Chrome(executable_path='chromedriver')
					time.sleep(2)
					driver2.get(link)
					try:
						cve = driver2.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/div/div/div/div[2]/h6').text 	# It will give text from this position of website
					except:
						cve = 'NOT FOUND'

					try:
						author =driver2.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[1]/h6/a').text
					except:
						author = 'NOT FOUND'

					try:
						title = driver2.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div/div[1]/div/div[1]/h1').text
					except:
						tile = 'NOT FOUND'

					try:
						downloadLink=driver2.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div/a[1]').get_attribute('href') 	 # It will give link from this position
					except:
						downloadLink = 'NOT FOUND'

					try:
						platform =driver2.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[3]/div/div[1]/div/div/div/div[1]/h6/a').text
					except:
						platform = 'NOT FOUND'

					print(cve, author,  title, downloadLink,platform)
					resultData["data"].append({
			                'Title':title,
			                'Platform':platform,
			                'Author':author,
			                'DownloadLink':downloadLink,
			                'CVE':cve
			            })
					driver2.close()

				except:
					print('Url doesnot open for document !!')
				time.sleep(4)

			time.sleep(5)
			next=driver.find_element_by_xpath('//*[@id="exploits-table_next"]/a')
			next.click()
			time.sleep(2)

		with open('data.json', 'w') as filepointer:
			json.dump(resultData, filepointer, indent=4)

		# display.stop()
	except:
		print('Website cant reached !! Try again')           #Here we can get information which is  no internet or problem to load the website

if __name__ == "__main__":
	getdata()                                                #program exicution start from here
