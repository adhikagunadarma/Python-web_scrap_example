# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:50:40 2021

@author: Adhika.Gunadarma
"""

import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install())

search_url="https://www.instagram.com" 
ig_username="adhikagunadarma"
ig_pass="whitz4872"

driver.get(search_url)
time.sleep(10)#sleep_between_interactions

#username = driver.find_element_by_xpath("//form[@id='loginForm']/input[1]")
#password = driver.find_element_by_xpath("//form[@id='loginForm']/input[2]")

username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')

loginButton = driver.find_element_by_xpath("//button[contains(@class,'L3NKy')]")
username.send_keys(ig_username)
password.send_keys(ig_pass)
loginButton.send_keys(Keys.ENTER)
time.sleep(5)#sleep_between_interactions

skipButton = driver.find_element_by_xpath("//button[contains(@class,'yWX7d')]")
skipButton.send_keys(Keys.ENTER)
time.sleep(5)#sleep_between_interactions


#Scroll to the end of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)#sleep_between_interactions


#Locate the images to be scraped from the current page 
imgResults = driver.find_elements_by_xpath("//img[contains(@class,'FFVAD')]") #Q4LuWD itu format class images dr google
totalResults=len(imgResults)

img_urls = set()
for result in imgResults:
            if result.get_attribute('src') and 'https' in result.get_attribute('src'):
                img_urls.add(result.get_attribute('src'))


        
os.chdir('D://anaconda//ml-learning//web-scrapping//dataset-ig-testing')
baseDir=os.getcwd()

for i, url in enumerate(img_urls):
    file_name = f"{i:150}.jpg"    
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")

    try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            
            file_path = os.path.join(baseDir, file_name)
            
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SAVED - {url} - AT: {file_path}")
    except Exception as e:
            print(f"ERROR - COULD NOT SAVE {url} - {e}")