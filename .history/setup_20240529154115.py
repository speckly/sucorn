"""Author: Andrew Higgins
https://github.com/speckly

sucorn project setup, for first time users"""

import os
import getpass
import json
import venv
import subprocess

def _venv_req():
    pip = f"{DIRECTORY}/venv/{'bin' if os.name != 'nt' else 'Scripts'}/pip"
    subprocess.check_call([pip, "install", "-r", "requirements.txt"], cwd=DIRECTORY)

DIRECTORY: str = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(f"{DIRECTORY}/.env"):
    token: str = getpass.getpass("\n/.env\nInput Discord token (enter to skip): ")
    if token.strip() != "":
        with open(".env", "w", encoding="utf-8") as env_f:
            env_f.write(f"TOKEN={token}")
        print("Written Discord Token to .env")

if not os.path.exists(f"{DIRECTORY}/images"):
    try:
        print('Creating images folder')
        os.makedirs(f"{DIRECTORY}/images")
    except FileExistsError:
        pass  # Happens for symbolic links?

if not os.path.exists(f"{DIRECTORY}/utilities/reverse_api/.env"):
    with open(f"{DIRECTORY}/utilities/reverse_api/.env", 'w', encoding="utf-8") as env_f:
        general: str = getpass.getpass('Input general password, if all accounts share the same password (enter to skip): ')
        env_f.write(f"GENERAL={general or ''}")
    while True:
        username = input("\n/utilities/reverse_api/.env\nInput Microsoft username (enter to skip): ")
        if username.strip() == "":
            break
        password = getpass.getpass(f"Password for {username} (enter to skip): ")
        if password.strip() == "":
            break
        pair: str = f"{username}={password}"
        with open(f"{DIRECTORY}/utilities/reverse_api/.env", "a", encoding="utf-8") as env_f:
            env_f.write(pair)
        print(f"Written {pair}")

if not os.path.exists(f"{DIRECTORY}/utilities/reverse_api/prompt.txt"):
    prompt: str = input("\n/reverse_api/prompt.txt\nInput prompt, can be changed later: ")
    with open(f"{DIRECTORY}/utilities/reverse_api/prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

if not os.path.exists(f"{DIRECTORY}/utilities/reverse_api/usernames.json"):
    with open("./utilities/reverse_api/usernames.json", 'w', encoding="utf-8") as uFile:
        usernames: dict = {"normal": [], "loaded": [], "unusable": [], "otp": []}
        json.dump(usernames, uFile, indent=4)
        print("initialised /utilities/reverse_api/usernames.json, use this file for loading of accounts in the normal key")

if input("Create venv? (Y): ").lower().strip() in ["", "y"]:
    venv.create(f"{DIRECTORY}/venv", with_pip=True)
    print("Creation complete")
if input("Install requirements in venv? (Y): ").lower().strip() in ["", "y"]:
    _venv_req()
elif input("Install requirements without venv? (Y): ").lower().strip() in ["", "y"]:
    os.system("pip install -r requirements.txt")

print("Setup complete!")
