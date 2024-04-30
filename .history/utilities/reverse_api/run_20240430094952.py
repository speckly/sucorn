"""Author: Andrew Higgins
https://github.com/speckly

sucorn project data preparation phase
Top level cli tool to manage and spawn child processes according
to given settings in arguments to automate the image creation process"""

import os
import json
import subprocess
import ctypes
import argparse
import platform
import keyboard
import pygetwindow as gw

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

def open_console_window(name: str, account_token: str, prompt: str, out_folder: str, delay: float, maximum: int):
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    Spawns a child process"""
    if platform.system() == 'Windows':
        spawn = ['start', 'cmd', '/k']
    elif platform.system() == "Darwin":
        spawn = ['open', '-a', 'Terminal.app']
    process = subprocess.Popen(
        spawn + ['python', f'{DIRECTORY}\\sub.py', name, account_token,
            prompt, out_folder, str(delay), str(maximum)],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return process

def organize_windows(dummy):
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    Organises the child processes, or brings them to view
    TODO: Dynamic for all resolutions"""

    columns = 5
    window_width = 450
    window_height = 240

    windows = gw.getWindowsWithTitle('reverse_api')

    for i, window in enumerate(windows):
        window.minimize()
        window.maximize()

        row = i // columns
        col = i % columns

        x_position = col * (window_width - 10)
        y_position = row * (window_height + 2)

        window.resizeTo(window_width, window_height)
        window.moveTo(x_position, y_position)

def terminate():
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    Terminates all the child processes"""
    windows = gw.getWindowsWithTitle("reverse_api")
    for window in windows:
        ctypes.windll.user32.PostMessageW(window._hWnd, 0x0010, 0, 0)
    print("Terminated")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kitty farm')
    parser.add_argument('folder', type=str, help='folder name, ./images/your_name_here')
    parser.add_argument('-d', '--delay', type=float, default=0,
        help='Delay time in seconds (default is 0)')
    parser.add_argument('-m', '--max', type=int, default=80,
        help='Maximum number of failed redirects before killing process (default is 80)')
    parser.add_argument('-t', '--test', type=bool, default=False,
        help='Runs the program with a testing cookie file named test_cookies.json (default is False)')
    args = parser.parse_args()

    out_path = f"{DIRECTORY}\\..\\..\\images\\{args.folder}\\"
    for subfolder in ['positive', 'neutral', 'negative']:
        subfolder_path = f"{out_path}\\{subfolder}"
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
            print(f"Created folder as it does not exist: {subfolder_path}")
    out_path = f'../../images/{args.folder}' # BUG: The trolling done here

    PROMPT_FILE = f"{DIRECTORY}/prompt.txt"
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, encoding="utf-8") as f:
            PROMPT = ''.join(f.readlines()).replace('\n', '')
    else:
        PROMPT = input("prompt.txt does not exist, enter your prompt here to be saved to prompt.txt -> ")
        with open(PROMPT_FILE, encoding="utf-8") as f:
            f.write(PROMPT)

    COOKIE_FILE = f'{DIRECTORY}/cookies.json' if args.test is False else f'{DIRECTORY}/test_cookies.json'
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, encoding="utf-8") as f:
            cookies = json.load(f)
    else:
        print("cookies.json does not exist, quitting since no cookies were found.")
        quit()

    if len(PROMPT) > 480:
        if input("Prompt is over 480, continue? (Y or N) ").lower().strip() == "n":
            quit()
    elif len(cookies.items()):
        for account, token in cookies.items():
            open_console_window(account, token, PROMPT, out_path, args.delay, args.max)

        keyboard.on_press_key('ins', organize_windows)
        keyboard.wait('end')

        terminate()
    