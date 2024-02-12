# NOTE: Currently impossible to differentiate from another session

from requests import get
import os
import sys
try: 
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    if input(f"BeautifulSoup4 is required to run this program ({sys.argv[0]}), execute pip install bs4? (Y): ").lower().strip() in ["", "y"]:
        os.system(f"pip install bs4")
    exit()
try:
    from selenium import webdriver # Blocked prompt uses JS
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ModuleNotFoundError:
    if input(f"selenium is required to run this program ({sys.argv[0]}), execute pip install selenium? (Y): ").lower().strip() in ["", "y"]:
        os.system(f"pip install selenium")
    exit()

def differentiate(URL):
    """
    Assumes generated URLS have been filtered out
    This functions differentiates between blocked/generating
    """
    browser = webdriver.Chrome()
    browser.get(URL)
    try:
        WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.blocked_bd')))
    except:
        pass
    html = browser.page_source

    soup = BeautifulSoup(html, 'html5lib')
    elements = soup.find_all('img', class_='blocked_bd') #get elements
    print(elements)
    if not elements: # Not blocked
        return False
    else:
        return True # Blocked

if __name__ == "__main__":
    BLOCKED_URL = "https://www.bing.com/images/create?q=colored+drawing+of+an+anime+girl+with+cat+ears+and+tail+bouncing+on+a+space+hopper+ball+with+a+handle%2C+space+hopper+is+has+an+cat+face+print%2C+age+appropriate%2C+ball+in+the+air%2C+cat+ears+are+the+same+color+as+girl%27s+hair%2C+space+hopper+handle+is+the+same+color+as+the+ball%2C+girl+not+wearing+shoes%2C+girl%27s+legs+in+front+of+her&rt=3&FORM=GENCRE&id=1-657a5be6d9914ffe9516e914a8c6646a"
    GENERATING_URL = "https://www.bing.com/images/create?q=colored+drawing+of+an+anime+girl+with+cat+ears+and+tail+bouncing+on+a+space+hopper+ball+with+a+handle%2C+space+hopper+is+has+an+cat+face+print%2C+age+appropriate%2C+ball+in+the+air%2C+cat+ears+are+the+same+color+as+girl%27s+hair%2C+space+hopper+handle+is+the+same+color+as+the+ball%2C+girl+not+wearing+shoes%2C+girl%27s+legs+in+front+of+her&rt=3&FORM=GENCRE&id=1-657a5f97b74c4c60bfb0fbf6ccbaec3d"
    GENERATED_URL = "https://www.bing.com/images/create/colored-drawing-of-an-anime-girl-with-cat-ears-and/1-657a5bd3c49741b4a7148b568dd4485e?FORM=GENCRE"
    print(differentiate(BLOCKED_URL))