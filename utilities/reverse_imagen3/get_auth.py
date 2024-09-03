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
    response = requests.request("GET", url, headers=headers)
    token = response.json()['access_token']
    return token

def cookie_string() -> str:
    """Author: Andrew Higgins
    Gets these cookies and returns them in a cookie string k=v;k=v;
    __Host-next-auth.csrf-token
    __Secure-next-auth.session-token"""

    cj: http.cookiejar.CookieJar = bc3.firefox(domain_name='aitestkitchen.withgoogle.com')
    out: str = ""
    for cookie in cj:
        c_name: str = cookie.name
        if c_name in ['__Host-next-auth.csrf-token', '__Secure-next-auth.session-token']:
            out += f"{c_name}={cookie.value};"
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get AI Test Kitchen cookies and stores them in .env')
    parser.add_argument('name', type=str, help="Output variable name in .env containing the cookie string")

    args = parser.parse_args()
    env_var: str = args.name
    cookie_string: str = cookie_string()

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
