from requests_futures.sessions import FuturesSession
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from threading import Thread
from bs4 import BeautifulSoup as soup
import numpy as np 
import time
import requests
import string
import csv

start = time.time()


def make_request(session, url):
    future = session.get(url)
    return future


url_list = []

for letter in list(string.ascii_lowercase):

    if letter == 'x':
        pass
    else:
        url = 'https://www.basketball-reference.com/players/' + letter
        url_list.append(url)

#print(url_list)

session = FuturesSession(max_workers=32)
futures = np.array([make_request(session, url) for url in url_list])
results = [future.result().text for future in futures]

player_list = []

for i in range(len(results)):

    body = soup(results[i], 'html.parser').tbody
    players = body.find_all('tr')
    
    for player in players:
        
        name = player.find('a').text
        start_year = int(player.find('td', {'data-stat': 'year_min'}).text)
        url = 'https://www.basketball-reference.com' + player.find('a')['href']

        if start_year >= 1996:
            player_list.append([name, url])

print('Player List & URL Collected')
print("Elapsed Time: %s" % (time.time() - start))

number_of_threads = 5

threads = []

DRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'

from joblib import Parallel, delayed
import threading    

def get_stats(player):

    names = player[0]
    url = player[1]

    options = Options()
    options.page_load_strategy = 'none'
    try:
        driver = drivers[threading.current_thread().name]
    except KeyError:
        drivers[threading.current_thread().name] = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        driver = drivers[threading.current_thread().name]

    driver.get(url)

    table = driver.find_element_by_xpath('//*[@id="totals"]/tbody')

    try:
        all_star = driver.find_element_by_xpath('//*[@id="all_star"]/tbody')
        years = [year.text for year in all_star.find_elements_by_xpath('./tr/th')]
    except:
        years = []

    season_totals = []
    #Get season totals by row
    for row in table.find_elements_by_xpath('./tr'):

        season = [td.text for td in row.find_elements_by_xpath("./td")]
        season.insert(0, row.find_element_by_xpath('./th').text)

        if len(season) == 32:
            season.pop(30)
        elif len(season) == 30:
            season.append('0')

        if season[0] in years:
            season.append('Yes')
        else:
            season.append('No')

        season.insert(0, names)

        for i in range(len(season)):
            if season[i] == '':
                season[i] = '0'
        season_totals.append(season)
    #Check if all star


    #Write to file
    with open('players_total.csv', 'a', newline='', encoding='utf-8') as file:
        write = csv.writer(file)
        write.writerows(season_totals)

drivers = {}
Parallel(n_jobs=2, backend="threading")(delayed(get_stats)(player) for player in player_list)
for driver in drivers.values():
    driver.quit()

    
print('Stats written to CSV')
print("Elapsed Time: %s" % (time.time() - start))



