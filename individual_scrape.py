import threading
import time
import json 
from selenium import webdriver 
start = time.time()

def individual_scrape(player):

    name = player[0]
    url = player[1]

    DRIVER_PATH = './chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    #url = 'https://www.basketball-reference.com/players/h/headlu01.html'
    driver.get(url)

    table = driver.find_element_by_xpath('//*[@id="totals"]/tbody')

    
    season_totals = [row.text.split(' ') for row in table.find_elements_by_xpath('./tr')]
    driver.close()

    player_totals[name] = season_totals
    print(name, (time.time() - start))
    return season_totals

with open('player_urls.txt') as f:
    player_urls = [i.strip('\n').split('|')  for i in f.readlines()]

player_totals = {}

# threads = [threading.Thread(target=individual_scrape(player)) for player in player_urls]

# for thread in threads:
#     time.sleep(0.05)
#     thread.start()
# for thread in threads:
#     thread.join()


for player in player_urls:

    player_totals[player[0]] = individual_scrape(player)

print("Elapsed Time: %s" % (time.time() - start))
print(player_totals)
print(len(player_totals))


f = open('data.json', 'w')
json.dump(player_totals, f)
f.close()

