import subprocess
import argparse
import platform
import keyboard
import os

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

def open_console_window(out_folder: str, name: str, delay: float, venv: bool = False):
    name = name.split("@")[0]
    if platform.system() == 'Linux':
        spawn = ['xfce4-terminal', '--hold', '-T', f'sucorn API {name}', '-e']
    else:
        raise OSError("This script is intended for Linux environments only")

    # BUG: venv not working, thank goodness sub.py only needs 1 requirement, maybe put in sh shell?
    command = f'sudo -u {os.getenv("SUDO_USER")} {f'{DIRECTORY}/../../venv/bin/' if venv else ""}python "{DIRECTORY}/imagen3.py" "{out_folder}" -d {delay} -n {name}'
    process = subprocess.Popen(
        spawn + [command.replace("'", "\\'")],
    )
    return process

def organize_windows(dummy):
    columns = 5
    window_width = 450
    window_height = 240

    result = subprocess.run(['wmctrl', '-l'], stdout=subprocess.PIPE, check=True)
    windows = [line for line in result.stdout.decode().split('\n') if 'sucorn API' in line]

    for i, window in enumerate(windows):
        window_id = window.split()[0]

        row = i // columns
        col = i % columns

        x_position = col * (window_width - 10)
        y_position = row * (window_height + 2)

        subprocess.run(['wmctrl', '-ir', window_id, '-e', f'0,{x_position},{y_position},{window_width},{window_height}'], check=True)

def terminate():
    result = subprocess.run(['wmctrl', '-l'], stdout=subprocess.PIPE, check=True)
    windows = [line for line in result.stdout.decode().split('\n') if 'sucorn API' in line]

    for window in windows:
        window_id = window.split()[0]
        subprocess.run(['wmctrl', '-ic', window_id], check=True)
    print("Terminated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kitty farm AGAIN')
    parser.add_argument('folder', type=str, help='folder name, ./images/your_name_here')
    parser.add_argument('-d', '--delay', type=float, default=0,
        help='Delay time in seconds (default is 0)')
    parser.add_argument('-v', '--venv', action='store_true',
        help='Use venv located in top level directory')
    args = parser.parse_args()

    sudo_user = os.getenv("SUDO_USER")
    if not sudo_user:
        print("You need to be the superuser to use this (blame keyboard module)")
        quit()

    with open(".env") as e_file:
        names = [line.split("=")[0] for line in e_file.readlines()]
    for name in names:
        open_console_window(args.folder, name, args.delay, venv=args.venv)

    keyboard.on_press_key('ins', organize_windows)
    keyboard.wait('end')

    terminate()
