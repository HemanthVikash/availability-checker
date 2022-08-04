from selenium.common.exceptions import NoSuchElementException      
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def wait_until_class(webdriver, classname): 
    try:
        wait = WebDriverWait(webdriver, 10)
        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, classname)))
        return element
    except:
        return None

def check_exists_by_xpath(webdriver, xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_class(webdriver, classname):
    try:
        webdriver.find_element_by_class_name(classname)
    except NoSuchElementException:
        return False
    return True