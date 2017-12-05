# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:56:05 2017

@author: jarre14
"""

import bs4 
from bs4 import BeautifulSoup as BS
from urllib.request import urlretrieve
from urllib.request import urlopen
import re
import pandas as pd

from setup import *

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
def get_data(pageName):
    pattern = re.compile(r'/\w+\?')
    matchNumber = pattern.findall(pageName)
    matchNumber = matchNumber[0][1:-1]
    print(matchNumber)
    
    wd = webdriver.Firefox(executable_path=r'C:\Users\jarre14\Downloads\geckodriver-v0.19.1-win64\geckodriver.exe')
    # 1 second wait for the driver to initialize before using it
    time.sleep(1)
    wd.get(pageName)
    wd.wait = WebDriverWait(wd, 10)
    try:
        win = wd.wait.until(EC.presence_of_element_located((By.ID, "overview")))
        # 2 second wait for the information to populate
        time.sleep(4)
        kills = win.find_elements_by_class_name('champion-kills')
        circles = kills[0].find_elements_by_tag_name('circle')
        kill_locations = [[x.get_attribute('cx'), x.get_attribute('cy'), x.get_attribute('class')] for x in circles]
        print(kill_locations[0])
        
        #x and y values are based on a 289 by 289 pixel grid with 0 in the top left corner
        #picture of the map in project folder
        names = ['x_coordinate', 'y_coordinate', 'details']
        kill_df = pd.DataFrame(kill_locations, columns=names)
        print(kill_df.iloc[0:4])
        kill_df.to_csv('\Game_Stats\{}_Kills.csv'.format(matchNumber))
        
        stats_win = wd.wait.until(EC.presence_of_element_located((By.ID, "stats")))
        #time.sleep(1)
        stats = stats_win.find_elements_by_id('stats-body')
        print(len(stats))
        #header = stats[0].find_elements_by_id('grid-header-row-439')
        #team100 = header[0].find_elements_by_class_name('team-100')
        #team200 = header[0].find_elements_by_class_name('team-200')
        
        #print(team100[0])
        
        grid_rows = stats[0].find_elements_by_class_name('grid-row')
        
        print(len(grid_rows))
        rows = [x.find_elements_by_class_name('view')[0] for x in grid_rows]
        data = [x.find_elements_by_class_name('grid-cell') for x in grid_rows]
        print(rows[0].get_attribute('innerText'))
        print(data[0][0].get_attribute('innerText'))
        labels = [x.get_attribute('innerText') for x in rows]
        row_data = [[x.get_attribute('innerText') for x in y] for y in data]
    
        row_data[3] = [int(x == '●') for x in row_data[3]]
        for i,row in enumerate(row_data):
            row.insert(0, labels[i])
            print(row)
        row_names = ["Stat","Champion_1","Champion_2","Champion_3","Champion_4","Champion_5","Champion_6","Champion_7","Champion_8","Champion_9","Champion_10"]
        #print(len(team100))
        #print(len(team200))
        print(len(grid_rows))
        print(row_data[3])
        
        df = pd.DataFrame(row_data, columns=row_names)
        print(df.iloc[0:4])
        df.to_csv('\Game_Stats\{}_Stats.csv'.format(matchNumber))
    except TimeoutException:
        print('window not found')
    wd.quit()

pageName1 = 'http://matchhistory.na.leagueoflegends.com/en/#match-details/TRLH1/30030?gameHash=fbb300951ad8327c&tab=overview'
pageName2 = 'http://matchhistory.na.leagueoflegends.com/en/#match-details/TRLH1/30054?gameHash=055b17da8456fdc8'
game_data = Dataframe_From_CSV('LeagueofLegends.csv')

for x in game_data['MatchHistory']:
        get_data(x)

#ls = [pageName1, pageName2]
#for page in ls:
#    get_data(page)













