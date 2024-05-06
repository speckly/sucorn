"""Author: Andrew Higgins
https://github.com/speckly

sucorn project data preparation phase
This script is used to automate the login process into Microsoft Bing Image Creator."""

import os
import json
import copy

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

    def get_cookie(driver: webdriver, username: str, password: str):
        """Author: Andrew Higgins
        https://github.com/speckly

        Gets the session cookie given a Microsoft username and password"""

        # Go to the login page
        driver.get("https://login.microsoftonline.com")

        # Enter the username and password
        driver.find_element(By.ID, "i0116").send_keys(username)
        driver.find_element(By.ID, "i0118").send_keys(password)

        # Click the sign in button
        driver.find_element(By.ID, "idSIButton9").click()

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id__3")))

        # Get the session cookie
        cookie = driver.get_cookie("MSPAuth")
        return cookie

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
        # Locked case
        next_btn = driver.find_element(By.ID, "StartAction")
        next_btn.click()

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

    u_cookie = driver.get_cookie("_U")["value"]

    # Finish up
    driver.get("https://www.bing.com/images/create")
    profile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "id_l")))
    profile.click()
    signout = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "id_signout")))
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
        with open(f"{DIRECTORY}/usernames.json", encoding="utf-8") as ufile:
            usernames = json.load(ufile)
    else:
        with open(f"{DIRECTORY}/usernames.json", 'w',
        encoding="utf-8") as uFile: # NOTE: Done for each username in case the webdriver crashes
            print("intialised usernames.json as it does not exist, please use this file for loading of accounts (in the normal key)")
            usernames = {"normal": [], "loaded": [], "unusable": [], "otp": []}
            json.dump(usernames, uFile, indent=4)

    JSON_FILE = f'{DIRECTORY}/cookies.json'
    for username in copy.deepcopy(usernames["normal"]): # Require modification of this list
        if GENERAL_PASS:
            password = GENERAL_PASS
        else:
            password = os.getenv(username.split("@")[0]) or input(f"Enter password for {username}: ")
            if not password:
                print(f"Missing password for {username}")
                continue
        # ...
        try:
            cookie = get_cookie(session_driver, username, password)
            if cookie == -1:
                print(f"Incorrect password for user {username}. Check /utilities/reverse_api/.env")
                continue
        except Exception as e:
            print(f"Unknown exception: {e}")
            quit()

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
