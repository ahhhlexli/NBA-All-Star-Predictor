
import requests
from bs4 import BeautifulSoup as soup 
import string

alphabets = list(string.ascii_lowercase)
alphabets.remove('x')

def player_grabber(letter):

    from bs4 import BeautifulSoup as soup 

    url = 'https://www.basketball-reference.com/players/' + letter
    page = requests.get(url)
    soup = soup(page.content, 'html.parser')
    list_find = soup.find_all('tr')
    player_list = [[text for text in i.stripped_strings if text != '*'] for i in list_find]

    return player_list

player_list = []

for i in alphabets:
    player_list = player_list + player_grabber(i)

pl = player_list.copy()

for player in player_list:
    if player[1] == 'From':
        pl.remove(player)
    elif int(player[1]) < 1996:
        pl.remove(player)

with open('players_after_1996.txt', 'a', encoding='utf-8') as f:
    for player in pl:
        
        f.writelines(player[0] + '\n')