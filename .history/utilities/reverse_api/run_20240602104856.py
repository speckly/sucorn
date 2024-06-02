import os
import json
import subprocess
import ctypes
import argparse
import platform
import keyboard
import pygetwindow as gw

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

def read_prompt():
    PROMPT_FILE = f"{DIRECTORY}/prompt.txt"
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, encoding="utf-8") as f:
            prompt = ''.join(f.readlines()).replace('\n', '')
    else:
        prompt = input("prompt.txt does not exist, enter your prompt here to be saved to prompt.txt -> ")
        with open(PROMPT_FILE, 'w', encoding="utf-8") as f:
            f.write(prompt)
    return prompt

def open_console_window(name: str, account_token: str, prompt: str, out_folder: str, delay: float, maximum: int):
    if platform.system() == 'Windows':
        spawn = ['start', 'cmd', '/k']
        creationflags = subprocess.CREATE_NEW_CONSOLE
    elif platform.system() == "Darwin":
        script = f"""
        tell application "Terminal"
            do script "python3 '{DIRECTORY}/sub.py' '{name.split('@')[0]}' '{account_token}' '{prompt}' '{out_folder}' '{delay}' '{maximum}'"
            activate
        end tell
        """
        process = subprocess.Popen(['osascript', '-e', script])
        return process
    else:
        spawn = ['x-terminal-emulator', '-e']
        creationflags = 0
        process = subprocess.Popen(
            spawn + ['python3', f'{DIRECTORY}/sub.py', name.split("@")[0], account_token,
                     prompt, out_folder, str(delay), str(maximum)],
            shell=True,
            creationflags=creationflags
        )
        return process

def organize_windows(dummy):
    columns = 5
    window_width = 450
    window_height = 240

    windows = gw.getWindowsWithTitle('sucorn API')

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
    windows = gw.getWindowsWithTitle("sucorn API")
    for window in windows:
        ctypes.windll.user32.PostMessageW(window._hWnd, 0x0010, 0, 0)
    print("Terminated")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kitty farm')
    parser.add_argument('folder', type=str, help='folder name, ./images/your_name_here')
    parser.add_argument('-d', '--delay', type=float, default=0, help='Delay time in seconds (default is 0)')
    parser.add_argument('-m', '--max', type=int, default=80, help='Maximum number of failed redirects before killing process (default is 80)')
    parser.add_argument('-t', '--test', action='store_true', help='Runs the program with a testing cookie file named test_cookies.json (default is False)')
    parser.add_argument('-l', '--log', action='store_true', help='Logs all errors to /logs')
    args = parser.parse_args()

    out_path = f"{DIRECTORY}/../../images/{args.folder}"
    if not os.path.exists(out_path):
        os.mkdir(out_path)
        prompt = read_prompt()
        with open(f"{out_path}/prompt.txt", "w", encoding="utf-8") as p_file:
            p_file.write(prompt)
    else:
        with open(f"{out_path}/prompt.txt", "r", encoding="utf-8") as p_file:
            prompt = p_file.read()

    for subfolder in ['positive', 'neutral', 'negative']:
        subfolder_path = f"{out_path}/{subfolder}"
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
            print(f"Created folder as it does not exist: {subfolder_path}")

    COOKIE_FILE = f'{DIRECTORY}/cookies.json' if args.test is False else f'{DIRECTORY}/test_cookies.json'
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, encoding="utf-8") as f:
            cookies = json.load(f)
    else:
        print("cookies.json does not exist, quitting since no cookies were found.")
        quit()

    if len(prompt) > 480 and input("Prompt is over 480, continue? (Y or N) ").lower().strip() == "n":
        quit()

    if len(cookies.items()):
        prompt = prompt.replace('\n', ' ').strip()
        for account, token in cookies.items():
            open_console_window(account, token, prompt, out_path, args.delay, args.max)

        keyboard.on_press_key('f5', organize_windows)  # Changed 'ins' to 'f5'
        keyboard.wait('end')

        terminate()
