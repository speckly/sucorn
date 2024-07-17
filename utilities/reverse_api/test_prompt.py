"""Author: Andrew Higgins
https://github.com/speckly

sucorn project data preparation phase
utility to test a prompt to see if it is allowed

BUG: Not tested"""

import json
import os
import argparse
import asyncio
from BingImageCreator import ImageGen

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser()
parser.add_argument("prompt_file", type=str, help="Your prompt to test, provide the location that it is stored in (prompt.txt)")

args = parser.parse_args()
try:
    with open(args.prompt_file) as p_file:
        prompt = p_file.read().replace("\n", " ").strip()
except FileNotFoundError:
    print("prompt file does not exist, quitting")
    quit()

print(f"Your prompt is '{prompt}'")

COOKIE_FILE = f'{DIRECTORY}/cookies.json'
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, encoding="utf-8") as f:
        cookies = json.load(f)
else:
    print("cookies.json does not exist, quitting since no cookies were found.")
    quit()

auth = cookies[list(cookies.keys())[0]]
image_generator = ImageGen(
    auth,
    None
)

image_generator.get_images(prompt)