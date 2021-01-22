import threading
import time
import json 
from selenium import webdriver 
import csv
start = time.time()

def individual_scrape(player):

    name = player[0]
    url = player[1]

    # DRIVER_PATH = './chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    #url = 'https://www.basketball-reference.com/players/h/headlu01.html'
    driver.get(url)

    try:
        table = driver.find_element_by_xpath('//*[@id="totals"]/tbody')
        season_totals = [[name] + row.text.split(' ') for row in table.find_elements_by_xpath('./tr')]

        with open('player_data.csv', 'a',newline='') as file:
            write = csv.writer(file)
            write.writerows(season_totals)

        #season_totals = [row.text.split(' ') for row in table.find_elements_by_xpath('./tr')]
        #driver.close()

        #player_totals[name] = season_totals
        print(name, (time.time() - start))
        return file
    except:
        return 'fail'

with open('player_urls.txt') as f:
    player_urls = [i.strip('\n').split('|')  for i in f.readlines()]

player_totals = {}

# threads = [threading.Thread(target=individual_scrape(player)) for player in player_urls]

# for thread in threads:
#     time.sleep(0.05)
#     thread.start()
# for thread in threads:
#     thread.join()


DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)



for player in player_urls[1000:]:

    individual_scrape(player)
        #if stats != 'fail':
            #pass
            #player_totals[player[0]] = stats



print("Elapsed Time: %s" % (time.time() - start))
#print(player_totals)
#print(len(player_totals))


# f = open('data.json', 'a')
# json.dump(player_totals, f)
# f.close()
