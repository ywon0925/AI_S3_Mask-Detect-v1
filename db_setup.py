import csv
import os
import requests
import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient


def get_images_url(driver, search_url, search_item):
   
    # Open brower with url for items image
    driver.get(search_url.format(q=search_item))

    # Scroll page to load more images
    for i in range(3):
        scroll_page(driver)

    # Find Image as node of XML on the page
    img_xml = driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]")
    totalResults = len(img_xml)
    print(totalResults)

    #Click on Image and find actual Source Link to download iamge
    img_urls = set()
    for i in range(totalResults):
        img=img_xml[i]
        try:
            img.click()     # Click on image to get bigger/actual image 
            time.sleep(2)   # Wait for page to load
            actual_images = driver.find_elements(By.CSS_SELECTOR,'img.n3VNCb')  # Get Elements that matches css_selector
            
            # Find Real Element with proper src link
            for actual_img in actual_images:
                if actual_img.get_attribute('src') and 'http' in actual_img.get_attribute('src') and 'encrypted' not in actual_img.get_attribute('src'):
                    img_urls.add(actual_img.get_attribute('src'))   # add to set
        except Exception:
            pass
    
    # Return set of images url
    return img_urls

def scroll_page(driver):
    """Scroll to bottom of page and wait for page to load"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 


def write_to_file(img_urls, filename):
    """Receive set of image url and write into text file"""
    with open(filename, 'a') as f:
        for url in img_urls:
            print(url)
            f.write(url)
            f.write('\n')

def file_to_dict(filename):
    url_dict_list = []
    with open(filename) as f:
        for row in f:
            temp_dict = {}
            temp_dict['URL'] = row
            url_dict_list.append(temp_dict)
    return url_dict_list


def upload_to_mongodb(url_dict_list, collection_name):
    HOST = 'cluster0.n76ap.mongodb.net'
    USER = 'admin'
    PASSWORD = ''
    DATABASE_NAME = 'myFirstDatabase'
    COLLECTION_NAME = collection_name
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    collection.insert_many(url_dict_list)
    print('Data added to MongoDB successfully')
    

if __name__ == "__main__":
    # Option to make brower run in background (No GUI)
    options = Options()
    options.headless = True
    # Install web driver needed for scraping
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # URL to search
    search_url = "https://www.google.com/search?q={q}&tbm=isch"

    # Search list & file to save to
    search_item = ['face+mask+man', 'face+mask+woman', 'face+mask+kid', '마스크+남자', '마스크+여자', '마스크+낀']
    mask_file = 'mask.txt'
    
    # Search list & file to save to
    search_item_2 = ['selfie', '셀카']
    no_mask_file = 'no-mask.txt'
    
    
    # Search img of ppl w/ mask
    for item in search_item:
        img_urls = get_images_url(driver, search_url, item)
        write_to_file(img_urls, mask_file)
    
    # Search img of ppl selfies
    for item in search_item_2:
        img_urls = get_images_url(driver, search_url, item)
        write_to_file(img_urls, no_mask_file)
    
    # END Session    
    driver.quit()
    
    # Get Dictinarly list of Image URLs
    url_list = file_to_dict(mask_file)
    # Upload to mongoDB
    upload_to_mongodb(url_list, 'maskURL')
    
    # Get Dictinarly list of Image URLs
    url_list = file_to_dict(no_mask_file)
    # Upload to mongoDB
    upload_to_mongodb(url_list, 'nomaskURL')
    