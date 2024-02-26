from ntpath import basename
from requests import get, exceptions
import os

try: 
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    if input(f"BeautifulSoup4 is required to run this program, execute pip install bs4? (Y): ").lower().strip() in ["", "y"]:
        os.system(f"pip install bs4")
    else:
        exit()
        
import re

def catRescue(URL: str) -> list:
    """
Author: @speckly
https://github.com/speckly

-- Cat Rescue --
This gets the full image of the nya nya nyan (i mean ) from a Bing Image AI link with 1-4 nya images nyan
Uses Beautiful Soup 4

-- Inputs --
URL of the collage nyan

-- Process --
Legacy: Individual full href can be found on <a class="iusc">. Opens the href and extracts the full URL.

Eliminates the parameter that shrinks the image with class "mimg" and therefore not requiring to open the full URL

-- Outputs --
List of embeddable hrefs of nyan, nyan be used in Discord, master."""

    rawHTML: bytes = get(URL).text
    soup: BeautifulSoup = BeautifulSoup(rawHTML, "html5lib")
    PREFIX = "https://th.bing.com/th/id/"

    # Don't worry about memory, its just up to 4 links
    elements = soup.find_all('img', class_='mimg') #get elements
    if not elements:
        elements = soup.find_all('img', class_='gir_mmimg') #get elements
    full_links = [link.get('src') for link in elements]
    #Thanks OpenAI for the regex for ID
    pattern = r'id/([^/?]+)'
    links = [PREFIX + re.search(pattern, url).group(1) for url in full_links]

    # Assume only one element, I dont know why firefox shows input while here it is textarea
    textinput = soup.find('textarea', {'id': 'sb_form_q'})
    if textinput:
        prompt = textinput.text
    else:
        prompt = ''

    return links, prompt

def catDownloader(URL: str, folder_name: str, mode: str, placeholder: bool=False) -> str:
    """
Author: @speckly
https://github.com/speckly

-- Cat Downloader --
Downloading of images customized for the use with the sucorn bot, triggered when the Discord buttons
are clicked. Features customised filename suffix saving.
NOTE: assumes that given page returns image only

-- Inputs --
URL: remote image
folder_name: folder name to save image in ./images/{folder_name}
mode: image suffix, starts with either Positive or Negative and ends with a number from 1-4
placeholder: if true, uses xxxxxxxx as the suffix instead, else uses mode

-- Process --
Use requests

-- Outputs --
Response messages"""
    message = ""
    os.chdir(f'{os.path.dirname(os.path.realpath(__file__))}') 
    os.chdir('..\images')
    try:
        if not os.path.exists(f'{folder_name}'):
            # If it doesn't exist, create the directory
            os.makedirs(f'{folder_name}')
            message += ", Directory created"
        
        
        try:
            response = get(URL)
        except exceptions.MissingSchema:
            message += ", **Missing protocol**"
        except exceptions.ConnectionError:
            message += ", **Unable to connect** check if host is up?"
        else:
            if response.status_code == 200:
                URL = basename(URL)
                query_start = URL.find('?')
                file_name = URL[:query_start] if query_start != -1 else URL # Get rid of parameters
                path = f'{folder_name}/{file_name}'
                for filename in os.listdir(folder_name):
                    if filename.startswith(file_name):
                        message += f", Image {file_name} already exists"
                        return message[2:]
                with open(f'{path}_{"x" * 8 if placeholder else mode[:-1]}.jpg', 'wb') as file: # Mode Posneg(1-4)
                    file.write(response.content)
                message += ", Saved successfully"
            else:
                message += ", **Request failed**"

        return message[2:]
    except Exception as e:
        return f"**Unknown error**: {e}"

if __name__ == "__main__":
    SAMPLE_URL = "https://www.bing.com/images/create/colored-drawing-of-an-energetic-anime-girl-with-ca/1-65ca091f4af1405da5b2994f2b34733f?FORM=GENCRE"
    # print(catRescue(SAMPLE_URL))
    print(catDownloader("https://th.bing.com/th/id/OIG2.PgMogaZtNgh6wGg4Tz1e", "testfrommain", "positive1"))
