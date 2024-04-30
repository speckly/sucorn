"""Author: @speckly on Discord
https://github.com/speckly

NOTE: working directory will be changed to /images
BUG: Rate limits when using statistics"""

import os
import sys
import datetime
import threading 
import time

from requests import get
from json import loads
from random import choice

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
del libs

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{DIRECTORY}/features')
from aclient import MyClient, PosNegView
from catrescue import catRescue
from sucorn_statistics import count_files
import discord

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

def timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def silly_message(interaction, title="", message="", emb_color=0xff0000, channel='', author=True, footer='speckles'):
    with open(f"{DIRECTORY}/features/the_funnies.txt") as f:
        the_funnies = [gif.rstrip('\n') for gif in f]
        
    emb=discord.Embed(title=title, description=message,
            color=emb_color, timestamp=datetime.datetime.now())
    if author:
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
    emb.set_footer(text=footer)
    emb.set_image(url=choice(the_funnies))
    if channel == "":
        await interaction.response.send_message(embed=emb)
    else:
        try:
            await channel.send(embed=emb)
        except:
            await silly_message(interaction, title="Error in parsing channel") # Will be termination case

@client.event
async def on_ready():
    print(f'{timestamp()}: Logged in as {client.user} (ID: {client.user.id})')

@client.tree.command(description='Embed message with a silly gif')
@discord.app_commands.describe(message='Message', title='Title')
async def silly_embed(interaction, message, title="Message"):
    emb_color = 0x00ff00 # TODO: Make this flexible, discord does not support hex
    try:
        catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
    except Exception as e:
        catFact = f"Meowerror: {e}"
    await silly_message(interaction, title, message, emb_color, footer=catFact)

@client.tree.command(name='sync', description='Owner only, command tree sync only when needed')
async def sync(interaction):
    if interaction.user.id == 494483880410349595:
        await client.tree.sync()
        await interaction.response.send_message('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')
    
@client.tree.command(description='Bing Image Generator URL to Discord Embed in full resolution')
@discord.app_commands.describe(link='Bing Image Generator URL')
async def embed_cat(interaction, link): #Optional[]
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
        await interaction.response.send_message(embeds=embed_list, view=PosNegView(len(results)))
    except Exception as error:
        emb=discord.Embed(title="Error:", description=f"Error logged: {error}", color=0xff0000, timestamp=datetime.datetime.now())
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
        emb.set_footer(text=catFact)
        await interaction.response.send_message(embed=emb)

@client.tree.command(description='Owner only, generate statistics on the category')
@discord.app_commands.describe()
async def statistics(interaction, target=''):
    if target == '':
        target = interaction.channel_id
    if (type(target) != int and not target.isnumeric()):
        await silly_message(interaction, title="Channel is not an integer.")
        return

    DUMP_CHANNEL = client.get_channel(int(target))
    if DUMP_CHANNEL == None:
        await silly_message(interaction, title="Channel is not a valid channel")
        return

    if interaction.user.id != 494483880410349595:
        await silly_message(interaction, title="Not authorized to use this command")
        return
    else:
        # Remove previous statistics
        async for message in DUMP_CHANNEL.history(limit=None):
            if message.author.bot:
                await message.delete()

        final_string = ""
        ordered_dir = sorted(os.listdir(f"{DIRECTORY}/images"), key=lambda x: int(x.split('-')[-1]) if x.split('-')[-1].isdigit() else float('inf'))
        for directory in ordered_dir:
            final_string = count_files(f'{DIRECTORY}/images/{directory}')
            try:
                catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
            except Exception as e:
                catFact = f"Meowerror: {e}"
            await silly_message(interaction, title=directory, 
                                message=final_string, emb_color=0x00ff00, 
                                channel=DUMP_CHANNEL, footer=catFact, author=False)

        try:
            
            for stat in os.listdir(f"{DIRECTORY}/statistics"):
                try:
                    catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
                except Exception as e:
                    catFact = f"Meowerror: {e}"
                file = discord.File(os.path.join(f"{DIRECTORY}/statistics", stat), filename="output.png")
                emb=discord.Embed(title=f"{stat.replace('.png', '')}", url="https://http.cat/status/200", 
                color=0x00ff00, timestamp=datetime.datetime.now())
                emb.set_footer(text=catFact)
                emb.set_image(url=f"attachment://output.png")

                await DUMP_CHANNEL.send(embed=emb, file=file)
        except:
            try:
                catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
            except Exception as e:
                catFact = f"Meowerror: {e}"
            emb=discord.Embed(title=f"Error", url="https://http.cat/status/500", 
            description="cat", color=0x00ff00, timestamp=datetime.datetime.now())
            emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            emb.set_footer(text=catFact)
            emb.set_image(url=f"attachment://output.png")
            
            await DUMP_CHANNEL.send(embed=emb, file=file)

@client.tree.command(description='Owner only, to nuke a channel with embedded images from the server')
@discord.app_commands.describe(target='Target Channel', folder_name='Folder name that the images reside in')
async def nuclear_cat_new(interaction, folder_name: str, mode: str, target=''):
    # Validation is done in ascending runtime complexity order
    mode = mode.strip().lower()
    if mode not in ['positive', 'negative', 'neutral', 'unlabelled']:
        await silly_message(interaction, title="Invalid mode", message='Accepted modes are positive, negative, neutral, unlabelled')
        return
    if target == '':
        target = interaction.channel_id
    elif type(target) != int and not target.isnumeric():
        await silly_message(interaction, title="Channel is not an integer.")
        return
    
    WDIR = f'{DIRECTORY}/images/{folder_name}/{mode if mode != "unlabelled" else ""}'
    if not os.path.exists(WDIR):
        await silly_message(interaction, title=f"{WDIR.replace(DIRECTORY, '')} does not exist")
        return
    
    DUMP_CHANNEL = client.get_channel(int(target))
    if DUMP_CHANNEL == None:
        await silly_message(interaction, title="Channel is not a valid channel")
        return

    if interaction.user.id != 494483880410349595:
        await silly_message(interaction, title="Not authorized to use this command")
        return
    else:
        await silly_message(interaction, title="Sending millions of cats to this channel now (v2)", emb_color=0x00ff00)
        number = 0
        match mode:
            case 'positive':
                COLOR = 0x00ff00
            case 'negative':
                COLOR = 0xff0000
            case 'neutral':
                COLOR = 0x0000ff
            case 'unlabelled':
                COLOR = 0x808080
        start_time = time.time()
        files = [file for file in os.listdir(WDIR) if file.endswith(".jpg") or file.endswith(".jpeg")]
        if files == []:
            await silly_message(interaction, title=f"Provided folder {WDIR.replace(DIRECTORY, '')} is empty", emb_color=0x808080, channel=DUMP_CHANNEL)
            return
        for filename in files:
            try:
                number += 1
                try:
                    catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
                except Exception as e:
                    catFact = f"Meowerror: {e}"

                # What kind of black magic is involved here with local files?
                file = discord.File(os.path.join(WDIR, filename), filename="output.png")
                emb=discord.Embed(title=f"#{number}", url="https://http.cat/status/200", 
                description="cat", color=COLOR, timestamp=datetime.datetime.now())
                emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
                emb.set_footer(text=catFact)
                emb.set_image(url=f"attachment://output.png")
                
                await DUMP_CHANNEL.send(embed=emb, file=file)
            except Exception as error:
                emb=discord.Embed(title="Error", description=f"Error logged: {error}", color=0xff0000, 
                                  timestamp=datetime.datetime.now(), url="https://http.cat/status/500")
                emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
                emb.set_footer(text=catFact)
                await DUMP_CHANNEL.send(embed=emb)
        
        runtime_seconds = time.time() - start_time
        hours = runtime_seconds // 3600
        minutes = (runtime_seconds % 3600) // 60
        remaining_seconds = runtime_seconds % 60

        emb=discord.Embed(title="Nuking complete", 
        description=f"Sent {number} images\nRuntime: {hours:.0f} hours, {minutes:.0f} minutes, {remaining_seconds:.2f} seconds",
            color=0x00FF00, timestamp=datetime.datetime.now())
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
        emb.set_footer(text="speckles")
        emb.set_image(url="https://media.tenor.com/M0YNmGgIQF4AAAAd/guh-cat.gif")
        await interaction.followup.send(embed=emb)
        
# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction, member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

# @client.event
# async def on_message(message):
#     if message.author.bot: 
#         return

@client.event
async def on_interaction(interaction):
    print(f'{timestamp()}: {interaction.user.name} ({interaction.user.id}) used {interaction.command.qualified_name} with failed={interaction.command_failed}')

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