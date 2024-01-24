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
from catrescue import catRescue
from ploterror import plotError, plot_process, plot_thread

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

instanceURLs = [None, None, None, None, None, None] #Contains the last unique URL of 6 instances
currentInstance = -1

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
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')
    
@client.tree.command(description='Bing Image Generator URL to Discord Embed in full resolution')
@discord.app_commands.describe(link='Bing Image Generator URL')
async def embed_cat(interaction: discord.Interaction, link: str): #Optional[]
    embed_list = []
    try:
        results, _ = catRescue(link)
        try:
            catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
        except Exception as e:
            catFact = f"Meowerror: {e}"
        for src in results:
            emb=discord.Embed(title=f"Nyan #", url=link, 
            description="Cat", color=0x00ff00, timestamp=datetime.datetime.now())
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

async def silly_message(interaction: discord.Interaction, msg: str, emb_color: hex = 0xff0000) -> None:
    emb=discord.Embed(title=msg, 
            color=emb_color, timestamp=datetime.datetime.now())
    emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
    emb.set_footer(text="Baka")
    emb.set_image(url="https://media.tenor.com/M0YNmGgIQF4AAAAd/guh-cat.gif")
    await interaction.response.send_message(embed=emb)

@client.tree.command(description='Owner only, to nuke a channel with a list of links fed into /embed_cat')
@discord.app_commands.describe(copy='Copy channel', target='Target Channel', ex_prompt='Validate prompt (recommended after 19 Dec 2023, prompts get trunc)')
async def nuclear_cat(interaction: discord.Interaction, copy: str, target:str='', ex_prompt:str=''): 
    if target == '':
        #Default value
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
        async for message in history: #TODO: use a stack?
            link = message.content
            embed_list = []
            if len(link) < 240:
                try:
                    results, prompt = catRescue(link)
                    timestamp = datetime.datetime.now()
                    if results == []:
                        print(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}: Empty result list')
                        playsound.playsound('C:\\Users\Dell\OneDrive - Singapore Polytechnic\Documents\compooting\CScraper-SpeckOS\sucorn_bot\\tests\\vine-boom.wav')
                        continue
                    elif prompt == '':
                        print(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}: Empty prompt/couldnt get prompt')
                        playsound.playsound('C:\\Users\Dell\OneDrive - Singapore Polytechnic\Documents\compooting\CScraper-SpeckOS\sucorn_bot\\tests\\vine-boom.wav')
                        continue
                    elif ex_prompt != '' and prompt != ex_prompt: # Empty string means no validation needed
                        print(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}: Prompt does not match channel')
                        playsound.playsound('C:\\Users\Dell\OneDrive - Singapore Polytechnic\Documents\compooting\CScraper-SpeckOS\sucorn_bot\\tests\\vine-boom.wav')
                        continue
                    # btnView = buttonViewSave()
                    try:
                        catFact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
                    except Exception as e:
                        catFact = f"Meowerror: {e}"
                    for src in results:
                        emb=discord.Embed(title=f"cats", url=link, 
                        description="catto", color=0x00ff00, timestamp=datetime.datetime.now())
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


# @client.tree.command(description='Counts the number of negative reactions in a channel')
# @discord.app_commands.describe(product='What product are you looking for?')
# async def count_negatives(interaction: discord.Interaction, product: str = "RTX3080"): #Optional[]
#     pass
# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.
# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

@client.event
async def on_message(message):
    if message.author.bot: 
        return
    if message.author.id == 988090297131089922 or message.author.id == 494483880410349595: # TODO: rewrite condition to include input channels
        content = message.content
        global currentInstance
        currentInstance = (currentInstance + 1) % 6
        if len(content) > 200: # Filtered url/generating
            await message.delete() 
            playsound.playsound('C:\\Users\Dell\OneDrive - Singapore Polytechnic\Documents\compooting\CScraper-SpeckOS\sucorn_bot\\tests\\vine-boom.wav')
            plotError(None, True) # NOTE: either update the list or use plotError to update
        else:
            global instanceURLs
            try:
                instanceIDX = instanceURLs.index(content)
                # A duplicate is found. Meaning that this current instance has not generated a new URL
                # This also gives us 100% confidence which instance we are on. 
                currentInstance = instanceIDX
                await message.delete()
                playsound.playsound('C:\\Users\Dell\OneDrive - Singapore Polytechnic\Documents\compooting\CScraper-SpeckOS\sucorn_bot\\tests\metal-alert.wav') # Feedback that the delay (in automation) is not enough and to raise an alert
                timestamp = datetime.datetime.now()
                print(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}: Repeated')
            except ValueError:
                instanceURLs[currentInstance] = content

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024  # in kilobytes

def monitor_performance(interval=300):
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = get_memory_usage()
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: CPU Usage {cpu_usage}%, Memory Usage {memory_usage} KB')
        time.sleep(interval)

if __name__ == "__main__":
    performance_thread = threading.Thread(target=monitor_performance, args=(1000,))
    performance_thread.start()
    plot_thread()
    client.run(os.getenv('TOKEN'))