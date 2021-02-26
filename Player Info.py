from selenium import webdriver 
import time
import string
from Individual_Player_Scrape import individual_scrape
start = time.time()


DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

link_list = []

for letter in list(string.ascii_lowercase):

    url = 'https://www.basketball-reference.com/players/' + letter
    driver.get(url)

    try:
        table = driver.find_elements_by_xpath('//*[@id="players"]/tbody/tr')

        for row in range(len(table)):
            
            try:
                start_year = int(table[row].find_element_by_xpath('./td[1]').text)
                name = table[row].find_element_by_xpath('./th').text
                link = table[row].find_element_by_xpath('./th//a')

                if start_year >= 1996:

                    player_info = [name, str(link.get_attribute('href'))]
                    link_list.append(player_info)           
            except:
                pass

    except:
        pass


for player in link_list:
    
    individual_scrape(player, driver)

print("Elapsed Time: %s" % (time.time() - start))



