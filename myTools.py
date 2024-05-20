# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 09:26:05 2019

@author: Jerry
"""

import os,sqlite3
import requests,time,re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import tkinter as tk






def openDataBase(file_name,sql_table,overwrite=False):
    """建立資料庫"""
    if not os.path.exists(file_name) or overwrite:
        #刪除原本檔案並重新建立檔案
        if os.path.exists(file_name):
            os.remove(file_name)            
        conn=sqlite3.connect(file_name)
        try:
            cur=conn.cursor()
            #建立table
            cur.execute(sql_table)  
            conn.commit()  
               
        except Exception as e:
            print(e)
        else:
            print('write table success!')
            print('conn success!')
            return conn
      

    conn=sqlite3.connect(file_name) 
    print('conn success!')
    return conn


def get_soup(url,form_data=None):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    try:
        if form_data:
            resp=requests.post(url,headers=headers,data=form_data)
        else:
            resp=requests.get(url,headers=headers)
        
        if resp.status_code==200:
            resp.encoding='utf-8-sig'
            return BeautifulSoup(resp.text,'lxml')
        else:
            return resp.status_code
        
    except Exception as e:
        print(e)
        
    return None



def get_chrome(url,driver=r'C:\chromedriver\chromedriver'):
    try:
        chrome=webdriver.Chrome(driver)
        chrome.implicitly_wait(10)
        chrome.get(url)
        
        return chrome
    except Exception as e:
        print(e)
        
    return None





