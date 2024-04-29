from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import json
import copy

def get_cookie(driver: webdriver, USERNAME: str, PASSWORD: str):
    driver.get("https://www.bing.com/images/create")
    
    create = driver.find_element(by=By.ID, value="create_btn_c")
    create.click()
    try:
        signin = driver.find_element(by=By.LINK_TEXT, value="Sign in with a personal account")
        signin.click()
    except:
        pass # button is not required

    # Microsoft sign in
    text_box = driver.find_element(By.NAME, "loginfmt")
    text_box.send_keys(USERNAME)
    next_btn = driver.find_element(By.ID, "idSIButton9")
    next_btn.click()
    try:
        text_box = driver.find_element(By.NAME, "passwd")
        pass_mode = True
    except:
        try:
            password_switch = driver.find_element(By.ID, "idA_PWD_SwitchToPassword")
            password_switch.click()
            pass_mode = True
        except:
            pass_mode = False
            otp_box = driver.find_element(By.ID, "idTxtBx_OTC_Password")
            otp_box.send_keys(input(f"OTP ({USERNAME}) -> "))
            signin = driver.find_element(By.ID, "primaryButton")
            signin.click()

    if pass_mode: # Input password if available
        text_box.send_keys(PASSWORD)
        next_btn = driver.find_element(By.ID, "idSIButton9")
        next_btn.click()
    
    try:
        if driver.find_element(By.ID, "i0118Error"):
            return -1
    except:
        pass

    try:
        accept_btn = driver.find_element(By.ID, "acceptButton")
        accept_btn.click()
    except:
        # Locked case
        next_btn = driver.find_element(By.ID, "StartAction")
        next_btn.click()

        select_element = driver.find_element(By.CSS_SELECTOR, 'select[id^="wlspispHIPCountrySelect"]')
        select = Select(select_element)
        select.select_by_value("SG")

        phone = driver.find_element(By.CSS_SELECTOR, 'input[id^="wlspispHIPPhoneInput"]')
        phone.send_keys(PASSWORD)

        send_code = driver.find_element(By.CSS_SELECTOR, 'a[id^="wlspispHipSendCode"]')
        send_code.click()
        
        input_code = driver.find_element(By.CSS_SELECTOR, 'input[id^="wlspispSolutionElement"]')
        input_code.send_keys(input(f"OTP (Phone) for {USERNAME} -> "))

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
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)

    load_dotenv()
    GENERAL_PASS = os.getenv("GENERAL")
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    usernames = []
    if os.path.exists(f"{DIRECTORY}/usernames.json"):
        with open(f"{DIRECTORY}/usernames.json") as ufile:
            usernames = json.load(ufile)
    else:
        with open(f"{DIRECTORY}/usernames.json", 'w') as uFile: # NOTE: Done for each username in case the webdriver crashes
            print("intialised usernames.json as it does not exist, please use this file for loading of accounts (in the normal key)")
            usernames = {"normal": [], "loaded": [], "unusable": [], "otp": []}
            json.dump(usernames, uFile, indent=4)

    JSON_FILE = f'{DIRECTORY}/cookies.json'
    for username in copy.deepcopy(usernames["normal"]): # Require modification of this list
        if GENERAL_PASS:
            password = GENERAL_PASS
        else:
            password = os.getenv(username.split("@")[0]) # Not case sensitive
            if not password:
                print(f"Missing password for {username}, skipping, check /utilities/reverse_api/.env")
                continue
        try:
            cookie = get_cookie(driver, username, password)
            if cookie == -1:
                print(f"Incorrect password for user {username}. Check /utilities/reverse_api/.env")
                continue
        except Exception as e:
            print(f"Unknown exception: {e}")
            quit()
        
        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE, 'r') as file:
                    data = json.load(file)
                data[username] = cookie
                with open(JSON_FILE, 'w') as file:
                    json.dump(data, file, indent=4)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in '{JSON_FILE}': {e}")
        else:
            with open(JSON_FILE, 'w') as file:
                json.dump({username: cookie}, file, indent=4)
        
        usernames["loaded"].append(usernames["normal"].pop(usernames["normal"].index(username)))
        with open(f"{DIRECTORY}/usernames.json", 'w') as uFile: # NOTE: Done for each username in case the webdriver crashes
            json.dump(usernames, uFile, indent=4)

        print(f'Cookie acquired for {username}')

    driver.quit()
    print("Mission accomplished")