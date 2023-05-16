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
from functions import *
from mongo import get_mongo


def hypefly():     
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
  mongo_uri=get_mongo()
  client = pymongo.MongoClient(mongo_uri)
  db = client['ShopWIse']
  collection = db["Sneakers"]
  n=collection.count_documents({})


  #chrome options 
  options=get_options()


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

          price=format_price(product_text[1])
        
          product_price.append(price)

          product_url.append(children.get_attribute('href'))

          image=children.find_element(By.XPATH,'.//div/img')
          image_url.append(image.get_attribute('src'))

          pricehistory_element[str(current_date)]=(price)
          pricehistory.append(pricehistory_element)

          #query
          query = {"Product Url":product_url[len(product_url)-1]}
          query_document = collection.find_one(query)

          if(query_document):
            
            #check last date
            check=check_date(query_document=query_document)
            if(check):
                  print('Same date')
            else:
              
              
              collection.update_one(query,{'$push': {"PriceHistory": pricehistory_element} })
            collection.update_one(query,{'$set':{'CurrentPrice':price}})
                

            
            #print('updated')
          else:
            #new document
            document={
                'Title':product_text[0],
                'Description':product_text[0],
                'CurrentPrice':price,
                'PriceHistory':pricehistory,
                'ProductUrl': product_url[len(product_url)-1],
                'ImageUrl':image_url[len(image_url)-1],
                'Store':'hypefly',
                "AddedDate": datetime.datetime.today().replace(microsecond=0)

              
            }
            documents.append(document)



  driver.quit()

  if(len(documents)>0):
    collection.insert_many(documents)
    print('Uploaded')
  else:
    print("Already Full")