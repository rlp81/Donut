import discord
import asyncpraw
import random
from discord.ext import commands
import json
import configparser
config = configparser.ConfigParser()
confile = config.read("config.conf")
icon = "https://cdn.discordapp.com/attachments/898697869941428319/912823807130107914/test.png"
async def get_meme(subs):
    reddit = asyncpraw.Reddit(client_id=config.get("reddit","client_id"),
                        client_secret=config.get("reddit","client_secret"),
                        user_agent=config.get("reddit","user_agent"))
    choice = random.choice(list(subs))
    memes_submissions = []
    subreddit = await reddit.subreddit(choice)
    async for submission in subreddit.hot(limit=100):
        memes_submissions.append(submission)
    submission = random.choice(memes_submissions)
    #for i in range(0, post_to_pick):
    #submission = random.choice(memes_submissions)next(x for x in memes_submissions if not x.stickied)
    return submission, choice

async def get_meme1(message):
    reddit = asyncpraw.Reddit(client_id=config.get("reddit","client_id"),
                        client_secret=config.get("reddit","client_secret"),
                        user_agent=config.get("reddit","user_agent"))
    memes_submissions = []
    subreddit = await reddit.subreddit(f"{message}")
    async for submission in subreddit.hot(limit=100):
        memes_submissions.append(submission)
    submission = random.choice(memes_submissions)
    return submission

class Reddit_Meme(discord.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    @discord.slash_command(name="meme")
    async def _meme(self, ctx, message = None):
        over18 = False
        with open("subs.json","r") as f:
            subs = json.load(f)
        with open("guilds.json","r") as f:
            guilds = json.load(f)
        if guilds[str(ctx.guild.id)]["over18"] == "True":
            over18 = True
        elif guilds[str(ctx.guild.id)]["over18"] == "False":
            over18 = False
        sublist = ""
        for sub in subs:    
            sublist += f" {sub}"
        if message == None:
                
                #try:
                submission, choice = await get_meme(subs)
                if over18 == True:
                    emb = discord.Embed(title=f"r/{choice}|{submission.title}",description=f"posted by {submission.author}", color=0xff571e)
                    emb.set_image(url=submission.url)
                    emb.set_footer(text="Praw API :D",icon_url=icon)
                    await ctx.respond(embed=emb)
                if over18 == False:
                    if submission.over_18 == True:
                        await ctx.respond("Did not send meme because it was 18+")
                    if submission.over_18 == False:
                        emb = discord.Embed(title=f"r/{choice}|{submission.title}",description=f"posted by {submission.author}", color=0xff571e)
                        emb.set_image(url=submission.url)
                        emb.set_footer(text="Praw API :D",icon_url=icon)
                        await ctx.respond(embed=emb)

                #except:
                    #await context.send("Failed to send meme")
        if message != None:
            if str(message) in sublist:
                try:
                    submission = await get_meme1(message)
                    if submission.over_18 == True:
                        await ctx.send("Did not send meme because it was 18+")
                    if submission.over_18 == False:
                        emb = discord.Embed(title=f"r/{message}|{submission.title}",description=f"posted by {submission.author}", color=0xff571e)
                        emb.set_image(url=submission.url)
                        emb.set_footer(text="Praw API :D",icon_url=icon)
                        await ctx.respond(embed=emb)
                except:
                    await ctx.respond("Failed to send meme")
            else:
                await ctx.respond(f"{message} is not a supported subreddit.")
    @discord.slash_command(name="memes")
    async def _memes(self, context):
        bans = [818939178661838868]
        if not context.author.id in bans:
            with open("subs.json","r") as f:
                subs = json.load(f)
            sublist = ""
            for sub in subs:
                sublist += f" {sub}"
            await context.respond(f"Supported subreddits:{sublist}")
    

def setup(bot):
    bot.add_cog(Reddit_Meme(bot))