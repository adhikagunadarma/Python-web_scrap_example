# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 21:03:20 2021

@author: Adhika.Gunadarma
"""

class ShopeeProduct:
    def __init__(self, name, price, sold, href, location):
        self.name = name
        self.price = price
        self.sold = sold
        self.href = href
        self.location = location

import os
import selenium
from selenium import webdriver
import time
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install())

search_url = "https://shopee.co.id/search?keyword={searchQuery}&maxPrice={maxPriceQuery}&minPrice={minPriceQuery}&noCorrection=true&page=0"
driver.get(search_url.format(searchQuery="poco", maxPriceQuery="200000000",minPriceQuery="1000"))


time.sleep(5)#sleep_between_interactions
#Scroll to the end of the page
pageHeight = driver.execute_script("return document.body.scrollHeight")


driver.execute_script("window.scrollTo(0,document.body.scrollHeight )")


os.chdir('D://anaconda//ml-learning//web-scrapping//dataset-shopee')
baseDir=os.getcwd()

listProductsHref =  driver.find_elements_by_xpath("//a[contains(@data-sqe,'link')]")
listProductsName =  driver.find_elements_by_xpath("//div[contains(@class,'_1NoI8_')]")
listProductsPrice =  driver.find_elements_by_xpath("//div[contains(@class,'_1DGuEV')]")
listProductsSold =  driver.find_elements_by_xpath("//div[contains(@class,'_245-SC')]")
#listProductsRating =  driver.find_elements_by_xpath("//div[contains(@class,'shopee-rating-stars__stars')]")
listProductsLocation =  driver.find_elements_by_xpath("//div[contains(@class,'_41f1_p')]")


#print(listProductsPrice[0].get_tag_name()) # ngambil tag span buat dimasukin ke dalem class price
print (len(listProductsHref))
listProducts = list()
if (len(listProductsHref) == len(listProductsName) == len(listProductsPrice) == len(listProductsSold) == len(listProductsLocation)):
    for i in range(0,len(listProductsHref)):
          name = listProductsName[i].text
          sold = listProductsSold[i].text
          location = listProductsLocation[i].text
          if listProductsHref[i].get_attribute('href'):
              href = listProductsHref[i].get_attribute('href')
         
          print (name,sold,location, href)    


# dari data ini bisa di filter untuk mencari barang dengan produk terjual dan rating penjual tertinggi
# produk href = a class _38_74r
# produk name = div class _1NoI8_ _2xHE6C _1co5xN
# produk price = div class _1w9jLI _1DGuEV _2ZYSiu
# produk terjual = div class _245-SC
# produk rating = div class shopee-rating-stars__stars
# kota penjual = _41f1_p