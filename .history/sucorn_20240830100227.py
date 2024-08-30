"""Author: @speckly on Discord
https://github.com/speckly

NOTE: working directory will be changed to /images
BUG: Rate limits when using statistics"""

import os
import sys
import datetime
import time

from json import loads
from random import choice
from requests import get
import discord
import dotenv

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{DIRECTORY}/features')
from aclient import MyClient, PosNegView
from catrescue import catRescue
from sucorn_statistics import count_files

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

def timestamp() -> str:
    """
    Author: Andrew Higgins
    https://github.com/speckly
    
    Returns the current timestamp"""

    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def silly_message(interaction: discord.Interaction, title: str="", message: str=""
                        ,emb_color: hex = 0xff0000, channel: discord.channel = '',
                        author: bool=True, footer: str='speckles') -> None:
    """
    Author: Andrew Higgins
    https://github.com/speckly
    
    silly_message automatically sends a silly message 
    in response to a Discord Interaction object/channel object.
    
    Usual arguments to a Discord Embed are expected in this function"""
    with open(f"{DIRECTORY}/features/the_funnies.txt", encoding="utf-8") as f:
        the_funnies = [gif.rstrip('\n') for gif in f]

    emb=discord.Embed(title=title, description=message,
            color=emb_color, timestamp=datetime.datetime.now())
    if author:
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
    emb.set_footer(text=footer)
    emb.set_image(url=choice(the_funnies))
    if channel == "":
        await interaction.response.send_message(embed=emb)
    else:
        try:
            await channel.send(embed=emb)
        except Exception:
            await silly_message(interaction, title="Error in parsing channel") # Termination case

@client.event
async def on_ready():
    print(f'{timestamp()}: Logged in as {client.user} (ID: {client.user.id})')

@client.tree.command(description='Embed message with a silly gif')
@discord.app_commands.describe(message='Message', title='Title')
async def silly_embed(interaction: discord.Interaction, message: str, title: str = "Message"):
    emb_color: hex = 0x00ff00 # TODO: Make this flexible, discord does not support hex
    try:
        cat_fact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
    except Exception as e:
        cat_fact = f"Meowerror: {e}"
    await silly_message(interaction, title, message, emb_color, footer=cat_fact)

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
            cat_fact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
        except Exception as e:
            cat_fact = f"Meowerror: {e}"
        for src in results:
            emb=discord.Embed(title="Nyan", url=link,
                description=prompt, color=0x00ff00, timestamp=datetime.datetime.now())
            emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            emb.set_footer(text=cat_fact)
            emb.set_image(url=src)
            embed_list.append(emb)
        await interaction.response.send_message(embeds=embed_list, view=PosNegView(len(results)))
    except Exception as error:
        emb=discord.Embed(title="Error:", description=f"Error logged: {error}", color=0xff0000, timestamp=datetime.datetime.now())
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
        emb.set_footer(text=cat_fact)
        await interaction.response.send_message(embed=emb)

@client.tree.command(description='Owner only, generate statistics on the category')
@discord.app_commands.describe()
async def statistics(interaction: discord.Interaction, target:str=''):
    if not target:
        target: int = interaction.channel_id
    elif not target.isnumeric():
        await silly_message(interaction, title="Channel is not an integer.")
        return

    dump_channel = client.get_channel(int(target))
    if dump_channel is None:
        await silly_message(interaction, title="Channel is not a valid channel")
        return

    if interaction.user.id != 494483880410349595:
        await silly_message(interaction, title="Not authorized to use this command")
        return
    else:
        # Remove previous statistics
        async for message in dump_channel.history(limit=None):
            if message.author.bot:
                await message.delete()

        final_string = ""
        ordered_dir = sorted(os.listdir(f"{DIRECTORY}/images"),
            key=lambda x: int(x.split('-')[-1]) if x.split('-')[-1].isdigit() else float('inf'))
        for directory in ordered_dir:
            final_string = count_files(f'{DIRECTORY}/images/{directory}')
            try:
                cat_fact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
            except Exception as e:
                cat_fact = f"Meowerror: {e}"
            await silly_message(interaction, title=directory, 
                                message=final_string, emb_color=0x00ff00, 
                                channel=dump_channel, footer=cat_fact, author=False)

        try:
            for stat in os.listdir(f"{DIRECTORY}/statistics"):
                try:
                    cat_fact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
                except Exception as e:
                    cat_fact = f"Meowerror: {e}"
                file = discord.File(os.path.join(f"{DIRECTORY}/statistics", stat), filename="output.png")
                emb=discord.Embed(title=f"{stat.replace('.png', '')}", url="https://http.cat/status/200",
                color=0x00ff00, timestamp=datetime.datetime.now())
                emb.set_footer(text=cat_fact)
                emb.set_image(url="attachment://output.png")

                await dump_channel.send(embed=emb, file=file)
        except Exception:
            try:
                cat_fact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
            except Exception as e:
                cat_fact = f"Meowerror: {e}"
            emb=discord.Embed(title="Error", url="https://http.cat/status/500", 
            description="cat", color=0x00ff00, timestamp=datetime.datetime.now())
            emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            emb.set_footer(text=cat_fact)
            emb.set_image(url="attachment://output.png")

            await dump_channel.send(embed=emb, file=file)

@client.tree.command(description='Owner only, to nuke a channel with embedded images from the server')
@discord.app_commands.describe(target='Target Channel', folder_name='Folder name images are in')
async def nuclear_cat_new(interaction: discord.Interaction, folder_name: str, mode: str, target:str=''):
    """
    Author: Andrew Higgins
    https://github.com/speckly
    
    Validation is done in ascending runtime complexity order"""
    mode = mode.strip().lower()
    if mode not in ['positive', 'negative', 'neutral', 'unlabelled']:
        await silly_message(interaction, title="Invalid mode",
            message='Accepted modes are positive, negative, neutral, unlabelled')
        return
    if not target:
        target = interaction.channel_id
    elif not isinstance(target, int) and not target.isnumeric():
        await silly_message(interaction, title="Channel is not an integer.")
        return

    wdir = f'{DIRECTORY}/images/{folder_name}/{mode if mode != "unlabelled" else ""}'
    if not os.path.exists(wdir):
        await silly_message(interaction, title=f"{wdir.replace(DIRECTORY, '')} does not exist")
        return

    dump_channel = client.get_channel(int(target))
    if dump_channel is None:
        await silly_message(interaction, title="Channel is not a valid channel")
        return

    
        await silly_message(interaction, title="Not authorized to use this command")
        return
    else:
        await silly_message(interaction,
            title="Sending millions of cats to this channel now (v2)", emb_color=0x00ff00)
        number = 0
        match mode:
            case 'positive':
                color = 0x00ff00
            case 'negative':
                color = 0xff0000
            case 'neutral':
                color = 0x0000ff
            case 'unlabelled':
                color = 0x808080
        start_time = time.time()
        files = [file for file in os.listdir(wdir) if file.endswith(".jpg") or file.endswith(".jpeg")]
        if not files:
            await silly_message(interaction, title=f"Provided folder {wdir.replace(DIRECTORY, '')} is empty",
                emb_color=0x808080, channel=dump_channel)
            return
        for filename in files:
            try:
                number += 1
                try:
                    cat_fact = loads(get("https://catfact.ninja/fact").content.decode("utf-8"))["fact"]
                except Exception as e:
                    cat_fact = f"Meowerror: {e}"

                # What kind of black magic is involved here with local files?
                file = discord.File(os.path.join(wdir, filename), filename="output.png")
                emb=discord.Embed(title=f"#{number}", url="https://http.cat/status/200",
                description="cat", color=color, timestamp=datetime.datetime.now())
                emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
                emb.set_footer(text=cat_fact)
                emb.set_image(url="attachment://output.png")

                await dump_channel.send(embed=emb, file=file)
            except Exception as error:
                emb=discord.Embed(title="Error", description=f"Error logged: {error}",
                    color=0xff0000, timestamp=datetime.datetime.now(),
                    url="https://http.cat/status/500")
                emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
                emb.set_footer(text=cat_fact)
                await dump_channel.send(embed=emb)

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
# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

@client.event
async def on_interaction(interaction):
    print(f'{timestamp()}: {interaction.user.name} ({interaction.user.id}) used {interaction.command.qualified_name} with failed={interaction.command_failed}')

if __name__ == "__main__":
    client.run(os.getenv('TOKEN'))