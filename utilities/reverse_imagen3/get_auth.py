"""until i properly figure out oauth2 (i think its just the lack of proper scope stopping me)
i will be using this method"""

# from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

chrome_options = Options()
# chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0")

with open('clients/users.json') as j:
    users = json.load(j)
driver = Chrome(options=chrome_options)

for username, pwd in users['usable'].items():
    try:
        driver.get('https://aitestkitchen.withgoogle.com/tools/image-fx')
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in with Google']")))
        button.click()
        driver.implicitly_wait(5)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']")))
        button.click()

        username_field = driver.find_element(By.ID, 'identifierId')
        username_field.send_keys(username)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        button.click()
        
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys(pwd)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        button.click()

        generate = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()=\"I'm feeling lucky\"]/..")))
        generate.click()

        # Automate the clear cache process
        driver.get('chrome://settings/clearBrowserData')
        driver.implicitly_wait(5)
        driver.find_element_by_xpath("//settings-ui").send_keys(Keys.RETURN)

    except:
        print("observe error")
    input("remove this when deploying")

