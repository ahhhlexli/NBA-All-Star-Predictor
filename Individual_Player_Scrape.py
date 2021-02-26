

def individual_scrape(player, driver):

    from selenium import webdriver 
    import csv

    name = player[0]
    url = player[1]

    # DRIVER_PATH = './chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    #url = 'https://www.basketball-reference.com/players/h/headlu01.html'
    driver.get(url)

    try:
        table = driver.find_element_by_xpath('//*[@id="totals"]/tbody')
        season_totals = [[name] + row.text.split(' ') for row in table.find_elements_by_xpath('./tr')]

        with open('players.csv', 'a', newline='') as file:
            write = csv.writer(file)
            write.writerows(season_totals)

        #season_totals = [row.text.split(' ') for row in table.find_elements_by_xpath('./tr')]
        #driver.close()

        #player_totals[name] = season_totals
        print(name, (time.time() - start))
        return file
    except:
        return 'fail'