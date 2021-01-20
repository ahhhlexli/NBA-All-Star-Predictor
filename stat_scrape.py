import requests
import bs4 as soup 

url = 'https://www.basketball-reference.com/players/'

#h/harriel01.html

with open('players_after_1996_noA.txt') as f:
    players = f.read().splitlines()
    

counter = 0
fail_list = []
for player in players[100:120]:
    
    player = player.lower()
    name = player.split(' ')
    end_str = name[1][0] + '/' +  name[1][:5] + name[0][:2] + '01.html'

    url = 'https://www.basketball-reference.com/players/' + end_str

    print(url)
    

    # try:
    #     requests.get(url)
    #     counter += 1
    #     print(counter, player)
    # except:
    #     fail_list.append(player)

print(fail_list)