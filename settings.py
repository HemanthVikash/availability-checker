import os
import validators

url = 'https://www.visible.com/shop/smartphones/apple'

def __modify_url():
    global url
    url = url.strip()


def __validate_url():
    global url
    __modify_url()
    if ("https" not in url):
        raise RuntimeWarning("The url entered is not safe. Driver may fail at runtime")
    return validators.url(url)




def main(): 
    global url
    flag = True
    while(flag):
        # url = input('Copy-paste the link for scraping: ')
        if(__validate_url()): 
            print("Accepted url")
            flag = False
        else: 
            print("Error with the url. Just copy-paste bruh..")
