# Author: Andrew Higgins
# https://github.com/speckly

# One-time use file, for transitioning the images to
# Therefore it is deprecated as labels in the filename are also discontinued, use subfolders instead

import os
import shutil

def move_files(directory=".", MANUAL=True):
    for filename in os.listdir(directory):
        current = os.path.join(directory, filename)
        if current.endswith(".jpg") or current.endswith(".jpeg"):
            status = process_file(filename, directory, MANUAL)
            if status == -1:
                print(f"{filename} was not moved successfully")
            else:
                print(f"{filename} was moved successfully")           

def process_file(filename, directory, MANUAL=True):
    labels = ["negative", "positive", "neutral", "ummmmmmm"]
    folder = ""
    for label in labels:
        if label in filename.lower():
            folder = f'{directory}/{label}' if label != 'ummmmmmm' else f'{directory}/neutral'
            break
    if folder == "":
        return -1

    if MANUAL == False:
        user_input = input(f"\n{filename} will be moved to {folder}, enter 0 to abort this action")
        if user_input.strip() == "0":
            return -1

    shutil.move(f'{directory}/{filename}', folder)
    return 0

if __name__ == "__main__":
    MANUAL = True
    if MANUAL == False:
        target_directory = f"../images/{input('Input the directory: ')}"
        move_files(target_directory, MANUAL)
    else:
        for i in range(0, 26):
            if i == 9: # i dont know where did 9 go
                continue
            cwd = f"../images/catgirls-{i}"
            print(f"Current directory: {cwd}")
            subfolders = ["positive", "negative", "neutral"]

            for subfolder in subfolders:
                subfolder_path = os.path.join(cwd, subfolder)
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                    print(f"Created subfolder: {subfolder_path}")

            move_files(cwd)

    print("File renaming completed.")
