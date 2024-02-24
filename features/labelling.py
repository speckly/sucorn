# Author: Andrew Higgins
# https://github.com/speckly

# NOTE: Hardcoded image offset
# TODO: what i just said above

from tkinter import Tk, Canvas, Label, RIGHT
from PIL import Image, ImageTk, ImageFilter
import os

class ImageLabeler:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_files = [f for f in os.listdir(folder_path) if f.lower().endswith('xxxxxxxx.jpg') or f.lower().endswith('xxxxxxxx.jpeg')]
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
        base_name, extension = os.path.splitext(current_file)
        new_filename = base_name.replace("_xxxxxxxx", "") + label + extension
        os.rename(os.path.join(self.folder_path, current_file), os.path.join(self.folder_path, new_filename))

        self.next_image()

    def next_image(self):
        self.current_index += 1
        if self.current_index < self.files:
            self.show_image()
        else:
            print("All images labeled. Exiting.")
            self.root.destroy()

    def show_image(self):
        current_file = self.image_files[self.current_index]
        image_path = os.path.join(self.folder_path, current_file)

        original_image = Image.open(image_path)
        aspect_ratio = original_image.width / original_image.height

        # Calculate the new width and height to maintain 1:1 aspect ratio
        new_width = min(self.root.winfo_width(), int(self.root.winfo_height() * aspect_ratio))
        new_height = int(new_width / aspect_ratio)

        # Resize the image using LANCZOS method
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)

        self.label.config(image=self.photo)
        self.label.image = self.photo
        info = f"""
Current file: {current_file}
Progress: {self.current_index}/{self.files}"""
        self.image_label.config(text=info)

        self.root.update_idletasks()
        self.root.update()


def main():
    while True:
        folder_path = f"../images/{input('Input folder name of images: ')}"
        if os.path.isdir(folder_path):
            break
        else:
            print('Directory not found')

    image_labeler = ImageLabeler(folder_path)
    image_labeler.show_image()
    image_labeler.root.mainloop()

if __name__ == "__main__":
    main()
