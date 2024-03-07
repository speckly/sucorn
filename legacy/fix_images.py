# Author: Andrew Higgins
# https://github.com/speckly

# One-time use file, for cleaning up the images with duplicate labels in the filename
# Therefore it is deprecated as labels in the filename are also discontinued, use subfolders instead

import os

def rename_files(directory=".", MANUAL=True):
    for filename in os.listdir(directory):
        current = os.path.join(directory, filename)
        if current.endswith(".jpg") or current.endswith(".jpeg"):
            if current.count("negative") + current.count("positive") + current.count("ummmmmmm") + current.count("neutral") > 1:
                new_filename = process_filename(filename, MANUAL)
                if new_filename != -1:
                    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

def process_filename(filename, MANUAL=True):
    if MANUAL == False:
        user_input = input(f"\n{filename} has duplicate labels, enter the new filename or press enter for the default fix, 0 to quit: ")
        if user_input.strip() == "0":
            exit()

    if MANUAL == False and user_input.strip().lower() != "":
        new_filename = user_input 
    else:
        parts = filename.split('_')
        labels = ["negative", "positive", "neutral", "ummmmmmm"]
        preserved_label = parts.pop(-1)
        new_parts = list(filter(lambda part: all(label not in part for label in labels), parts)) + ["_" + preserved_label]
        new_filename = "".join(new_parts)
        if MANUAL == False and input(f"Confirm the new filename is {new_filename}? (Y): ").lower().strip() == "n":
            print("Ignoring this file")
            return -1

    print(f"Renamed to {new_filename}")
    return new_filename

if __name__ == "__main__":
    MANUAL = False
    if MANUAL:
        target_directory = f"../images/{input('Input the directory: ')}"
        rename_files(target_directory, MANUAL)
    else:
        for i in range(10, 26):
            print(f"Current directory number: {i}")
            rename_files(f"../images/catgirls-{i}")
    print("File renaming completed.")
