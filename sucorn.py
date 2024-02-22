"""Author: @speckly on Discord
https://github.com/speckly

NOTE: working directory will be changed to /images"""

import os
import sys
import datetime
import threading 
import time

# cat fact API
from requests import get
from json import loads

# Requires pip install
import importlib
libs = {"discord": None, "dotenv": None, "playsound": None, "psutil": None}
for lib in libs:
    try: 
        libs[lib] = importlib.import_module(lib)
    except ModuleNotFoundError:
        if input(f"{lib} is required to run this program, execute pip install {lib}? (Y): ").lower().strip() in ["", "y"]:
            installation = lib if lib != "dotenv" else "python-dotenv" # Pip install python-dotenv and import as dotenv
            os.system(f"pip install {installation}")
            libs[lib] = importlib.import_module(lib)
        else:
            exit()

discord, dotenv, playsound, psutil = libs["discord"], libs["dotenv"], libs["playsound"], libs["psutil"]
del libs # Not required anymore

# Features
sys.path.append('./features')
from aclient import MyClient, PosNegView
from cscraper import CScraper
from catrescue import catRescue, catDownloader

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

def timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command(description='Calls the person gay')
@discord.app_commands.rename(text_to_send='name')
@discord.app_commands.describe(text_to_send='Your name')
async def gay(interaction: discord.Interaction, text_to_send: str):
    await interaction.response.send_message(f'{text_to_send} is gay lmao!!!')

@client.tree.command(name='sync', description='Owner only, command tree sync only when needed')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 494483880410349595:
        await client.tree.sync()
        await interaction.response.send_message('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')
    
@client.tree.command(description='Bing Image Generator URL to Discord Embed in full resolution')
@discord.app_commands.describe(link='Bing Image Generator URL')
async def embed_cat(interaction: discord.Interaction, link: str): #Optional[]
    embed_list = []
    try:
        results, prompt = catRescue(link)
        try:
            catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
        except Exception as e:
            catFact = f"Meowerror: {e}"
        for src in results:
            emb=discord.Embed(title=f"Nyan #", url=link, 
            description=prompt, color=0x00ff00, timestamp=datetime.datetime.now())
            emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            emb.set_footer(text=catFact)
            emb.set_image(url=src)
            embed_list.append(emb)
        # view = PosNegView(len(results))
        # print(view.is_persistent())
        await interaction.response.send_message(embeds=embed_list, view=PosNegView(len(results)))
    except Exception as error:
        emb=discord.Embed(title="Error:", description=f"Error logged: {error}", color=0xff0000, timestamp=datetime.datetime.now())
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
        emb.set_footer(text=catFact)
        await interaction.response.send_message(embed=emb)

async def silly_message(interaction: discord.Interaction, msg: str, emb_color: hex = 0xff0000) -> None:
    emb=discord.Embed(title=msg, 
            color=emb_color, timestamp=datetime.datetime.now())
    emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
    emb.set_footer(text="speckles")
    emb.set_image(url="https://media.tenor.com/M0YNmGgIQF4AAAAd/guh-cat.gif")
    await interaction.response.send_message(embed=emb)

@client.tree.command(description='Owner only, to nuke a channel with a list of links fed into /embed_cat')
@discord.app_commands.describe(copy='Copy channel', target='Target Channel', ex_prompt='Validate prompt (recommended after 19 Dec 2023, prompts get trunc)')
async def nuclear_cat(interaction: discord.Interaction, copy: str, target:str='', ex_prompt:str=''): 
    if target == '':
        target = interaction.channel_id
    if not copy.isnumeric() or (type(target) != int and not target.isnumeric()):
        await silly_message(interaction, "Channel is not an integer.")
        return

    COPY_CHANNEL = client.get_channel(int(copy))
    DUMP_CHANNEL = client.get_channel(int(target))
    if COPY_CHANNEL == None or DUMP_CHANNEL == None:
        await silly_message(interaction, "Channel is not a valid channel")
        return

    if interaction.user.id != 494483880410349595:
        await silly_message(interaction, "Not authorized to use this command")
        return
    else:
        await silly_message(interaction, "Sending millions of cats to this channel now", 0x00ff00)

        # This is the end of your channel
        history = COPY_CHANNEL.history(limit=None) # Verified to have no loss for a channel with 48 results
        number = 0
        async for message in history: #TODO: use a stack?
            link = message.content
            embed_list = []
            if len(link) < 240:
                try:
                    results, prompt = catRescue(link)
                    if results == []:
                        print(f'{timestamp()}: Empty result list')
                        playsound.playsound(f'{DIRECTORY}\\tests\\vine-boom.wav')
                        continue
                    elif prompt == '':
                        print(f'{timestamp()}: Empty prompt/couldnt get prompt')
                        playsound.playsound(f'{DIRECTORY}\\tests\\vine-boom.wav')
                        continue
                    elif ex_prompt != '' and prompt != ex_prompt: # Empty string means no validation needed
                        print(f'{timestamp()}: Prompt does not match channel')
                        playsound.playsound(f'{DIRECTORY}\\tests\\vine-boom.wav')
                        continue
                    try:
                        catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
                    except Exception as e:
                        catFact = f"Meowerror: {e}"
                    number += 1
                    for src in results:
                        emb=discord.Embed(title=f"#{number}", url=link, 
                        description="cat", color=0x00ff00, timestamp=datetime.datetime.now())
                        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
                        emb.set_footer(text=catFact)
                        emb.set_image(url=src)
                        embed_list.append(emb)
                    await DUMP_CHANNEL.send(embeds=embed_list, view=PosNegView(len(results)))
                except Exception as error:
                    emb=discord.Embed(title="Error", description=f"Error logged: {error}\n[link]({link}", color=0xff0000, timestamp=datetime.datetime.now())
                    emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
                    emb.set_footer(text=catFact)
                    await DUMP_CHANNEL.send(embed=emb)
            else:
                emb=discord.Embed(title="Error", description=f"[Link]({link}) over 240 characters", color=0xff0000, timestamp=datetime.datetime.now())
                emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
                emb.set_footer(text=catFact)
                await DUMP_CHANNEL.send(embed=emb)

@client.tree.command(description='Owner only, to download all current unlabelled images')
@discord.app_commands.describe(target='Target Channel', placeholder='Use placeholders in last 8 characters of file name')
async def download_all(interaction: discord.Interaction, target:str='', placeholder:bool=False): 
    if target == '':
        target = interaction.channel_id
    if interaction.user.id != 494483880410349595:
        await silly_message(interaction, "Not authorized to use this command")
        return
    else:
        # TODO: add response here
        await silly_message(interaction, "Downloading millions of cats from this channel now", 0x00ff00)
        target = client.get_channel(int(target))
        channel_name = target.name
        history = target.history(limit=None) # Verified to have no loss for a channel with 48 results
        start_time = time.time()
        message_count = 0
        image_count = 0

        async for message in history:
            message_count += 1
            view = discord.ui.View.from_message(message)
            pos_labels = {}
            labels = {}
            for button in view.children:
                if button.label[:-1] == "Negative" and not button.disabled:
                    labels[button.label] = button
                elif button.label[:-1] == "Positive":
                    pos_labels[button.label] = button
            print(message_count)
            
            # NOTE: I have commented out editing the view as it adds too many requests and its not too important
            for label in labels: # for all Negative buttons that are not disabled
                # labels[label].disabled = True # Disable current button
                image_number = int(label[-1])
                # view.remove_item(pos_labels["Positive" + label[-1]])
                image_index = image_number - 1 # Labels are 1-4 attached to the end of the string
                try:
                    emb = message.embeds[image_index]
                    res = f"Image {image_index+1}: {catDownloader(emb.image.url, channel_name, label, placeholder)}\n"
                    image_count += 1
                except IndexError:
                    res = f"Image {image_index+1}: Index out of range"
                # await message.edit(view=view)
                print(res)

        
        runtime_seconds = time.time() - start_time
        hours = runtime_seconds // 3600
        minutes = (runtime_seconds % 3600) // 60
        remaining_seconds = runtime_seconds % 60

        emb=discord.Embed(title="Download complete", 
        description=f"Downloaded {image_count} images from {message_count} messages\nRuntime: {hours:.0f} hours, {minutes:.0f} minutes, {remaining_seconds:.2f} seconds",
            color=0x00FF00, timestamp=datetime.datetime.now())
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
        emb.set_footer(text="speckles")
        emb.set_image(url="https://media.tenor.com/M0YNmGgIQF4AAAAd/guh-cat.gif")
        await interaction.followup.send(embed=emb) 
        
# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.
# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

# @client.event
# async def on_message(message):
#     if message.author.bot: 
#         return
    

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024  # in kilobytes

def monitor_performance(interval=300):
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = get_memory_usage()
        print(f'{timestamp()}: CPU Usage {cpu_usage}%, Memory Usage {memory_usage} KB')
        time.sleep(interval)

if __name__ == "__main__":
    performance_thread = threading.Thread(target=monitor_performance, args=(1000,))
    performance_thread.start()
    client.run(os.getenv('TOKEN'))