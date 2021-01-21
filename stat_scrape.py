import requests
import bs4 as soup 
import threading
import time

start = time.time()
url = 'https://www.basketball-reference.com/players/'

with open('players_after_1996_noA.txt') as f:
    players = f.read().splitlines()
    
with open('special.txt') as f:
    parsed = [i.split('|') for i in f.read().splitlines()]
    special = [i[0].strip() for i in parsed]
    end = {i[0].strip() : i[1].strip() for i in parsed}

fail_list = []
url_list = []

for player in players:
 
    player = player.lower()
    name = player.replace('.', '').replace('\'', '').replace('-', '').split(' ')

    if player in special:
        end_str = end[player]
    else:
        end_str = name[1][0] + '/' +  name[1][:5] + name[0][:2] + '01.html'

    url = 'https://www.basketball-reference.com/players/' + end_str
    url_list.append((player,url))

urls = url_list #this being the list of url generated

def fetch_url(url):
    try:
        r = requests.get(url[1])
        #print(url[1] + "\tStatus: " + str(r.status_code))
        print("'%s\' fetched in %ss" % (url[1], (time.time() - start)))

        if r.status_code != 200:
            fail_list.append(url)

    except Exception as e:
        print(url + "\tNA FAILED TO CONNECT\t" + str(e))
        
threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for thread in threads:
    time.sleep(0.05)
    thread.start()
for thread in threads:
    thread.join()

print("Elapsed Time: %s" % (time.time() - start))
print(fail_list)
print(len(fail_list))

with open('fail_list.txt', 'w') as f:
    for i in fail_list:
    
        f.writelines(i[0] + '\n')