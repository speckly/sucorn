import os
import argparse
import requests
import browser_cookie3 as bc3
from dotenv import load_dotenv

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
def get_access_token(cookie_str: str) -> str:
    """thank you @theonehong on discord this really helped!!!!
    TODO: find the response if a cookie has expired or is invalid, apparently its 1 day?"""

    url = "https://aitestkitchen.withgoogle.com/api/auth/session"
    headers = {
        'cookie': cookie_str,
        'referer': 'https://aitestkitchen.withgoogle.com/tools,/image-fx?utm_source=gdm&utm_medium=site',
    }
    response = requests.request("GET", url, headers=headers).json()
    try:
        token = response['access_token']
    except KeyError:
        return "" # handle in parent function call
    return token

def cookie_string() -> str:
    """Author: Andrew Higgins
    Gets this cookie and returns it in a cookie string k=v;
    __Secure-next-auth.session-token"""

    for cookie_fn in [
        bc3.chrome,
        bc3.chromium,
        bc3.opera,
        bc3.opera_gx,
        bc3.brave,
        bc3.edge,
        bc3.vivaldi,
        bc3.firefox,
        bc3.librewolf,
        bc3.safari,
    ]:
        try:
            cookies: http.cookiejar.CookieJar = cookie_fn(domain_name='aitestkitchen.withgoogle.com')

            for cookie in cookies:
                c_name: str = cookie.name
                if c_name == '__Secure-next-auth.session-token':
                    return f"{c_name}={cookie.value};"
        except bc3.BrowserCookieError:
            continue
        except PermissionError as e:
            print(
                f"Permission denied while trying to load cookies from {cookie_fn.__name__}. {e}"
            )
        except Exception as e:
            print(
                f"Error happened while trying to load cookies from {cookie_fn.__name__}. {e}"
            )

    # target cookie is not found, log error in imagen3.py
    return ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get AI Test Kitchen cookies and stores them in .env')
    parser.add_argument('name', type=str, help="Output variable name in .env containing the cookie string")

    args = parser.parse_args()
    env_var: str = args.name
    cookie_string: str = cookie_string()
    if cookie_string == "":
        print("Could not find session cookie")
        quit()

    DOTENV_PATH = f'{DIRECTORY}/.env'
    if os.path.exists(DOTENV_PATH):
        load_dotenv(DOTENV_PATH)

        if os.getenv(env_var) is None:
            with open(DOTENV_PATH, 'a', encoding='utf-8') as f:
                f.write(f"{env_var}={cookie_string}\n")
            print(f"Added {env_var} to .env file.")
        else:
            print(f"{env_var} already exists in .env file. No changes will be made.")
    else:
        with open(DOTENV_PATH, 'w', encoding='utf-8') as f:
            f.write(f"{env_var}={cookie_string}\n")
        print(f"Created .env file and added {env_var}.")

    # access_token: str = get_access_token(cookie_string) # For demo purpose, not supposed to persist
    # print(access_token)
