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
from mongo import get_mongo


def vegnonveg():

      current_date = datetime.datetime.now()

      url_main='https://www.vegnonveg.com/footwear'

      urls=[]
      urls.append(url_main)


      product_desc=[]
      product_title=[]
      product_url=[]
      product_price=[]
      image_url=[]
      documents=[]

      scroll_pause_time = 3




      #chrome options 
      options=get_options()
      #mongdb
      mongo_uri=get_mongo()
      client = pymongo.MongoClient(mongo_uri)
      db = client['ShopWIse']
      collection = db["sneakers"]
      n=collection.count_documents({})


      #start driver
      driver=uc.Chrome(options=options)
      driver.get(url_main)
      screen_height = driver.execute_script("return window.screen.height;")
      i = 4

      while True:
                  driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
                  i += 1
                  time.sleep(scroll_pause_time)
                  
                  scroll_height = driver.execute_script("return document.body.scrollHeight;")  
                  if (screen_height) * i > scroll_height:
                        break


      driver.implicitly_wait(35)
      j=0
      search=driver.find_elements(By.XPATH,'//*[@id="products"]/div')
      for children in search:
            
            pricehistory=[]
            pricehistory_element={}

            j=j+1
            full_text=children.find_element(By.XPATH,'.//a/div[2]/div')
            product_text=(full_text.get_attribute('innerText'))
            product_text=product_text.strip()
            product_text=product_text.split('\n')
            for i in range(0,len(product_text)):
                  product_text[i]=product_text[i].strip()
            #print(product_text[5])
            product_text[5]=format_price(product_text[5])
            #print(product_text[5])
            
                  
            product_title.append(product_text[0])
            product_desc.append(product_text[3])
            product_price.append(product_text[5])  
            
            

            link_text=children.find_element(By.XPATH,'.//div/a')
            product_url.append(link_text.get_attribute('href'))


            image_text=children.find_element(By.XPATH,'.//div/a/div/img')
            image_url.append(image_text.get_attribute('src'))     


            pricehistory_element[str(current_date)]=(product_text[5])
            pricehistory.append(pricehistory_element)
            #query
            query = {"Product Url":product_url[len(product_url)-1]}
            query_document = collection.find_one(query)

            if(query_document):
                  check=check_date(query_document=query_document)
                  if(check):
                        print()
                  #update

                  else:
                        print('New date')
                        collection.update_one(query,{'$push': {"PriceHistory": pricehistory_element} })
                  collection.update_one(query,{'$set':{'CurrentPrice':product_price[len(product_price)-1]}})
                        #print('updated')
            else:
                        #new document
                  document={
                        'Title':product_text[0],
                        'Description':product_text[3],
                        'CurrentPrice':product_text[5],
                        'PriceHistory':pricehistory,
                        'Product Url': product_url[len(product_url)-1],
                        'Image Url':image_url[len(image_url)-1],
                        'Store':'vegnonveg',
                        "AddedDate": datetime.datetime.today().replace(microsecond=0)
                        
                  }
                  documents.append(document)



      driver.quit()
      print(j)
      #print(documents)

      if(len(documents)>0 and j>=610 ):
            collection.insert_many(documents)
            print('Uploaded')
      else:
            print('Full')


if __name__=='__main__':
      vegnonveg()
    
