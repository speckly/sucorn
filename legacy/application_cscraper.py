import discord

results = [] # sorry i cant somehow pass it into buttonView
@client.tree.command(description='Scraper for predefined keys (WIP as classes change daily)')
@discord.app_commands.describe(product='What product are you looking for?')
async def scrape(ictLocal: discord.Interaction, product: str = "RTX3080"): #Optional[]
    global results
    try:
        results = CScraper(product) # title, url, desc
        btnView = buttonView()
        emb=discord.Embed(title=results[buttonView.pageno][0], url=results[buttonView.pageno][1], 
        description=results[buttonView.pageno][2], color=0x00ff00, timestamp=datetime.datetime.now())
    except Exception as error:
        btnView = None
        emb=discord.Embed(title=f"Error {error}", description="Error logged", color=0xff0000, timestamp=datetime.datetime.now())
    emb.set_author(name=ictLocal.user.name, icon_url=ictLocal.user.display_avatar) # type: ignore
    await ictLocal.response.send_message(embed=emb, view=btnView)

#Save buttons for saving images
class buttonViewSave(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Save", style=discord.ButtonStyle.success)
    async def save(self, interaction, button):
        channel = client.get_channel(1160193893367812096)
        await channel.send(embed=interaction.response.content)
        # interaction.response.embed