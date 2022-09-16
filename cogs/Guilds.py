import discord
from discord.ext import commands
import json

class Guilds(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
    @commands.Cog.listener() # we can add event listeners to our cog
    async def on_member_join(self, member): # this is called when a member joins the server
        with open("channels.json", "r") as f:
            chan = json.load(f)
        if not int(chan[str(member.guild.id)]["welcome"]) == 0:
            channel = self.bot.get_channel(int(chan[str(member.guild.id)]["welcome"]))
            await channel.send('Welcome to the server, {member.mention}!')
    @commands.Cog.listener() # we can add event listeners to our cog
    async def on_member_leave(self, member): # this is called when a member joins the server
        with open("channels.json", "r") as f:
            chan = json.load(f)
        if not int(chan[str(member.guild.id)]["leave"]) == 0:
            channel = self.bot.get_channel(int(chan[str(member.guild.id)]["leave"]))
            await channel.send('Cya later, {member}.')
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("channels.json", "r") as f:
            chans = json.load(f)
            if not str(guild.id) in chans:
                chans[guild.id] = {}
                chans[guild.id]["welcome"] = 0
                chans[guild.id]["leave"] = 0
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)
        with open("guilds.json", "r") as f:
            guilds = json.load(f)
        if not str(guild.id) in guilds:
            guilds[guild.id] = {}
            guilds[guild.id]["over18"] = "False"
    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        with open("channels.json", "r") as f:
            chans = json.load(f)
            if str(guild.id) in chans:
                chans.pop(chans[str(guild.id)])
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Guilds(bot)) # add the cog to the bot