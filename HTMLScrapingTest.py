# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:56:05 2017

@author: jarre14
"""

import bs4 
from bs4 import BeautifulSoup as BS
from urllib.request import urlretrieve
from urllib.request import urlopen

pageName = 'http://matchhistory.na.leagueoflegends.com/en/#match-details/TRLH1/30030?gameHash=fbb300951ad8327c&tab=overview'
#page = urlopen(pageName).read()
#print(page)
#soup = BS(page, 'html.parser')
#print(soup)

#name_box = soup.find('div', attrs={'class': 'section-wrapper-content-wrapper'})
#name_box = soup.find('div', attrs={'class': 'main'})
#print(name_box)
#name = name_box.text.strip()
#print(name)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ******Must have geko driver, selenium, and a new version of fireforx installed*********

wd = webdriver.Firefox(executable_path=r'C:\Users\jarre14\Downloads\geckodriver-v0.19.1-win64\geckodriver.exe')
# 1 second wait for the driver to initialize before using it
time.sleep(1)
wd.get(pageName)
wd.wait = WebDriverWait(wd, 10)
try:
    win = wd.wait.until(EC.presence_of_element_located((By.ID, "map-314")))
    # 2 second wait for the information to populate
    time.sleep(2)
    kills = win.find_elements_by_class_name('champion-kills')
    circles = kills[0].find_elements_by_tag_name('circle')
    kill_locations = [[x.get_attribute('cx'), x.get_attribute('cy'), x.get_attribute('class')] for x in circles]
    print(kill_locations[0])
    
    stats_win = wd.wait.until(EC.presence_of_element_located((By.ID, "stats")))
    time.sleep(1)
    stats = stats_win.find_elements_by_id('stats-body')
    print(len(stats))
    header = stats[0].find_elements_by_id('grid-header-row-439')
    team100 = header[0].find_elements_by_class_name('team-100')
    team200 = header[0].find_elements_by_class_name('team-200')
    
    grid_rows = stats[0].find_elements_by_class_name('grid-row')
    
    print(len(grid_rows))
    rows = [x.find_elements_by_class_name('view')[0] for x in grid_rows]
    data = [x.find_elements_by_class_name('grid-cell') for x in grid_rows]
    print(rows[0].get_attribute('innerText'))
    print(data[0][0].get_attribute('innerText'))
    labels = [x.get_attribute('innerText') for x in rows]
    row_data = [[x.get_attribute('innerText') for x in y] for y in data]
    print(len(team100))
    print(len(team200))
    print(len(grid_rows))
    print(labels[0], row_data[0])
    
except TimeoutException:
    print('window not found')
wd.quit()