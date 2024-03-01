import json
import subprocess
import pygetwindow as gw
import ctypes
import time
import keyboard

def open_console_window(account, token, prompt, out_path):
    process = subprocess.Popen(
        ['start', 'cmd', '/k', 'python', 'sub.py', account, token, prompt, out_path],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return process

def organize_windows(dummy):
    rows = 3  # Adjust the number of rows based on your preference
    columns = 4  # Adjust the number of columns based on your preference
    window_width = 450  # Adjust the width of each window based on your preference
    window_height = 270  # Adjust the height of each window based on your preference

    windows = gw.getWindowsWithTitle('reverse_api')

    for i, window in enumerate(windows):
        window.minimize()
        window.maximize()

        row = i // columns
        col = i % columns

        x_position = 10 + col * (window_width + 2)
        y_position = 10 + row * (window_height + 2)

        window.moveTo(x_position, y_position)
        window.resizeTo(window_width, window_height)
        

def terminate():
    windows = gw.getWindowsWithTitle("reverse_api")
    for window in windows:
        ctypes.windll.user32.PostMessageW(window._hWnd, 0x0010, 0, 0)
    print("Terminated")

if __name__ == "__main__":
    OUT_PATH = "..\..\\images\\catgirls-24"
    with open('prompt.txt') as f:
        PROMPT = ''.join(f.readlines()).replace('\n', '')
    with open("test_cookies.json") as f:
        cookies = json.load(f)

    if len(PROMPT) > 480:
        input("Prompt is over 480, continue? ")
    for account, token in cookies.items():
        open_console_window(account, token, PROMPT, OUT_PATH)

    keyboard.on_press_key('ins', organize_windows)

    keyboard.wait('end')
    terminate()
    