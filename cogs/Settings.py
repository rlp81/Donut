import discord
from discord import option
import json

class settings(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    @discord.slash_command(name="settings",description="Change server settings") # we can also add application commands
    @option("over18", description="Allows 18+ reddit memes")
    @option("inflation", description="Turns on inflation in the economy")
    async def settings(self, ctx, over18: bool = None, inflation: bool = None):
        if inflation != None:
            with open("guilds.json", "r") as f:
                guilds = json.load(f)
            if str(ctx.guild.id) in guilds:
                guilds[str(ctx.guild.id)]["inflation"] = f"{inflation}"
            else:
                guilds[str(ctx.guild.id)] = {}
                guilds[str(ctx.guild.id)]["inflation"] = f"{inflation}"
            with open("guilds.json", "w") as f:
                json.dump(guilds, f, indent=4)
            await ctx.respond(f"Changed setting inflation to {inflation}")
        if over18 != None:
            with open("guilds.json", "r") as f:
                guilds = json.load(f)
            if str(ctx.guild.id) in guilds:
                guilds[str(ctx.guild.id)]["over18"] = f"{over18}"
            else:
                guilds[str(ctx.guild.id)] = {}
                guilds[str(ctx.guild.id)]["over18"] = f"{over18}"
            with open("guilds.json", "w") as f:
                json.dump(guilds, f, indent=4)
            await ctx.respond(f"Changed setting over18 to {over18}")
        else:
            pass

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(settings(bot)) # add the cog to the bot