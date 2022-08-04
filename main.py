from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import settings
import common_methods as cm
import time

import json 
import sys 
import random 
import requests
import timeit

useless_phones = {
    'https://www.visible.com/shop/smartphones/iphone-se': "Apple iPhone SE",
    'https://www.visible.com/shop/smartphones/iphone-11': "Apple iPhone 11",
    'https://www.visible.com/shop/smartphones/iphone-xs-pre-owned': "Apple iPhone XS Pre-Owned",
    'https://www.visible.com/shop/smartphones/iphone-xr-pre-owned': "Apple iPhone XR",
    "https://www.visible.com/shop/smartphones/iphone-x-pre-owned": "Apple iPhone X",
    'https://www.visible.com/shop/smartphones/iphone-8-pre-owned': "Apple iPhone 8"

}

class Scraper:
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='./chromedriver')
        
    def test_driver(self):
        self.driver.get('https://www.google.com/')
        xpath = '/html/body/div[1]/div[2]/div/img'
        if (cm.check_exists_by_xpath(self.driver, xpath)):
            print("Driver works")
        else:
            print("Ripperoni")
            



    def light_pass(self):
        print(f"Getting {settings.url} ...")
        self.driver.get(settings.url)

        try:
            phones_container = self.driver.find_element_by_class_name('TileWrapper-sc-1xbwotf-1')
        except Exception as e:
            print(e)
            return None
        if (phones_container is not None):
            phones = phones_container.find_elements_by_class_name('Tile-sc-1xbwotf-2')

            for phone in phones:
                top_banner = phone.find_element_by_class_name('TileTopBannerSection-sc-1xbwotf-37')
                in_stock = True
                if (cm.check_exists_by_class(top_banner, 'OutOfStock-sc-1xbwotf-41')):
                    in_stock = False
                    phone_detail = phone.find_element_by_class_name('TileMiddleSection-sc-1xbwotf-38')
                    phone_name = phone_detail.find_element_by_tag_name('span').text
                    
                else: 
                    in_stock = True
                    phone_detail = phone.find_element_by_class_name('TileMiddleSection-sc-1xbwotf-38')
                    link = phone_detail.find_element_by_tag_name('a').get_attribute('href')
                    phone_name = phone_detail.find_element_by_tag_name('span').text
                    if (link not in useless_phones):
                        print(phone_name, "is available. Head over to: ", link, "NOW!")
                        slack_notify(link, phone_name)
                    


            

    

    def __del__(self):
        self.driver.quit()
    

def slack_notify(phone_link, phone_name): 
    url = "https://hooks.slack.com/services/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"
    message = (f"A {phone_name} has been spotted! Go to {phone_link} to get it!")
    title = (f"Company Phone Available!")
    slack_data = {
        "username": "NotificationBot",
        "icon_emoji": ":iphone:",
        #"channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


def main(): 
    scraper = Scraper()
    print('Starting cycle')
    start = time.time()
    while(1):
        try: 
            scraper.light_pass()
        except WebDriverException as e:
            print(e)
             
        end = time.time()
        print('Time elapsed: ', end - start, "seconds")
        
        lag = 30
        print(f"Sleeping for {lag} seconds")
        time.sleep(lag)

if __name__ == "__main__":
    settings.main()
    main()