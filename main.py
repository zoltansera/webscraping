'''
Scraping advertisement website for new ads with selenium
'''
import sys
import time
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

    def run(self):
        '''
        Creating log file, and calling scrape as many times as needed
        '''
        with open("logs.txt", "w", encoding="utf-8") as logfile:
            print("Estimated run time: "+ str(self.frequency*self.repetitions) + " minutes.\n")
            logfile.write("Scraping started at "+str(time.localtime()) + "\n")

            for _ in range(self.repetitions):
                print("Scraping started at "+str(time.localtime()))
                logfile.write("Scraping started at "+str(time.localtime()) + "\n")
                self.scrape()
                time.sleep(60*self.frequency)

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
                EC.presence_of_element_located((By.CLASS_NAME, "main-box-footer")))
            listings = driver.find_elements(
                By.XPATH, '//*[contains(@class, "list-item")]')
            if not self.last_item_id:
                print("Found "+str(len(listings)) +
                      " items on latest results page.")
                for idx, item in enumerate(listings):
                    if idx == 0:
                        self.last_item_id = item.find_element(
                            By.XPATH, '//*[contains(@id, "listid")]').get_attribute("id")
                        print("Last item ID: " + self.last_item_id)
                    print(item.find_element(
                        By.CLASS_NAME, "item-title").
                            find_element(By.TAG_NAME, 'a').get_attribute('text')
                    )
            else:
                if listings[0].find_element(
                        By.XPATH, '//*[contains(@id, "listid")]').get_attribute("id") \
                        != self.last_item_id:
                    self.last_item_id = listings[0].find_element(
                        By.XPATH, '//*[contains(@id, "listid")]').get_attribute("id")
                    print("UJ HIRDETES")
                    print(listings[0].find_element(
                        By.CLASS_NAME, "item-title").
                        find_element(By.TAG_NAME, 'a').get_attribute('text')
                    )
                    php_url = "https://sorbusdigital.com/storage/sendnoti.php?mailto=" + \
                    self.recipient + "&keyword=" + self.keyword + "&site=" + \
                        self.site + "&url=" + \
                        listings[0].find_element(
                            By.CLASS_NAME, "item-title"). \
                            find_element(By.TAG_NAME, 'a').get_attribute('href')
                    driver.get(php_url)

        finally:
            driver.quit()


if __name__ == "__main__":
    myScraper = Scraper(sys.argv)
    myScraper.run()
    print("Scraping finished.\n")
