"""Author: Andrew Higgins
https://github.com/speckly

sucorn project setup, for first time users"""

import os
import getpass
import json

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(f"{DIRECTORY}/.env"):
    token = getpass.getpass("Input Discord token (hidden, enter to quit): ")
    if token.strip() != "":
        with open(".env", "w", encoding="utf-8") as env_f:
            env_f.write(f"TOKEN={token}")
        print("Written Discord Token to .env")

if not os.path.exists(f"{DIRECTORY}/images"):
    try:
        print('Creating images folder')
        os.makedirs(f"{DIRECTORY}/images")
    except FileExistsError:
        pass # Happens for symbolic links?

if not os.path.exists(f"{DIRECTORY}/utilities/reverse_api/.env"):
    while True:
        username = input("/utilities/reverse_api/.env\nInput Microsoft username for reverse API if needed (press enter to quit): ")
        if username.strip() == "":
            break
        password = getpass.getpass("Input your password (hidden): ")
        if password.strip() == "":
            break
        pair = f"{username}={password}"
        with open(f"{DIRECTORY}/utilities/reverse_api/.env", "a", encoding="utf-8") as env_f:
            env_f.write(pair)
        print(f"Written {pair}")

if not os.path.exists(f"{DIRECTORY}/utilities/reverse_api/prompt.txt"):
    prompt = input("/reverse_api/prompt.txt\nInput prompt, can be changed later: ")
    with open(f"{DIRECTORY}/reverse_api/prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

if not os.path.exists(f"{DIRECTORY}/reverse_api/usernames.json"):
    with open("./utilities/reverse_api/usernames.json", 'w', encoding="utf-8") as uFile:
        print("intialised usernames.json as it does not exist, please use this file for loading of accounts (in the normal key)")
        usernames = {"normal": [], "loaded": [], "unusable": [], "otp": []}
        json.dump(usernames, uFile, indent=4)

if input("Install requirements? (Y): ").lower().strip() in ["", "y"]:
    os.system("pip install -r requirements.txt")

print("Setup complete!")
