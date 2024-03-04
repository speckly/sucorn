# sucorn_bot

A project to automate the creation of AI generated images using Dall-E 3 hosted on Bing Image Creator. 
The goals of this project include
- automatic collection of images through the [BingImageCreator reverse-engineered API](https://github.com/acheong08/BingImageCreator/tree/main)
- displaying these results on Discord for remote labelling
- **WIP** using Discord for persistent remote access of images by uploading blob instead of src which expires
- downloading from Discord remote to local storage
- **transitioning** images are organised by subfolders of different labels instead of renaming the filename, this is also for easier training of Keras classifier
- **consider** use db 
- use [pandas](https://pypi.org/project/pandas/) and [matplotlib](https://pypi.org/project/matplotlib/) for displaying statistics
- **WIP** training of Keras classifier
and labelling these images from both remote (Discord) and local (tkinter)

# Usage
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

### utilities/reverse_api/get_cookie.py

### utilities/reverse_api/run.py
