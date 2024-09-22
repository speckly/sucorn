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

def open_console_window(name: str, out_folder: str, delay: float=None):
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    Spawns a child process
    """

    spawn = ['start', 'cmd', '/k']
    process = subprocess.Popen(
        spawn + ['python', f'{DIRECTORY}/imagen3.py', name] + ['-f', out_folder] if out_folder else []
        + ['-d', delay] if delay else [],
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
    """Author: Andrew Higgins
    https://github.com/speckly

    sucorn project data preparation phase
    Terminates all the child processes"""
    windows = gw.getWindowsWithTitle("sucorn API")
    for window in windows:
        ctypes.windll.user32.PostMessageW(window._hWnd, 0x0010, 0, 0)
    print("Terminated")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kitty farm')
    parser.add_argument('folder', type=str, help='folder name, ./images/your_name_here')
    parser.add_argument('-d', '--delay', type=float, default=0,
        help='Delay time in seconds (default is 0)')
    parser.add_argument('-l', '--log', action='store_true',
        help='Logs all errors to /logs') # TODO: implement
    args = parser.parse_args()

    out_path = args.folder

    COOKIE_FILE = f'{DIRECTORY}/.env'
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, encoding="utf-8") as f:
            cookies = f.readlines()
    else:
        print(".env does not exist, quitting since no cookies were found.")
        quit()

    if len(cookies):
        pf = platform.system()
        if pf != "Windows":
            print("This is intended for Windows only")
            quit()
        for line in cookies:
            open_console_window(line.split("=")[0], out_path, args.delay)

        keyboard.on_press_key('ins', organize_windows)
        keyboard.wait('end')

        terminate()
