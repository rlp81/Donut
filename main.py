import discord
import json
import os
import configparser
config = configparser.ConfigParser()
confile = config.read("config.conf")
bot = discord.Bot(debug_guilds=[])
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
for file in os.listdir(f"{os.getcwd()}/cogs"):
    if file.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{file[:-3]}")
            print(f"cogs.{file[:-3]} loadeded successfully")
        except:
            print(f"cogs.{file[:-3]} failed to load")

@bot.slash_command()
async def load(context, extintion):
    try:
        bot.load_extension(f'cogs.{extintion}')
        await context.send(f"cogs.{extintion} loaded sucessfully!")
    except:
        await context.send(f"cogs.{extintion} failed to load!")
@bot.slash_command()
async def unload(context, extintion):
    try:
        bot.unload_extension(f'cogs.{extintion}')
        await context.send(f"cogs.{extintion} unloaded sucessfully!")
    except:
        await context.send(f"cogs.{extintion} failed to unload!")

@bot.slash_command(name="reload", description="Reload a cog")
async def reload(context, extintion):
        try:
            bot.unload_extension(f'cogs.{extintion}')
            bot.load_extension(f'cogs.{extintion}')
            await context.send(f"cogs.{extintion} reloaded sucessfully!")
        except:
            await context.send(f"cogs.{extintion} failed to reload!")

if __name__ == "__main__":
    bot.run(config.get("config","token"))
