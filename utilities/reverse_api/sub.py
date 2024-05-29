"""Author: Andrew Higgins
https://github.com/speckly

sucorn project data preparation phase
This file contains the workflow used per child process to automate the image creation process"""

import os
import sys
import time
import subprocess
import json
import asyncio
import keyboard
if sys.platform == 'win32':
    import ctypes
    from run import read_prompt
    import pygetwindow as gw # linux users will not want to import this
else:
    from run_linux import read_prompt

def on_hotkey(ptr: list) -> None:
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    Callback function to update prompt using modifying by reference"""
    s = time.time()
    prompt = read_prompt()
    print(f"\nPrompt reloaded in {time.time()-s:.4f}s, {prompt}")
    ptr[0] = prompt

async def main(account: str, token: str, prompt: str, out_path: str, delay: str, max_attempts: str) -> None:
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    This is the function to be executed per child process to automate the image creation process
    Command line arguments are parsed as a string so this function converts it"""
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{account} sucorn API")
    else:
        sys.stdout.write(f"\x1b]2;sucorn API {account}\x07")
    count = combo = 0
    max_attempts = int(max_attempts)
    delay = float(delay)
    prompt_pointer = [prompt] # I LOVE POINTERS I LOVE MODIFYING BY REFERENCE
    keyboard.add_hotkey('ctrl+shift+r', on_hotkey, args=(prompt_pointer,))

    while combo < max_attempts:
        await asyncio.sleep(delay)

        s = time.time()
        count += 1
        print(f"\n{account} Cycle {count}, Strike {combo}: ", end="")
        # Put here because of reloading
        cmd = f"python BingImageCreator.py -U {token} --prompt \"{prompt_pointer[0]}\" --output-dir {out_path}" 
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

        print(f"{time.time()-s:.4f}s")

    if os.path.exists('cookies.json'):
        with open('cookies.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        if account in data:
            del data[account]
            print(f"Account {account} removed successfully.")
        else:
            print(f"Account {account} not found")
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
    if sys.platform.startswith('linux'):
        subprocess.run(['exit'], check=True) # TODO: Confirm this
    elif sys.platform == 'darwin':
        subprocess.run(['osascript', '-e', 'tell application "Terminal" to close first window'], check=True) # TODO: Confirm this
    elif sys.platform == 'win32':
        ctypes.windll.user32.PostMessageW(gw.getActiveWindow()._hWnd, 0x0010, 0, 0)

if __name__ == '__main__':
    # Unpack all of the args, no argparser required as it is validated on run.py
    asyncio.run(main(*sys.argv[1:]))
