import os
import sys
import time
import ctypes
import subprocess

def run_command(account, token, prompt, out_path):
    cmd = f"py BingImageCreator.py -U {token} --prompt \"{prompt}\" --output-dir {out_path}"
    count = 0

    while True:
        s = time.time()
        count += 1
        print(f"{account} {count}: ", end="")
        
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        
        print(f"{time.time() - s}s")

if __name__ == '__main__':
    account, token, prompt, out_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    ctypes.windll.kernel32.SetConsoleTitleW(f"reverse_api - {account}")
    run_command(account, token, prompt, out_path)

