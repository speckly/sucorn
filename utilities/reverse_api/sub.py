import os
import sys
import time
import ctypes
import subprocess
import json

def run_command(account, token, prompt, out_path):
    cmd = f"py BingImageCreator.py -U {token} --prompt \"{prompt}\" --output-dir {out_path}"
    count = combo = 0
    MAX = 20
    DELAY = 8

    while combo < MAX:
        time.sleep(DELAY)
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

    with open('cookies.json', 'r') as file:
        data = json.load(file)
    if account in data:
        del data[account]
        print(f"Account {account} removed successfully.")
    else:
        print(f"Account {account} not found")
    with open('cookies.json', 'w') as file:
        json.dump(data, file, indent=4)  

    with open('usernames.json', 'r') as file:
        usernames = json.load(file)
    if account in usernames["cookie"] and account not in usernames["unusable"]:
        usernames["unusable"].append(usernames["cookie"].pop(usernames["cookie"].index(account)))
        print(f"Account {account} moved to unusable")
    else:
        print(f"Account {account}, not modified in usernames.json, please check")
    with open('usernames.json', 'w') as file:
        json.dump(usernames, file, indent=4)  

    input(f"Terminated at {time.asctime()} due to {MAX} consecutive redirects. Press any key to quit ")
    os.system('exit')

if __name__ == '__main__':
    account, token, prompt, out_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    ctypes.windll.kernel32.SetConsoleTitleW(f"reverse_api - {account}")
    run_command(account, token, prompt, out_path)

