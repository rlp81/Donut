import discord
import json
import os
import configparser
config = configparser.ConfigParser()
confile = config.read("config.conf")
bot = discord.Bot(debug_guilds=[806540680473346058])
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

if __name__ == "__main__":
    bot.run(config.get("config","token"))