import random
import os
from typing import Union
import requests
from dotenv import load_dotenv
import contextlib
import base64
import time

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

# v1runimagefx comes first, what is aitestkitchen for then? "https://aitestkitchen.withgoogle.com/api/trpc/media.generateEnhancedPrompt"
# edit: its for showing what the enhanced prompt is smh
ENDPOINT = "https://aisandbox-pa.googleapis.com/v1:runImageFx"

class ImageGen:
    """
    Image generation by ImageFX
    Parameters:
        authorization: str, authorisation token found in your Bearer <auth>
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
        print(f"{time.time()-s}s server response")
        """ single image case, hard to see for those more than 1
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
        if response.status_code == 200:
            res_json = response.json()
            print(f"There are {len(res_json['imagePanels'])} image panels")
            for image_panel in res_json["imagePanels"]:
                print(f"There are {len(image_panel['generatedImages'])} images in this panel")
                for generated_image in image_panel["generatedImages"]:
                    self.save_image(generated_image["encodedImage"], prompt)
        elif response.status_code != 429:
            print(f"Failed with HTTP {response.status_code}:\n{response.text}")
            """usually this
            {
                "error": {
                    "code": 400,
                    "message": "Request contains an invalid argument.",
                    "status": "INVALID_ARGUMENT"
                }
            }"""
        else:
            return 1
        return 0

    def save_image(
        self,
        encodedImage: list,
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
            with open(os.path.join(self.output_folder, "prompt.txt"), "w") as file:
                file.write(prompt)

        png_index = 0
        while os.path.exists(os.path.join(self.output_folder, f"{png_index}.png")):
            png_index += 1
        with open(os.path.join(self.output_folder, f"{png_index}.png"), "wb") as output_file:
            output_file.write(base64.b64decode(encodedImage))
        png_index += 1

if __name__ == "__main__":
    prompt = "a single anime girl with cat ears and tail bouncing around on a space hopper, girl is high up in the air, in a race" # TODO: use arguments
    load_dotenv()
    test_generator = ImageGen(authorization=os.getenv("auth"), debug_file=None, output_folder="../../images/imagen3/fr_1")
    cycle = 1
    while True:
        print(f"Cycle {cycle}")
        terminate = test_generator.get_images(prompt=prompt)
        if terminate:
            print("HTTP 429 received, you have exceeded your daily quota, try again tomorrow")
            break
        cycle += 1
        # time.sleep(10)