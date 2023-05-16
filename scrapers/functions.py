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

#check if same shoe is being checked twice
def check_date(query_document):
        current_date = datetime.datetime.now()
        document_history=query_document['PriceHistory']
        document_price=document_history[len(document_history)-1]
        last_date=''
        for k,v in document_price.items():
            last_date=k
        last_date=last_date[:10]
        now_date_str=str(current_date)
        now_date=now_date_str[:10]
          
        if(last_date==now_date):
              return True
        else:
              return False

#set selenium options
def get_options():
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

      return options

#format integere value for price
def format_price(old_price):
      new_price=old_price.replace(',','')
      new_price=new_price.replace('₹','')
      new_price=new_price.replace(' ','')
      if(new_price.isdigit()):
              new_price=int(new_price)
      else:
              new_price=99999999
      return new_price
