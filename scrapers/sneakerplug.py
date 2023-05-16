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
from functions import *

current_date = datetime.datetime.now()



#set urls
url_main='https://sneakerplug.co.in/collections/navbar-sneakers'
urls=[]
urls.append(url_main)
for i in range(2,3):
    urls.append('https://sneakerplug.co.in/collections/navbar-sneakers?page='+str(i))

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
#collection = db["super_kicks"]
collection = db["sneakers"]
n=collection.count_documents({})


options=get_options()


#start driver
driver=uc.Chrome(options=options)

for url in urls:
    driver.get(url)
    driver.implicitly_wait(35)

    search=driver.find_elements(By.XPATH,'//*[@id="js-product-ajax"]/div[1]/div')


    for children in search:
        pricehistory=[]
        pricehistory_element={}
        j=j+1
    

        desc_text=children.find_element(By.XPATH,'.//div/center/div/a')
        #print(product_text)
        product_title.append(desc_text.text)
        product_desc.append(desc_text.text)
        product_url.append(desc_text.get_attribute('href'))
        ''' print(product_title)
        print(product_url) '''

        price_text=children.find_element(By.XPATH,'.//div/center/div/div[2]')
        product_price.append(price_text.text)
       
        image=children.find_element(By.XPATH,'.//div/div/a/img')
        print(j,image.get_attribute('srcset'))
      

''' 
        
       

        product_title.append(product_text[0])
        product_desc.append(product_text[1])
        product_price.append(product_text[2])
    
        
       
       
        
       

       
        pricehistory_element[str(current_date)]=(product_text[2])
        pricehistory.append(pricehistory_element)

        #query
        query = {"Product Url":product_url[len(product_url)-1]}
        query_document = collection.find_one(query)

        if(query_document):
          #update
          check=check_date(query_document=query_document)
          if(check):
                print('Same date')
          #update

          else:
                print('New date')
                collection.update_one(query,{'$push': {"PriceHistory": pricehistory_element} })
          collection.update_one(query,{'$set':{'CurrentPrice':product_price[len(product_price)-1]}})
        else:
          #new document
            document={
                'Title':product_text[0],
                'Description':product_text[1],
                'CurrentPrice':product_text[2],
                'PriceHistory':pricehistory,
                'Product Url': product_url[len(product_url)-1],
                'Image Url':image_url[len(image_url)-1],
                'Store':'sneakerplug',
                "AddedDate": datetime.datetime.today().replace(microsecond=0)
                
            }
            documents.append(document) '''


    


print(j)
print(product_price)
print(image_url)

print(documents)
driver.quit()
''' if(j>=292 and len(documents)>0):
    collection.insert_many(documents)
    print('Uploaded')
else:
    print('Full') '''
