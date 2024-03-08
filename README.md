# sucorn_bot
A project to automate the creation of AI generated images using Dall-E 3 hosted on Bing Image Creator, and to classify which ones are good and which ones are bad, so that time spent during the ML/DL life cycle is reduced
The goals of this project include
- **deprecated** automatic collection of images using ```pyautogui```,
- automatic collection of images through the [BingImageCreator reverse-engineered API](https://github.com/acheong08/BingImageCreator/tree/main)
- automatic collection of session cookies using ```WebDriver```
- displaying these images on Discord for remote labelling
- **WIP** using Discord for persistent remote access of images by uploading blob instead of src which expires
- downloading from Discord remote to local storage
- images are organised by subfolders of different labels instead of renaming the filename, this is also for easier training of Keras classifier
- **considering** use db 
- labelling these images from both remote (Discord) and local (tkinter)
- use [pandas](https://pypi.org/project/pandas/) and [matplotlib](https://pypi.org/project/matplotlib/) for displaying statistics
- **WIP** training of Keras classifier

# Setup
> [!WARNING]
> There is no .exe file because I am a [stupid smelly nerd](https://github.com/sherlock-project/sherlock/issues/2011)
```bash
pip install -r requirements.txt
```
**WIP automating these** Required files and folders:
- ```.env``` with ```TOKEN=<your discord token here>```
- ```/images```
- ```/utilities/reverse_api/.env``` with ```PASSWORD=<your password here>```
- ```/utilities/reverse_api/prompt.txt```

# Data collection phase
> [!WARNING]
> Use this ethically, as this makes requests to BingImageCreator. Avoid using too many instances as it will result in executing a DoS attack on this host.

### utilities/reverse_api/get_cookie.py

### utilities/reverse_api/run.py
Creates n-number of instances that will use the reverse engineered API to generate images from ```prompt.txt```. n-number of instances depends on how many pairs are found in ```cookies.json```
```bash
python run.py --delay 10 --max 20
```
Each instance here will have a cooldown of 10 seconds after downloading all images from the query before 

### utilities/automation.py
> [!WARNING]
> This feature is deprecated, use 

# Data preparation phase
### features/sucorn_statistics.py
This is both a feature and utility, feature used for the ```/statistics``` slash command in Discord, utility can be used in the command line. 

```bash
python sucorn_statistics.py
```
Providing no options will iterate through all subfolders in ```./images```
```bash
python sucorn_statistics.py --csv sample_statistics.csv --mode write
```
Writes these results out to a given csv file, ommitting the ```--mode``` flag will read the csv and display it using [matplotlib](https://pypi.org/project/matplotlib/)