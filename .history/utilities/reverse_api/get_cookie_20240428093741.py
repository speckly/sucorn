from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
import os

driver = webdriver.Chrome()

def get_cookie(driver, username, password):
    driver.get("https://example.com/login")
    username_input = driver.find_element_by_id("username")
    password_input = driver.find_element_by_id("password")
    submit_button = driver.find_element_by_css_selector("button[type='submit']")

    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button.click()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav")))
    except:
        return -1

    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'sessionid':
            return cookie['value']

    return -1

if __name__ == '__main__':
    with open("usernames.json", 'r') as ufile:
        usernames = json.load(ufile)
    for username in usernames['normal']:
        if os.getenv(username.split("@")[0]):
            password = os.getenv(username.split("@")[0])
        else:
            password = input(f"Enter password for {username}: ")
        try:
            cookie = get_cookie(driver, username, password)
        except Exception as e:
            print(f"Unknown exception: {e}")
            continue
        if cookie!= -1:
            with open("cookies.json", 'w') as cfile:
                json.dump({username: cookie}, cfile, indent=4)
            print(f'Cookie acquired for {username}')