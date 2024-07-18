# sucorn
pronounced as [su-kon](https://fubuki.moe/mascots.html)

A project to automate the creation of AI generated images using Dall-E 3 hosted on Bing Image Creator, and to classify which ones are good and which ones are bad, so that time spent during the ML/DL life cycle is reduced
The goals of this project include
- **deprecated** automatic collection of images using `pyautogui`,
- automatic collection of images through the [BingImageCreator reverse-engineered API](https://github.com/acheong08/BingImageCreator/tree/main)
- **WIP** automatic collection of images through [stable diffusion's](https://github.com/CompVis/stable-diffusion) text2img, hopefully with automatic parameter tuning
- Automatic collection of Microsoft Session cookies using `WebDriver`
- Displaying these images on Discord for remote labelling
- Labelling these images from both remote (Discord) and local (tkinter) for training
- Using Discord for easy, persistent remote access of images
- use [pandas](https://pypi.org/project/pandas/) and [matplotlib](https://pypi.org/project/matplotlib/) for displaying statistics locally and on Discord
- **WIP** training of Keras classifier
- **WIP** training of Stable Diffusion LoRA (LoRA not included in this repo)

# Setup
> [!WARNING]
> There is no .exe file because I am a [stupid smelly nerd](https://github.com/sherlock-project/sherlock/issues/2011)

It is recommended that a venv is used as there are a lot of dependencies (50>)
```bash
python setup.py
```

# Bot
Requires your bot token in `.env`, follow the setup guide
```bash
python sucorn.py
```

# Data collection phase
> [!WARNING]
> Use this ethically, as this makes requests to BingImageCreator. Avoid using too many instances as it will result in executing a DoS attack on this host.

### utilities/reverse_api/get_cookie.py

Load account names in the `normal` list in `usernames.json` and run this file. This will automatically get the session cookie for each account and store it into `cookies.json`. Credentials are taken from `.env`. The `loaded` list contains account names with the cookie acquired and stored

### utilities/reverse_api/run.py || run_linux.py
> [!INFO]
> Replaces all double quotation marks in prompt with single quotation marks in Linux, keyboard ctrl shift r does not work either

Creates n-number of instances that will use the reverse engineered API to generate images from `imagedir/prompt.txt`. n-number of instances depends on how many pairs are found in `cookies.json`
If `imagedir` does not exist then `utilities/reverse_api/prompt.txt` will be used to create `imagedir/prompt.txt`
```bash
python run.py imagedir --delay 10 --max 20
```
Each instance here will have a cooldown of 10 seconds after downloading all images from the query before 

Keys:
- Tab: Brings the child processes to front
- End: Terminates all child processes
- Ctrl + Shift + R: Reloads prompt from `utilities/reverse_api/new_prompt.txt`. Currently unavailable

###### If it doesn't work
Try changing the parameters located in `BingImageCreator.py` TODO: instructions here

### utilities/reverse_api/.env

WIP
```
GENERAL=your_password_here
speckly=your_password_here
```

### utilities/automation.py
> [!WARNING]
> This feature is deprecated, use utilities/reverse_api

Makes use of `pyautogui` to automatically navigate the GUI, using mouse clicks and keyboard presses. The output is links pasted in a Discord channel. Run the Discord slash command `/nuclear_cat copy=<copy channel>`

# Data preparation phase
### features/sucorn_statistics.py
This is both a feature and utility, feature used for the `/statistics` slash command in Discord, utility can be used in the command line. 

```bash
python sucorn_statistics.py
```
Providing no options will iterate through all subfolders in `./images`
```bash
python sucorn_statistics.py --csv sample_statistics.csv --mode write
```
Writes these results out to a given csv file, ommitting the `--mode` flag will read the csv and display it using [matplotlib](https://pypi.org/project/matplotlib/)

### utilities/labelling.py
For supervised learning, we need to label the images
> [!WARNING]
> Do not run this with reverse_api/run.py, as there will be duplicate file names and overwriting will occur, will fix this later

```bash
labelling.py foldername
```
Ensure that `foldername` is a valid foldername in ./images
The following keys will label the image by moving it into its subfolder
- 0 for negative
- 1 for positive
- 2 for neutral
- ESC to quit

# remove later

`py BingImageCreator.py --cookie-file test_cookie.txt --debug-file debug.log --prompt "an astronaut on the moon"`