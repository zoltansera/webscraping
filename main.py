'''
Continuously scraping advertisement website for new ads with selenium
'''


import os
import sys
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper():
    '''
    Scraper class
    '''
    def __init__(self, args):
        self.site = args[1]
        self.keyword = args[2]
        self.recipient = args[3]
        self.frequency = int(args[4])
        self.repetitions = int(args[5])
        self.last_item_id = None
        self.stored_data = { 'title': [], 'url': []}


    def run(self):
        '''
        Calling scrape as many times as needed, then calling export results
        '''
        print("Listening for new advertisements started.")
        print("Estimated run time: "+ str(self.frequency*self.repetitions) + " minutes.")
        # initial scrape, repetition count will start after this one
        self.scrape()
        for _ in range(self.repetitions):
            print("Next check starts in " + str(self.frequency) + " minute(s).")
            time.sleep(60*self.frequency)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Scraping started at " + current_time)
            self.scrape()

        self.export()


    def export(self):
        '''
        Export new findings to csv
        '''
        if len(self.stored_data['title']) > 0:
            data = pd.DataFrame({'title':self.stored_data['title'], 'url':self.stored_data['url']})
            data.to_csv('results.csv', index=False)
        else:
            print("No new advertisements appeared during run time.")


    def get_title_attr(self, item, attr):
        '''
        Returns attribute extracted from <a> element
        found in parent with class item-title
        '''
        return item.find_element(By.CLASS_NAME, "item-title"). \
            find_element(By.TAG_NAME, 'a').get_attribute(attr)


    def scrape(self):
        '''
        Method that does the scraping.
        '''
        driver = webdriver.Firefox()
        driver.get(self.site)
        searchbar = driver.find_element(By.NAME, "q")
        searchbar.send_keys(self.keyword)
        searchbar.send_keys(Keys.RETURN)
        try:
            _element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "main-box-footer"))
            )

            listings = driver.find_elements(
                By.XPATH, '//*[contains(@class, "list-item")]'
            )

            latest_list_id = listings[0].find_element(
                By.XPATH, '//*[contains(@id, "listid")]'
            ).get_attribute("id")

            if not self.last_item_id:
                print(
                    "Found " + str(len(listings)) + " items on latest results page.",
                    "Latest item ID: " + latest_list_id,
                    sep=os.linesep
                )
                self.last_item_id = latest_list_id
                for item in listings:
                    print(self.get_title_attr(item, 'text'))

            else:
                if  latest_list_id != self.last_item_id:
                    self.last_item_id = latest_list_id
                    print("New advertisement found!")
                    self.stored_data['title'].append(self.get_title_attr(listings[0], 'text'))
                    self.stored_data['url'].append(self.get_title_attr(listings[0], 'href'))
                    print(self.get_title_attr(listings[0], 'text'))

                    php_url = "https://sorbusdigital.com/storage/sendnoti.php?mailto=" + \
                        self.recipient + "&keyword=" + self.keyword + "&site=" + \
                        self.site + "&url=" + self.get_title_attr(listings[0], 'href')

                    driver.get(php_url)
                else:
                    print("No new ad appeared during this cycle.\n")

        finally:
            driver.quit()


if __name__ == "__main__":
    myScraper = Scraper(sys.argv)
    myScraper.run()
    print("Scraping finished.\n")
