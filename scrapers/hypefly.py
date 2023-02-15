import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import undetected_chromedriver as uc
import os
import pandas as pd
import pymongo
import datetime

current_date = datetime.datetime.now()

    

url_main='https://hypefly.co.in/collections/all-sneakers'

urls=[]
urls.append(url_main)


product_desc=[]
product_title=[]
product_url=[]
product_price=[]
image_url=[]
documents=[]
j=0

#mongdb
client = pymongo.MongoClient("mongodb+srv://jairajani:jairajani@shopwise.6twmxrd.mongodb.net/?retryWrites=true&w=majority")
db = client['ShopWIse']
collection = db["hypefly"]
n=collection.count_documents({})


#chrome options 
options=webdriver.ChromeOptions()

user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--window-size=1920x1480')


#start driver
driver=uc.Chrome(options=options)


for url in urls:
    driver.get(url)
    driver.implicitly_wait(35)

    search=driver.find_elements(By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/a')


    for children in search:
        j=j+1
        
        pricehistory=[]
        pricehistory_element={}

        #get text
        product_text=(children.text.split('\n'))
        product_text[1]=product_text[1].replace('from Rs. ','')
        product_desc.append(product_text[0])
        product_price.append(product_text[1])
        product_url.append(children.get_attribute('href'))

        image=children.find_element(By.XPATH,'.//div/img')
        image_url.append(image.get_attribute('src'))

        pricehistory_element[str(current_date)]=(product_text[1])
        pricehistory.append(pricehistory_element)

        #query
        query = {"Product Url":product_url[len(product_url)-1]}
        query_document = collection.find_one(query)

        if(query_document):
          #update
          collection.update_one(query,{'$set':{'CurrentPrice':product_text[1]}})
          collection.update_one(query,{'$push': {"PriceHistory": pricehistory_element} })
          #print('updated')
        else:
          #new document
          document={
              'Title':product_text[0],
              'Description':product_text[0],
              'CurrentPrice':product_text[1],
              'PriceHistory':pricehistory,
              'Product Url': product_url[len(product_url)-1],
              'Image Url':image_url[len(image_url)-1],
            
          }
          documents.append(document)

        

driver.quit()

if(len(documents)>0):
  collection.insert_many(documents)
  print('Uploaded')
else:
  print("Already Full")