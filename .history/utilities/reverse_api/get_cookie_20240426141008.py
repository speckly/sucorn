from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

def sign_in(driver, username, password):
    driver.get("https://www.bing.com/images/create")
    create = driver.find_element(by=By.ID, value="create_btn_c")
    create.click()
    try:
        signin = driver.find_element(by=By.LINK_TEXT, value="Sign in with a personal account")
        signin.click()
    except:
        pass  # button is not required

    # Microsoft sign in
    text_box = driver.find_element(By.NAME, "loginfmt")
    text_box.send_keys(username)
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
            otp_box.send_keys(input(f"OTP ({username}) -> "))
            signin = driver.find_element(By.ID, "primaryButton")
            signin.click()

    if pass_mode:  # Input password if available
        text_box.send_keys(password)
        next_btn = driver.find_element(By.ID, "idSIButton9")
        next_btn.click()

    try:
        if driver.find_element(By.ID, "i0118Error"):
            return False
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
        phone.send_keys(password)

        send_code = driver.find_element(By.CSS_SELECTOR, 'a[id^="wlspispHipSendCode"]')
        send_code.click()

        input_code = driver.find_element(By.CSS_SELECTOR, 'input[id^="wlspispSolutionElement"]')
        input_code.send_keys(input(f"OTP (Phone) for {username} -> "))

        submit = driver.find_element(By.ID, "ProofAction")
        submit.click()

        finish = driver.find_element(By.ID, "FinishAction")
        finish.click()
