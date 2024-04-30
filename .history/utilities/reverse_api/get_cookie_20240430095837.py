"""Author: Andrew Higgins
https://github.com/speckly

sucorn project data preparation phase
This script is used to automate the login process into Microsoft Bing Image Creator."""

import os
import json
import copy

from selenium import webdriver  # Add missing import statement
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

    # Rest of the code...
