import discord
import json
import random
from discord.ext import commands

class Economy(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot
    econ = discord.SlashCommandGroup("economy","Economy related commands")
    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open("balance.json","r") as f:
            bal = json.load(f)
        with open("inventory.json","r") as f:
            inv = json.load(f)
        if not str(message.channel.guild.id) in inv:
            inv[str(message.channel.guild.id)] = {}
            if not str(message.author.id) in inv[str(message.channel.guild.id)]:
                inv[str(message.channel.guild.id)][str(message.author.id)] = {}
        if not str(message.author.id) in inv[str(message.channel.guild.id)]:
            inv[str(message.channel.guild.id)][str(message.author.id)] = {}
        if str(message.author.id) in bal[str(message.guild.id)]:
            id = message.author.id
            bal[str(message.guild.id)][str(id)]["wallet"] += 1
        else:
            id = message.author.id
            if not str(message.guild.id) in bal:
                bal[str(message.guild.id)] = {}
            bal[str(message.guild.id)][str(id)] = {}
            bal[str(message.guild.id)][str(id)]["wallet"] = 1
            bal[str(message.guild.id)][str(id)]["bank"] = 0
        with open("balance.json", "w") as f:
            json.dump(bal, f, indent=4)
        with open("inventory.json", "w") as f:
            json.dump(inv, f, indent=4)
    @econ.command(name="shop", description="Lists what's available in the shop.")
    async def _shop(self, ctx):
        with open("shop.json", "r") as f:
            shop = json.load(f)
        emb = discord.Embed(title="Shop")
        if not str(ctx.guild.id) in shop:
            shop[str(ctx.guild.id)] = {}
            shop[str(ctx.guild.id)]["items"] = {}
            shop[str(ctx.guild.id)]["money"] = {}
            shop[str(ctx.guild.id)]["money"]["total"] = 0
            with open("shop.json", "w") as f:
                json.dump(shop, f, indent=4)
            store = shop[str(ctx.guild.id)]["items"]
            for item, value in shop[str(ctx.guild.id)]["items"]:
                emb.add_field(name=f"ID: {item} Name: {store['name']} Description: {store['desc']}", value=f"Price: {store['price']}", inline=False)
        else:
            for item, value in shop[str(ctx.guild.id)]["items"].items():
                store = shop[str(ctx.guild.id)]["items"][str(item)]
                emb.add_field(name=f"ID: {item} Name: {store['name']} Description: {store['desc']}", value=f"Price: {store['price']}", inline=False)
        await ctx.respond(embed=emb)
    @econ.command(name="additem", description="Adds a new item to the shop")
    async def _additem(self, ctx, name: str, desc: str, price: int):
        with open("shop.json", "r") as f:
            shop = json.load(f)
        id = random.randint(000,999)
        shop[str(ctx.guild.id)]["items"][str(id)] = {}
        shop[str(ctx.guild.id)]["items"][str(id)]["name"] = name
        shop[str(ctx.guild.id)]["items"][str(id)]["desc"] = desc
        shop[str(ctx.guild.id)]["items"][str(id)]["price"] = price
        shop[str(ctx.guild.id)]["items"][str(id)]["settings"] = {}
        shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["addrole"] = "False"
        shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["removerole"] = "False"
        shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["role"] = ""
        shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["sellable"] = "True"
        with open("shop.json", "w") as f:
            json.dump(shop, f, indent=4)
        await ctx.respond(f"Added item {shop[str(ctx.guild.id)]['items'][str(id)]['name']} with price {shop[str(ctx.guild.id)]['items'][str(id)]['price']}")
    @econ.command(name="edititem", description="Edits an item in the shop")
    async def _additem(self, ctx, id: int, newid: int = None, name: str = None, desc: str = None, price: int = None, addrole: bool = None, removerole: bool = None, role: int = None, sellable: bool = None):
        with open("shop.json", "r") as f:
            shop = json.load(f)
        if str(id) in shop[str(ctx.guild.id)]["items"]:
            if newid != None:
                shop[str(ctx.guild.id)]["items"][str(newid)] = shop[str(ctx.guild.id)]["items"][str(id)]
                shop[str(ctx.guild.id)]["items"].pop(str(id))
            if name != None:
                shop[str(ctx.guild.id)]["items"][str(id)]["name"] = name
            if desc != None:
                shop[str(ctx.guild.id)]["items"][str(id)]["desc"] = desc
            if price != None:
                shop[str(ctx.guild.id)]["items"][str(id)]["price"] = price
            if addrole != None:
                shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["addrole"] = f"{addrole}"
            if removerole != None:
                shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["removerole"] = f"{removerole}"
            if role != None:
                shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["role"] = ""
            if sellable != None:
                shop[str(ctx.guild.id)]["items"][str(id)]["settings"]["sellable"] = f"{sellable}"
        with open("shop.json", "w") as f:
            json.dump(shop, f, indent=4)
        await ctx.respond(f"Edited item successfully")
    @econ.command(name="removeitem", description="Removes an item from the shop")
    async def _additem(self, ctx, id: int):
        with open("shop.json", "r") as f:
            shop = json.load(f)
        if str(id) in shop[str(ctx.guild.id)]["items"]:     
            name = shop[str(ctx.guild.id)]["items"][str(id)]["name"]
            shop[str(ctx.guild.id)]["items"].pop(str(id))
            await ctx.respond(f"Removed item {name}")
        else:
            await ctx.respond(f"Item {id} not found")
        with open("shop.json", "w") as f:
            json.dump(shop, f, indent=4)
    @econ.command(name="buy", description="Buys an item from the shop")
    async def buy(self, ctx, item: int):
        with open("shop.json", "r") as f:
            shop = json.load(f)
        with open("balance.json","r") as f:
            bal = json.load(f)
        if str(item) in shop[str(ctx.guild.id)]["items"]:
            price = int(shop[str(ctx.guild.id)]["items"][str(item)]["price"])
            if int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) >= price:
                with open("inventory.json", "r") as f:
                    inv = json.load(f)
                bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) - price
                if str(ctx.guild.id) in inv:
                    if str(ctx.author.id) in inv[str(ctx.guild.id)]:
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]
                    if not str(ctx.author.id) in inv[str(ctx.guild.id)]:
                        inv[str(ctx.guild.id)][str(ctx.author.id)] = {}
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]

                else:
                    inv[str(ctx.guild.id)] = {}
                    if str(ctx.author.id) in inv[str(ctx.guild.id)]:
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]
                    else:
                        inv[str(ctx.guild.id)][str(ctx.author.id)] = {}
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]
                name = inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['name']
                with open("balance.json", "w") as f:
                    json.dump(bal, f, indent=4)
                with open("inventory.json", "w") as f:
                    json.dump(inv, f, indent=4)
                await ctx.respond(f"You have successfully bought item {name} for {price}")
            else:
                await ctx.respond(f"You do not have an money for item {name}.")        
        else:
            await ctx.respond(f"Item {item} not found")
    @econ.command(name="inventory", description="Shows your inventory")
    async def inventory(self, ctx):
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        emb = discord.Embed(title="Inventory", description="Shows the user's inventory")
        if str(ctx.guild.id) in inv:
            if str(ctx.author.id) in inv[str(ctx.guild.id)]:
                for item, value in inv[str(ctx.guild.id)][str(ctx.author.id)].items():
                    emb.add_field(name=f"ID: {item} Name: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['name']}", value=f"Price: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['price']} Sellable: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['settings']['sellable']}", inline=False)
            else:
                inv[str(ctx.guild.id)][str(ctx.author.id)] = {}
                for item, value in inv[str(ctx.guild.id)][str(ctx.author.id)].items():
                    emb.add_field(name=f"ID: {item} Name: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['name']}", value=f"Price: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['price']} Sellable: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['settings']['sellable']}", inline=False)
        else:
            inv[str(ctx.guild.id)] = {}
            inv[str(ctx.guild.id)][str(ctx.author.id)] = {}
            for item, value in inv[str(ctx.guild.id)][str(ctx.author.id)].items():
                emb.add_field(name=f"ID: {item} Name: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['name']}", value=f"Price: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['price']} Sellable: {inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['settings']['sellable']}", inline=False)
        await ctx.respond(embed=emb)
    @econ.command(name="sell", description="Sells an item")
    async def sell(self, ctx, id: int = None, sellall: bool = None):
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        with open("balance.json", "r") as f:
            bal = json.load(f)
        if id != None:
            if inv[str(ctx.guild.id)][str(ctx.author.id)][str(id)]['settings']['sellable'] == "True":
                price = inv[str(ctx.guild.id)][str(ctx.author.id)][str(id)]['price']
                name = inv[str(ctx.guild.id)][str(ctx.author.id)][str(id)]['name']
                bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) + int(inv[str(ctx.guild.id)][str(ctx.author.id)][str(id)]['price'])
                inv[str(ctx.guild.id)][str(ctx.author.id)].pop(str(id))
                await ctx.respond(f"Sold item {name} for {price}.") 
        if sellall != None:
            total = 0
            items = []
            for item, value in inv[str(ctx.guild.id)][str(ctx.author.id)].items():
                if inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['settings']['sellable'] == "True":
                    total += int(inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['price'])
                    bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) + int(inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['price'])
                    items.insert(1,item)
            for i in items:
                inv[str(ctx.guild.id)][str(ctx.author.id)].pop(str(i))
            await ctx.respond(f"Sold all sellable items for {total}.")
        with open("inventory.json", "w") as f:
            json.dump(inv, f, indent=4)
        with open("balance.json", "w") as f:
            json.dump(bal, f, indent=4)

    @econ.command(name="balance",description="Shows a person's balance")
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        id = member.id
        with open("balance.json","r") as f:
            bal = json.load(f)
        if str(id) in bal[str(ctx.guild.id)]:
            emb = discord.Embed(title=f"{member}'s Balance")
            emb.add_field(name="Wallet", value=bal[str(ctx.guild.id)][str(id)]["wallet"])
            emb.add_field(name="Bank", value=bal[str(ctx.guild.id)][str(id)]["bank"])
            await ctx.respond(embed=emb)
        else:
            bal[str(ctx.guild.id)][str(id)] = {}
            bal[str(ctx.guild.id)][str(id)]["wallet"] = 0
            bal[str(ctx.guild.id)][str(id)]["bank"] = 0
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            emb = discord.Embed(title=f"{member}'s Balance")
            emb.add_field(name="Wallet", value=bal[str(ctx.guild.id)][str(id)]["wallet"])
            emb.add_field(name="Bank", value=bal[str(ctx.guild.id)][str(id)]["bank"])
            await ctx.respond(embed=emb)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Economy(bot)) # add the cog to the bot