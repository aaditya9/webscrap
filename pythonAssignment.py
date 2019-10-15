import requests
import json
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time

def getdata():
	result={"data" : []}
	try:
		for page in range(0,10):												# loop
			driver = webdriver.Chrome(executable_path='chromedriver').set_window_position(-0, 0)
			driver.get('https://www.exploit-db.com')
			time.sleep(5) 														#Waiting to render all data on site
			tableData=[]
			try:
				data=driver.find_element_by_xpath('//*[@id="exploits-table_wrapper"]/div[2]/div').set_window_position(-0, 0) # we get tbody data
				tableData=data.find_elements_by_tag_name('tr')
			except:
				print('Server Down')

			for iter in range(0,len(tableData)-1):
				try:
					link=tableData[iter].find_element_by_xpath('//*[@id="exploits-table"]/tbody/tr['+str(iter+1)+']/td[5]/a').get_attribute('href') # getting here title link
					# driver2 = webdriver.Chrome(executable_path='chromedriver')
					driver2 = webdriver.Chrome(executable_path='chromedriver').set_window_position(-0, 0)
					driver2.get(link)
					time.sleep(2)												#Waiting to render all data on site


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

					# print(cve, author,  title, downloadLink,platform)
					result["data"].append({
			                'Title':title,
			                'Platform':platform,
			                'Author':author,
			                'DownloadLink':downloadLink,
			                'CVE':cve
			            })
					driver2.close()
				except:
					print('Url doesnot open for document !!')
			try:
				driver.find_element_by_xpath('//*[@id="exploits-table_next"]/a').click()
				time.sleep(2)
			except:
				print('Url for next page link is not getting!')

		with open('data.json', 'w') as filepointer:
			json.dump(result, filepointer, indent=4)

	except Exception as error:
		print('Website is not loading')
		print(error)
		# return

if __name__ == "__main__":
	getdata() 																	# Call the function which gives scrap of site
