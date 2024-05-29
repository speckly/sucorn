"""
Author: Andrew Higgins
https://github.com/speckly

labelling.py V2, makes use of folders to label images.
This is a GUI tool that shows the current image being labelled and moves it to
its respective folder depending on the keyboard input
0 is negative, 1 is positive, 2 is neutral
"""

import os
import argparse
import shutil
from tkinter import Tk, Canvas, Label, RIGHT
from PIL import Image, ImageTk, UnidentifiedImageError

def map_path(abs_path: str) -> str:
    """
    Author: Andrew Higgins
    https://github.com/speckly

    Input: path to the file
    Output: prefix folder to this  
    """
    labels = ["positive", "negative", "neutral"]
    for label in labels:
        if label in abs_path:
            return f"{label}/"
    return ""

class ImageLabeler:
    """
    Author: Andrew Higgins
    https://github.com/speckly

    Tkinter labeller that shows the current image being labelled and moves it to
    its respective folder depending on the keyboard input
    0 is negative, 1 is positive, 2 is neutral
    """
    def __init__(self, folder_path, options={}):
        self.folder_path = folder_path
        self.rewrite = options.get("rewrite")
        category = options.get("category")

        if self.rewrite:
            self.image_files = [f"{map_path(dirpath)}{filename}"
                                for dirpath, _, filenames in os.walk(folder_path)
                                for filename in filenames
                                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg')]
        elif category is not None:
            self.image_files = [f"{category}/{filename}"
                                for filename in os.listdir(f"{folder_path}/{category}")
                                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg')]
        else:
            self.image_files = [filename
                                for filename in os.listdir(folder_path)
                                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg')]
        self.files = len(self.image_files)
        if self.files == 0:
            print("All images labeled. Quitting")
            exit(0)
        self.current_index = 0

        self.root = Tk()
        self.root.title("Image Labeler")
        self.root.attributes('-fullscreen', True)

        self.label = Label(self.root)
        self.label.pack(expand=True, fill="both", side="left")

        self.image_label = Label(self.root, text="", anchor="e", padx=10)
        self.image_label.pack(side=RIGHT)

        self.canvas = Canvas(self.root)
        self.canvas.pack(expand=True, fill="both")

        self.root.bind('2', lambda event: self.label_image('_neutral'))
        self.root.bind('1', lambda event: self.label_image('_positive'))
        self.root.bind('0', lambda event: self.label_image('_negative'))
        self.root.bind('<Escape>', self.escape)
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.show_image()

    def escape(self, d1):
        # d1 -> <KeyPress event send_event=True state=Mod1 keysym=Escape keycode=27 char='\x1b' x=1315 y=743>
        print('Program terminated')
        self.root.destroy()
        exit(0)

    def label_image(self, label):
        current_file = self.image_files[self.current_index]

        source_path = os.path.join(self.folder_path, current_file)
        destination_folder = None

        if label == '_positive':
            destination_folder = os.path.join(self.folder_path, 'positive')
        elif label == '_negative':
            destination_folder = os.path.join(self.folder_path, 'negative')
        elif label == '_neutral':
            destination_folder = os.path.join(self.folder_path, 'neutral')

        if destination_folder:
            destination_path = os.path.join(destination_folder, current_file.split("/")[-1]) # Get file name only

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            shutil.move(source_path, destination_path)
        else:
            print(f"Invalid label: {label}") # Should not happen

        self.next_image()

    def next_image(self):
        self.current_index += 1
        if self.current_index < self.files:
            try:
                self.show_image()
            except UnidentifiedImageError: # UnidentifiedImageError
                print("skipping")
                self.next_image()
        else:
            print("All images labeled. Exiting.")
            self.root.destroy()

    def show_image(self):
        current_file = self.image_files[self.current_index]
        image_path = os.path.join(self.folder_path, current_file)

        try:
            original_image = Image.open(image_path)
        except:
            return
        aspect_ratio = original_image.width / original_image.height

        new_width = min(self.root.winfo_width(), int(self.root.winfo_height() * aspect_ratio))
        new_height = int(new_width / aspect_ratio)

        resized_image = original_image.resize((new_width, new_height)) # Image.LANCZOS does not exist
        photo = ImageTk.PhotoImage(resized_image)

        self.label.config(image=photo)
        self.label.image = photo
        info = f"""
Current file: {current_file}
Progress: {self.current_index}/{self.files}"""
        self.image_label.config(text=info)

        self.root.update_idletasks()
        self.root.update()


def main():
    """cli tool that launches a labelling program, labels only files with a placeholder "xxxxxxxx"
    Press 0 for negative, 1 for positive and 2 for unsure
    Required positional argument: folder-name
    --rewrite: adds already labeled images to the labeller, will overwrite the old label"""
    parser = argparse.ArgumentParser(description='Image Labeling Program')
    parser.add_argument('folder_name', type=str, help='Folder name of images')
    parser.add_argument('--rewrite', action='store_true', help='Rewrite all images regardlesss of label')
    parser.add_argument('--reset', action='store_true', help='Reset images')
    parser.add_argument('-c', '--category', choices=['positive', 'negative', 'neutral'], help='Label images with the following category')

    args = parser.parse_args()
    options = {"rewrite": args.rewrite, "category": args.category}

    folder_path = f"{os.path.dirname(os.path.realpath(__file__))}/../images/{args.folder_name}"
    if not os.path.isdir(folder_path):
        print(f'Directory not found: {folder_path}')
        return
    else:
        for subfolder in ['positive', 'neutral', 'negative']:
            subfolder_path = os.path.join(folder_path, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
                print(f"Created folder as it does not exist: {subfolder_path}") 

    if args.reset: # TODO: Update for new structure
        confirmation = input(f"Are you sure you wish to reset the labels of the following directory? {args.folder_name} (N) ")
        if confirmation.lower() != "y":
            print("Quitting")
            return
        else:
            for current_file in [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')]:
                base_name, extension = os.path.splitext(current_file)
                for replacements in ["_Positive", "_Negative", "_positive", "_negative"]:
                    base_name = base_name.replace(replacements, "")
                new_filename = base_name + extension
                os.rename(os.path.join(folder_path, current_file), os.path.join(folder_path, new_filename))
            print("Reset")
            return
    
    image_labeler = ImageLabeler(folder_path=folder_path, options=options)
    image_labeler.show_image()
    image_labeler.root.mainloop()

if __name__ == "__main__":
    main()
