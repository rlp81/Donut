import discord
import json
from discord.ext import commands
import configparser
config = configparser.ConfigParser()
confile = config.read("config.conf")
class botinfo:
    guilds = []
bot = discord.Bot()

#events

@bot.event
async def on_ready():
    print("Donut is online!")
    with open("guilds.json","r") as f:
        guilds = json.load(f)
    botinfo.guilds = guilds
@bot.event
async def on_member_leave(member: discord.Member):
    with open("channels.json","r") as f:
        channels: dict = json.load(f)
    if member.guild.id in channels:
        channel = channels[member.guild.id]["leave"]
        if channel:
            await channel.send(f"{member} has saddly left us.")
        else:
            pass
    else:
        pass
@bot.event
async def on_member_join(member: discord.Member):
    with open("channels.json","r") as f:
        channels: dict = json.load(f)
    if member.guild.id in channels:
        channel = channels[member.guild.id]["welcome"]
        if channel:
            await channel.send(f"Welcome to {member.guild.name}, {member.mention}!")
        else:
            pass
    else:
        pass
@bot.event
async def on_guild_join(guild: discord.Guild):
    with open("guilds.json","r") as f:
        guilds: list = json.load(f)
    guilds.append(guild.id)
    with open("guilds.json", "w") as f:
        json.dump(guilds,f,indent=4)
@bot.event
async def on_guild_leave(guild: discord.Guild):
    with open("guilds.json","r") as f:
        guilds: list = json.load(f)
    guilds.pop(guild.id)
    with open("guilds.json", "w") as f:
        json.dump(guilds,f,indent=4)

#commands

@bot.slash_command(name="echo",guild_ids=[806540680473346058])
async def slash(ctx,*,message):
    await ctx.respond(message)
@bot.slash_command(name="boticon",guild_ids=[806540680473346058])
async def boticon(ctx):
    await ctx.send(bot.user.avatar)

if __name__ == "__main__":
    bot.run(config.get("config","token"))
