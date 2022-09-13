import discord
from discord.ext import commands
import json

class Channels(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    @discord.slash_command(name="setwelcomechannel",description="Sets your welcome channel.") # we can also add application commands
    async def _welchan(self, ctx, channel: discord.Option(discord.TextChannel)):
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if not str(ctx.guild.id) in chans:
            chans[ctx.guild.id] = {}
            chans[ctx.guild.id]["welcome"] = channel.id
            chans[ctx.guild.id]["leave"] = 0
        else:
            chans[str(ctx.guild.id)]["welcome"] = channel.id
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)
        await ctx.respond(f"Set {channel} as your welcome channel.")
    @discord.slash_command(name="setleavechannel",description="Sets your leave channel.") # we can also add application commands
    async def _levchan(self, ctx, channel: discord.Option(discord.TextChannel)):
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if not str(ctx.guild.id) in chans:
            chans[ctx.guild.id] = {}
            chans[ctx.guild.id]["welcome"] = 0
            chans[ctx.guild.id]["leave"] = channel.id
        else:
            chans[str(ctx.guild.id)]["leave"] = channel.id
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)
        await ctx.respond(f"Set {channel} as your welcome channel.")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Channels(bot)) # add the cog to the bot