from requests_futures.sessions import FuturesSession
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

session = FuturesSession(max_workers=100)
futures = np.array([make_request(session, url[1]) for url in player_list ])
results = [future.result().text for future in futures]

print('Player Stats Collected:')
print("Elapsed Time: %s" % (time.time() - start))
print('Processing Stats:')

for i in range(len(results)):

    script = soup(results[i], 'html.parser')
    name = script.find('h1', {'itemprop': 'name'}).span.text
    body = script.tbody

    season_totals = [[name] + [cat.text for cat in row.find_all('td')] for row in body.find_all('tr')]

    temp = []
    for season in season_totals:
        if 'Did' in season[3]:
            temp.append(season)
    for i in temp:
        season_totals.remove(i)

    with open('players_pergame.csv', 'a', newline='', encoding='utf-8') as file:
        write = csv.writer(file)
        write.writerows(season_totals)
    
print('Stats written to CSV')
print("Elapsed Time: %s" % (time.time() - start))



