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

[.exe? What is that?](https://github.com/sherlock-project/sherlock/issues/2011)
```bash
pip install -r requirements.txt
```
**WIP automating these** Required files and folders:
```.env``` with ```TOKEN=<your discord token here>```
```/images```
```/utilities/reverse_api/.env``` with ```PASSWORD=<your password here>```
```/utilities/reverse_api/usernames.json```
```/utilities/reverse_api/prompt.txt```
```/utilities/reverse_api/cookies.json```
```/utilities/reverse_api/test_cookies.json```

### features/sucorn_statistics.py
This is both a feature and utility, feature used for the ```/statistics``` slash command in Discord, utility can be used in the command line. Default option will iterate through all subfolders in ```./images```
```sucorn_statistics```

### utilities/reverse_api/get_cookie.py

### utilities/reverse_api/run.py
