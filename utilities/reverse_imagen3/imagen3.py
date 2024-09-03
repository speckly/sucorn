"""Author: Andrew Higgins
https://github.com/speckly

single image case, hard to see for those more than 1
{
    "imagePanels": [
        {
        "prompt": "A whimsical anime catgirl with beautiful eyes and long, flowing pink hair, playfully bouncing on a brightly colored space hopper, anime style",
        "generatedImages": [
            {
            "encodedImage": "",
            "seed": 329995,
            "mediaGenerationId": "CAMaJDNlNjk3YzkwLWZlMDItNGU4OS04MDBhLWNjZjZiMWE4MWY4NSIDQ0FFKiQ5NjE1MWM1MS0zZjAzLTQzN2ItYjY0Yi0xNzkzZmIyZTQzMjk",
            "isMaskEditedImage": false,
            "modelNameType": "IMAGEN_3",
            "workflowId": "3e697c90-fe02-4e89-800a-ccf6b1a81f85"
            }
        ]
        }
    ]
}
"""

import os
import random
import contextlib
import base64
import time
import argparse
import ctypes
import sys
from typing import Union
import requests
from dotenv import load_dotenv
from get_auth import get_access_token

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
FORWARDED_IP = (
    f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
)
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.5",
    "cache-control": "max-age=0",
    "content-type": "application/json",
    "referrer": "https://aitestkitchen.withgoogle.com/",
    "origin": "https://aitestkitchen.withgoogle.com",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
    "x-forwarded-for": FORWARDED_IP,
}

# "https://aitestkitchen.withgoogle.com/api/trpc/media.generateEnhancedPrompt"
# for showing what the enhanced prompt is
ENDPOINT = "https://aisandbox-pa.googleapis.com/v1:runImageFx"

class ImageGen:
    """
    Image generation by ImageFX
    Parameters:
        authorization: str, authorisation token found in your Bearer <auth>
        lazy to document do it another time sorry
    """

    def __init__(
        self,
        authorization: str,
        output_folder: str,
        debug_file: Union[str, None] = None
    ) -> None:
        self.auth = authorization
        self.output_folder = output_folder
        self.debug_file = debug_file
        self.session: requests.Session = requests.Session()
        self.session.headers = HEADERS
        self.session.headers.update({
            'Authorization': f'Bearer {self.auth}'
        })

    def get_images(self, prompt: str) -> int:
        """
        Fetches image encodings, requires auth
        Parameters:
            prompt: str

        DEV: observe seed, highest is 764k
        clientContext session is removed lets see what happens
        candidatesCount can go up to umm 8, leave it at 4 to be safe, doesnt seem to ever return more than 4?
        """
        body = {
            "userInput": {
                "candidatesCount": 8,
                "prompts": [
                    prompt
                ],
                "seed": random.randint(1,1000000)
            },
            "clientContext": {
                "tool":"IMAGE_FX"
            },
            "modelInput": {
                "modelNameType": "IMAGEN_3"
            }
        }
        s = time.time()
        response = self.session.post(
            ENDPOINT,
            allow_redirects=False,
            timeout=200,
            json=body
        )
        print(f"{time.time()-s:.4f}s server response")

        if response.status_code == 200:
            res_json = response.json()
            print(f"There are {len(res_json['imagePanels'])} image panels")
            for image_panel in res_json["imagePanels"]:
                print(f"There are {len(image_panel['generatedImages'])} image(s) in this panel")
                for generated_image in image_panel["generatedImages"]:
                    self.save_image(generated_image["encodedImage"], prompt)
        elif not (response.status_code == 429 or response.status_code == 401):
            if response.status_code == 400:
                print("Bad images")
            else:
                print(f"Failed with HTTP {response.status_code}:\n{response.text}")
        else:
            return response.status_code
        return 0

    def save_image(
        self,
        encoded_image: list,
        prompt: str
    ) -> None:
        """
        Saves images to output directory
        Parameters:
        consider flexibility in output dir or file name?
        """
        with contextlib.suppress(FileExistsError):
            os.mkdir(self.output_folder)
            print("Created folder as it did not exist")
            with open(os.path.join(self.output_folder, "prompt.txt"), "w", encoding='utf-8') as file:
                file.write(prompt)

        png_index = 0
        while os.path.exists(os.path.join(self.output_folder, f"{png_index}.png")):
            png_index += 1
        with open(os.path.join(self.output_folder, f"{png_index}.png"), "wb") as output_file:
            output_file.write(base64.b64decode(encoded_image))
        png_index += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="Name of the variable to access in the .env")
    parser.add_argument("-f", "--folder", type=str,
        help="Output folder for images, default is images folder at the top level", default=f'{DIRECTORY}/../../images')
    # TODO: handle above better
    parser.add_argument("-d", "--delay", type=float, help="Delay between requests", default=0)
    args = parser.parse_args()
    delay = args.delay

    # TODO: dynamic instances
    with open(f"{DIRECTORY}/prompt.txt", "r", encoding='utf-8') as p_file:
        prompt = p_file.read().replace("\n", " ") # NOTE: doubt

    load_dotenv()
    name = args.name
    test_generator = ImageGen(authorization=get_access_token(cookie_str=os.getenv(name)), debug_file=None, output_folder=args.folder)
    cycle = 1
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name} sucorn API")
    else:
        sys.stdout.write(f"\x1b]2;sucorn API {name}\x07")

    while True:
        print(f"Cycle {cycle}")
        terminate = test_generator.get_images(prompt=prompt) # 0, 401 or 429
        if terminate == 429:
            print("HTTP 429 received, you have exceeded your daily quota, try again tomorrow")
            break
        elif terminate == 401:
            print("HTTP 401 received, your token might have expired")
            break
        cycle += 1
        time.sleep(delay)

# Terminate case, remove the string from the .env file
if input("Remove the account from the .env file?").strip().lower() in ["y", ""]:
    if not os.path.exists(f"{DIRECTORY}/.env"):
        print(".env file does not exist. How did you even run this file")
    else:
        # store temporarily, what if its really big hmmmmmmmmm
        with open(f"{DIRECTORY}/.env", 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(f"{DIRECTORY}/.env", 'w', encoding='utf-8') as file:
            for line in lines:
                if not line.strip().startswith(f"{name}="):
                    file.write(line)
            print(f"Removed {name} from .env file.")
