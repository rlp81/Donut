import discord


class Sus(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    @discord.slash_command(name="sus",description="Sussy wussy") # we can also add application commands
    async def sus(self, ctx):
        await ctx.respond("Sussy")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Sus(bot)) # add the cog to the bot