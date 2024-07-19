"""
Author: Andrew Higgins
https://github.com/speckly

ok actually this isnt really a dataset maker but it just takes images recursively and it puts it in a folder
"""

import os
import shutil

def get_unique_filename(dest_dir, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename

    while os.path.exists(os.path.join(dest_dir, unique_filename)):
        unique_filename = f"{base}_{counter}{extension}"
        counter += 1

    return unique_filename

def gather_jpeg_images(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith('.jpeg'):
                file_path = os.path.join(root, file)
                unique_filename = get_unique_filename(dest_dir, file)
                shutil.copy(file_path, os.path.join(dest_dir, unique_filename))
                print(f'Copied: {file_path} to {os.path.join(dest_dir, unique_filename)}')

source_directory = '../images/filtered'
destination_directory = '../images/dataset2'

gather_jpeg_images(source_directory, destination_directory)
