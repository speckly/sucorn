"""Author: Andrew Higgins
https://github.com/speckly

sucorn project data preparation phase
This file contains the workflow used per child process to automate the image creation process"""

import os
import sys
import time
import ctypes
import subprocess
import json

os.chdir(os.path.dirname(os.path.realpath(__file__)))
def run_command(account: str, token: str, prompt: str, out_path: str, delay: str, max_attempts: str):
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    This is the function to be executed per child process to automate the image creation process"""
    ctypes.windll.kernel32.SetConsoleTitleW(f"reverse_api - {account}")
    cmd = f"python BingImageCreator.py -U {token} --prompt \"{prompt}\" --output-dir {out_path}"
    count = combo = 0
    max_attempts = int(max_attempts)
    delay = float(delay)
   
    while combo < max_attempts:
        time.sleep(delay)
        s = time.time()
        count += 1
        print(f"\n{account} Cycle {count}, Strike {combo}: ", end="")
        try:
            subprocess.run(cmd, shell=True, check=True, stderr=subprocess.PIPE)
            combo = 0
        except subprocess.CalledProcessError as e:
            exc = e.stderr.decode().split("\n")[-2]
            print(f"Failed: {exc}")
            if "Exception: Redirect failed" in exc:
                combo += 1
            else:
                combo = 0

        print(f"{time.time() - s}s")

    if os.path.exists('cookies.json'):
        with open('cookies.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        if account in data:
            del data[account]
            print(f"Account {account} removed successfully.")
        else:
            print(f"Account {account} not found")
            sys.exit(1)
        with open('cookies.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    else:
        print("cookies.json not found, unable to remove cookie associated with this account, run get_cookie to restore this file")

    if os.path.exists('usernames.json'):
        with open('usernames.json', 'r', encoding="utf-8") as file:
            usernames = json.load(file)
        if account in usernames["loaded"] and account not in usernames["unusable"]:
            usernames["unusable"].append(usernames["loaded"].pop(usernames["loaded"].index(account)))
            print(f"Account {account} moved to unusable")
        else:
            print(f"Account {account}, not modified in usernames.json, please check")
        with open('usernames.json', 'w', encoding="utf-8") as file:
            json.dump(usernames, file, indent=4)
    else:
        print("usernames.json not found, unable to move account to unusable category, run get_cookie to restore this file")

    input(f"Terminated at {time.asctime()} due to {max_attempts} consecutive redirects. Press any key to quit ")
    sys.exit(0)

if __name__ == '__main__':
    # Unpack all of the args, no argparser required as it is validated on run.py
    run_command(*sys.argv[1:])
