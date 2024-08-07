"""Author: Andrew Higgins
https://github.com/speckly

sucorn project data preparation phase
This script is used to automate the login process into Microsoft Bing Image Creator.

BUG: Too many requests
 Traceback (most recent call last):
  File "get_cookie.py", line 154, in <module>
    cookie = get_cookie(session_driver, username, password)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "get_cookie.py", line 99, in get_cookie
    u_cookie = driver.get_cookie("_U")["value"]
               ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^"""

import os
import json
import copy
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

def get_cookie(driver: webdriver, username: str, password: str):
    """Author: Andrew Higgins
    https://github.com/speckly

    Gets the session cookie given a Microsoft username and password"""

    driver.get("https://www.bing.com/images/create")

    create = driver.find_element(by=By.ID, value="create_btn_c")
    create.click()
    try:
        signin = driver.find_element(by=By.LINK_TEXT, value="Sign in with a personal account")
        signin.click()
    except Exception:
        pass # button is not required

    # Microsoft sign in
    text_box = driver.find_element(By.NAME, "loginfmt")
    text_box.send_keys(username)
    next_btn = driver.find_element(By.ID, "idSIButton9")
    next_btn.click()
    try:
        text_box = driver.find_element(By.NAME, "passwd")
        pass_mode = True
    except Exception:
        try:
            password_switch = driver.find_element(By.ID, "idA_PWD_SwitchToPassword")
            password_switch.click()
            text_box = driver.find_element(By.ID, "i0118")
            pass_mode = True
        except Exception:
            pass_mode = False
            otp_box = driver.find_element(By.ID, "idTxtBx_OTC_Password")
            otp_box.send_keys(input(f"OTP ({username}) -> "))
            signin = driver.find_element(By.ID, "primaryButton")
            signin.click()

    if pass_mode: # Input password if available
        text_box.send_keys(password)
        next_btn = driver.find_element(By.ID, "idSIButton9")
        next_btn.click()

    try:
        if driver.find_element(By.ID, "i0118Error"):
            return -1
    except Exception:
        pass

    try:
        accept_btn = driver.find_element(By.ID, "acceptButton")
        accept_btn.click()
    except Exception:
        
        try:
            next_btn = driver.find_element(By.ID, "StartAction")
            next_btn.click()

            # Locked case
            select_element = driver.find_element(By.CSS_SELECTOR,
            'select[id^="wlspispHIPCountrySelect"]')
            select = Select(select_element)
            select.select_by_value("SG")

            phone = driver.find_element(By.CSS_SELECTOR, 'input[id^="wlspispHIPPhoneInput"]')
            phone.send_keys(password)

            send_code = driver.find_element(By.CSS_SELECTOR, 'a[id^="wlspispHipSendCode"]')
            send_code.click()

            input_code = driver.find_element(By.CSS_SELECTOR, 'input[id^="wlspispSolutionElement"]')
            input_code.send_keys(input(f"OTP (Phone) for {username} -> "))

            submit = driver.find_element(By.ID, "ProofAction")
            submit.click()

            finish = driver.find_element(By.ID, "FinishAction")
            finish.click()

            accept_btn = driver.find_element(By.ID, "acceptButton")
            accept_btn.click()
        except Exception:
            input("Manual for now until i implement automation here, get to the end and enter") # Lets protect your account
        

    u_cookie = driver.get_cookie("_U")["value"]

    # Finish up # BUG: unstable
    driver.get("https://www.bing.com/images/create")
    profile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "id_l")))
    time.sleep(0.5)
    profile.click()
    signout = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "id_signout")))
    time.sleep(0.5)
    signout.click()
    return u_cookie


if __name__ == "__main__":

    JSON_FILE = 'cookies.json'
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    print("Author: Andrew Higgins")
    print("https://github.com/speckly")
    print("Creating webdriver")

    session_driver = webdriver.Chrome(options=chrome_options)
    session_driver.implicitly_wait(5)

    load_dotenv()
    GENERAL_PASS = os.getenv("GENERAL")
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    usernames = []
    if os.path.exists(f"{DIRECTORY}/usernames.json"):
        try: 
            with open(f"{DIRECTORY}/usernames.json", encoding="utf-8") as ufile:
                usernames = json.load(ufile)
        except json.JSONDecodeError:
            print("usernames.json decode error")
            quit()
    else:
        with open(f"{DIRECTORY}/usernames.json", 'w',
        encoding="utf-8") as uFile: # NOTE: Done for each username in case the webdriver crashes
            print("intialised usernames.json as it does not exist, load accounts in the normal key")
            usernames = {"normal": [], "loaded": [], "unusable": [], "otp": []}
            json.dump(usernames, uFile, indent=4)

    print("Starting")
    JSON_FILE = f'{DIRECTORY}/cookies.json'
    for username in copy.deepcopy(usernames["normal"]): # Require modification of this list
        if GENERAL_PASS:
            password = GENERAL_PASS # TODO: override this
        else:
            password = os.getenv(username.split("@")[0]) # Not case sensitive
            if not password:
                print(f"Missing password for {username}, check /utilities/reverse_api/.env")
                continue
        cookie = get_cookie(session_driver, username, password)
        if cookie == -1:
            print(f"Incorrect password for user {username}. Check /utilities/reverse_api/.env")
            continue

        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE, 'r', encoding="utf-8") as file:
                    data = json.load(file)
                data[username] = cookie
                with open(JSON_FILE, 'w', encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in '{JSON_FILE}': {e}")
        else:
            with open(JSON_FILE, 'w', encoding="utf-8") as file:
                json.dump({username: cookie}, file, indent=4)

        usernames["loaded"].append(usernames["normal"].pop(usernames["normal"].index(username)))
        # NOTE: Done for each username in case the webdriver crashes
        with open(f"{DIRECTORY}/usernames.json", 'w', encoding="utf-8") as uFile:
            json.dump(usernames, uFile, indent=4)

        print(f'Cookie acquired for {username}')

    session_driver.quit()
    print("Mission accomplished")
