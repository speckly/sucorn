import json
import subprocess
import pygetwindow as gw
import ctypes
import keyboard
import argparse
import os

def open_console_window(account, token, prompt, out_path, delay=0, maximum=10):
    process = subprocess.Popen(
        ['start', 'cmd', '/k', 'python', 'sub.py', account, token, prompt, out_path, str(delay), str(maximum)],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return process

def organize_windows(dummy):
    rows = 3
    columns = 4
    window_width = 450
    window_height = 270

    windows = gw.getWindowsWithTitle('reverse_api')

    for i, window in enumerate(windows):
        window.minimize()
        window.maximize()

        row = i // columns
        col = i % columns

        x_position = col * (window_width - 10)
        y_position = row * (window_height + 2)

        window.moveTo(x_position, y_position)
        window.resizeTo(window_width, window_height)
        

def terminate():
    windows = gw.getWindowsWithTitle("reverse_api")
    for window in windows:
        ctypes.windll.user32.PostMessageW(window._hWnd, 0x0010, 0, 0)
    print("Terminated")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kitty farm')
    parser.add_argument('number', type=str, help='folder catgirls-n')
    parser.add_argument('-d', '--delay', type=float, default=0, help='Delay time in seconds (default is 0)')
    parser.add_argument('-m', '--max', type=int, default=10, help='Maximum number of failed redirects before killing process (default is 10)')
    parser.add_argument('-t', '--test', type=bool, default=False, help='Runs the program with a testing cookie file named test_cookies.json (default is False)')
    args = parser.parse_args()

    OUT_PATH = f"..\..\\images\\catgirls-{args.number}\\"
    for subfolder in ['positive', 'neutral', 'negative']:
        subfolder_path = os.path.join(OUT_PATH, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
            print(f"Created folder as it does not exist: {subfolder_path}")

    if os.path.exists('prompt.txt'):
        with open('prompt.txt') as f:
            PROMPT = ''.join(f.readlines()).replace('\n', '')
    else:
        PROMPT = input("prompt.txt does not exist, enter your prompt here to be saved to prompt.txt -> ")
        with open("prompt.txt") as f:
            f.write(PROMPT)
    cookie_file = 'cookies.json' if args.test == False else 'test_cookies.json'
    if os.path.exists(cookie_file):
        with open(cookie_file) as f:
            cookies = json.load(f)
    else:
        print("cookies.json does not exist, quitting since no cookies were found.")
        quit()

    if len(PROMPT) > 480:
        if input("Prompt is over 480, continue? (Y or N) ").lower().strip() == "n":
            quit()
    elif len(cookies.items()):
        for account, token in cookies.items():
            open_console_window(account, token, PROMPT, OUT_PATH, args.delay, args.max)

        keyboard.on_press_key('ins', organize_windows)
        keyboard.wait('end')

        terminate()
    