@client.tree.command(description='Owner only, to download all current unlabelled images, DEPRECATED')
@discord.app_commands.describe(target='Target Channel', placeholder='Use placeholders in last 8 characters of file name')
async def download_all(interaction: discord.Interaction, target:str='', placeholder:bool=True): 
    if target == '':
        target = interaction.channel_id
    if interaction.user.id != 494483880410349595:
        await silly_message(interaction, title="Not authorized to use this command")
        return
    else:
        await silly_message(interaction, title="Downloading millions of cats from this channel now", emb_color=0x00ff00)
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
                image_number = int(label[-1])
                image_index = image_number - 1 # Labels are 1-4 attached to the end of the string
                try:
                    emb = message.embeds[image_index]
                    res = f"Image {image_index+1}: {catDownloader(emb.image.url, channel_name, label, placeholder)}\n"
                    image_count += 1
                except IndexError:
                    res = f"Image {image_index+1}: Index out of range"
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


@client.tree.command(description='DEPRECATED, owner only, reads the whole copy channel')
@discord.app_commands.describe(copy='Copy channel', target='Target Channel', ex_prompt='Validate prompt (recommended after 19 Dec 2023, prompts get trunc)')
async def nuclear_cat_legacy(interaction: discord.Interaction, copy: str, target:str='', ex_prompt:str=''): 
    if target == '':
        target = interaction.channel_id
    if not copy.isnumeric() or (type(target) != int and not target.isnumeric()):
        await silly_message(interaction, title="Channel is not an integer.")
        return

    COPY_CHANNEL = client.get_channel(int(copy))
    DUMP_CHANNEL = client.get_channel(int(target))
    if COPY_CHANNEL == None or DUMP_CHANNEL == None:
        await silly_message(interaction, title="Channel is not a valid channel")
        return

    if interaction.user.id != 494483880410349595:
        await silly_message(interaction, title="Not authorized to use this command")
        return
    else:
        await silly_message(interaction, title="Sending millions of cats to this channel now", emb_color=0x00ff00)

        # This is the end of your channel
        history = COPY_CHANNEL.history(limit=None) # Verified to have no loss for a channel with 48 results
        number = 0
        async for message in history: # TODO: use a stack?
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
                    emb=discord.Embed(title="Error", description=f"Error: {error}\n[link]({link}", color=0xff0000, timestamp=datetime.datetime.now())
                    emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
                    emb.set_footer(text=catFact)
                    await DUMP_CHANNEL.send(embed=emb)
            else:
                emb=discord.Embed(title="Error", description=f"[Link]({link}) over 240 characters", color=0xff0000, timestamp=datetime.datetime.now())
                emb.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
                emb.set_footer(text=catFact)
                await DUMP_CHANNEL.send(embed=emb)