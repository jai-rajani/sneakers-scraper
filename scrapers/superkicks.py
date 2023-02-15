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
import pymongo
import datetime

current_date = datetime.datetime.now()



#set urls
url_main='https://superkicks.in/product-category/footwear/sneakers/?_sft_pa_gender=men&_sfm__price=0+30000'
urls=[]
urls.append(url_main)
for i in range(2,12):
    urls.append('https://superkicks.in/product-category/footwear/sneakers/?_sft_pa_gender=men&_sfm__price=0+30000&sf_paged='+str(i))

#initialise variables

product_desc=[]
product_title=[]
product_url=[]
product_price=[]
image_url=[]
documents=[]
j=0


#mongodb database
client = pymongo.MongoClient("mongodb+srv://jairajani:jairajani@shopwise.6twmxrd.mongodb.net/?retryWrites=true&w=majority")
db = client['ShopWIse']
collection = db["super_kicks"]
n=collection.count_documents({})


#chrome options 
options=webdriver.ChromeOptions()
#user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
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

    search=driver.find_elements(By.XPATH,'/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/main/div[2]/ul/li')


    for children in search:
        pricehistory=[]
        pricehistory_element={}
        j=j+1
    

        product_text=(children.text.split('\n'))
        #print(product_text)
        if(product_text[0]=='New Arrival' or product_text[0]=='Sale'):
            product_text.pop(0)
        #print(product_text)
        if(len(product_text)>3):
            product_text[2]=product_text[3]

        product_text[2]=product_text[2].replace('₹','')

       

        product_title.append(product_text[0])
        product_desc.append(product_text[1])
        product_price.append(product_text[2])
    
        
        link=children.find_element(By.XPATH,'.//div/a')
        product_url.append(link.get_attribute('href'))

        
        image=children.find_element(By.XPATH,'.//div/a/img')
        image_url.append(image.get_attribute('src'))

       
        pricehistory_element[str(current_date)]=(product_text[2])
        pricehistory.append(pricehistory_element)

        #query
        query = {"Product Url":product_url[len(product_url)-1]}
        query_document = collection.find_one(query)

        if(query_document):
          #update
          collection.update_one(query,{'$set':{'CurrentPrice':product_text[2]}})
          collection.update_one(query,{'$push': {"PriceHistory": pricehistory_element} })
          #print('updated')
        else:
          #new document
            document={
                'Title':product_text[0],
                'Description':product_text[1],
                'CurrentPrice':product_text[2],
                'PriceHistory':pricehistory,
                'Product Url': product_url[len(product_url)-1],
                'Image Url':image_url[len(image_url)-1],
                
            }
            documents.append(document)


    


print(j)
driver.quit()
if(j>=292 and len(documents)>0):
    collection.insert_many(documents)
    print('Uploaded')
else:
    print('Full')
