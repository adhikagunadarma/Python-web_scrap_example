
import selenium
import time
import io
import requests
import os

from PIL import Image
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager # perlu pip instal selenium dan webdrivemanager ya
opts = webdriver.ChromeOptions()
opts.headless =True

os.chdir('D://anaconda//ml-learning//web-scrapping')

driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)
#search_url = "https://www.google.com/search?q={q}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568"
#driver.get(search_url.format(q='Dog'))

def scroll_to_end(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)#sleep_between_interactions
    
    
#no license issues

def getImageUrls(name,driver):
    
    search_url = "https://www.instagram.com/explore/tags/{q}/"
    driver.get(search_url.format(q=name))
    img_urls = set()
    
        
    scroll_to_end(driver)
        
    #Locate the images to be scraped from the current page 
    imgResults = driver.find_elements_by_xpath("//img[contains(@class,'FFVAD')]") #Q4LuWD itu format class images dr google
  
    for result in imgResults:
        if result.get_attribute('src') and 'https' in result.get_attribute('src'):
            img_urls.add(result.get_attribute('src'))
                        
            
                  
    return img_urls


def downloadImages(folder_path,file_name,url):
    try:
        image_content = requests.get(url).content
    except Exception as e:
            print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")
    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
       
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SAVED - {url} - AT: {file_path}")
    except Exception as e:
        print(f"ERROR - COULD NOT SAVE {url} - {e}")
        
        
def saveInDestFolder(searchNames,destDir,driver):
    for name in list(searchNames):
        path=os.path.join(destDir,name)
        if not os.path.isdir(path):
            os.mkdir(path)
        print('Current Path',path)
        totalLinks=getImageUrls(name,driver)
        print('totalLinks',totalLinks)

        if totalLinks is None:
                print('images not found for :',name)
                continue
        else:
                for i, link in enumerate(totalLinks):
                    file_name = f"{i:150}.jpg"
                    downloadImages(path,file_name,link)
            
searchNames=['Halloween','Geeks'] 
destDir=f'./dataset-ig-hashtags/'

saveInDestFolder(searchNames,destDir,driver)