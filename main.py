import discord 
from discord.utils import get
import youtube_dl
from discord.ext import commands, tasks
import asyncio
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from itertools import cycle
import aiohttp
import io
import traceback
import time
import logging
import requests
import sys
import os
import shutil
from os import system
import json 
client = discord.Client()
from colorama import init, Fore, Back, Style
import datetime
from discord.voice_client import VoiceClient
import random
from asyncio import sleep as s 
from asyncio import sleep 
init(convert=True)


queue = []
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ";", intents=intents)
client.remove_command('help')
ROLE = "user"
api_key = 'a90a2e9106e4cc839a1327a5fd8fea00'
base_url = "http://api.openweathermap.org/data/2.5/weather?"




filtered_words = ["nigger", "cp", "child porn", "kkk"]

@client.event
async def on_ready():
    print("Bot is online")
    await client.change_presence(activity=discord.Game(name=f"world simulator")) # This changes the bots 'activity'


#help

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help ", description = f"``* means the command has a subcommand\nnote: the music is in beta``",color = 0xd65c27)

    em.add_field(name = "\n \nModeration", value = "``ban, unban, massunban, kick, jail, unjail, purge, bc, lockdown, toggle*``", inline=False)
    em.add_field(name = "Economy", value = "``shop, balance*, beg, deposit*, withdraw*, send*, rob*, slots,\nbuy, sell, bag, leaderboard*``", inline=False)
    em.add_field(name = "\n \nFun", value = "``wanted, hitler, ``", inline=False)
    em.add_field(name = "Music", value = "``join*, leave*, play*, pause, resume, np*, queue*, skip,\nvolume*``", inline=False)
    em.add_field(name = "Utility", value = "``snipe, av*, btc*, eth*, role, seticon*, userinfo*, createrole*, deleterole*, weather``", inline=False)

    await ctx.send(embed = em)


@client.event
async def on_message(ctx):
   if "discord.gg" in ctx.content.lower():
       await ctx.delete()
       emb = discord.Embed(description=f"<:xx:866167093048377395> Advertising is not allowed", color=0xe25c5c)
       await ctx.channel.send(embed=emb)
       await client.process_commands(ctx)


#user-info

@client.command(aliases=['ui'])
async def userinfo(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]



    embed = discord.Embed(timestamp=ctx.message.created_at, color = 0xd65c27)
    
    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild Name:", value=member.display_name)

    embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)

    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)


@help.command()
async def jail(ctx):

    em = discord.Embed(title = "Syntax", description = ";jail (user) <reason>",color = 0xd65c27)


    em.add_field(name = "**Examples**", value = ";jail mp5#4746 dumb")

    await ctx.send(embed = em)

    
@help.command()
async def unjail(ctx):

    em = discord.Embed(title = "Syntax", description = ";unjail (user) <reason>",color = 0xd65c27)


    em.add_field(name = "**Examples**", value = ";unjail mp5#4746 good boy")

    await ctx.send(embed = em)



#role


@client.command('role')
@commands.has_permissions(administrator=True) #permissions
async def role(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
    return await ctx.send('**:x: | That role is above your top role!**') 
  if role in user.roles:
      await user.remove_roles(role) #removes the role if user already has
      emb = discord.Embed(description=f"<:check:818339901959438346> {ctx.author.mention} Removed the role  **{role}** from {user.mention}", color = 0x2ecc71)
      await ctx.send(embed=emb)
  else:
      await user.add_roles(role) #adds role if not already has it
      emb = discord.Embed(description=f"<:check:818339901959438346> {ctx.author.mention} Added the role **{role}** to {user.mention}", color = 0x2ecc71)
      await ctx.send(embed=emb)


#createrole


@client.command(aliases=['crole', 'makerole'])
@commands.has_permissions(manage_roles=True) # Check if the user executing the command can manage roles
async def createrole(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role **{name}** has been created')

@createrole.error
async def createrole_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(description=f":warning: {ctx.author.mention}: Please specify a role to create", color=0xf1c40f)
            await ctx.send(embed=emb)

#removerole

@client.command(aliases=['delete', 'delrole', 'drole'], name="deleterole", pass_context=True)
async def deleterole(ctx, role_name):
    #find role object
    role_object = discord.utils.get(ctx.message.guild.roles, name=role_name)
    #delete role
    await role_object.delete()
    emb = discord.Embed(description=f"<:check:818339901959438346> {ctx.author.mention} Deleted the role **{role_name}**", color = 0x2ecc71)
    await ctx.send(embed=emb)


@deleterole.error
async def deleterole_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(description=f":warning: {ctx.author.mention}: Please specify a role to delete", color=0xf1c40f)
            await ctx.send(embed=emb)


#btc

@client.command(aliases=['bitcoin'])
async def btc(ctx):
	r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
	r = r.json()
	usd = r['USD']
	eur = r['EUR']
	embed = discord.Embed(color=(0xf2a900))
	embed.description=f'**{str(usd)}$ USD**'
	embed.set_author(name='Bitcoin', icon_url='https://media.discordapp.net/attachments/806971294795956254/808381684012810310/600.png?width=480&height=480')
	embed.set_footer(text='updated bitcoin prices to this hour')
	await ctx.send(embed=embed)
	    
#eth

@client.command(aliases=['ethereum'])
async def eth(ctx):
	r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR')
	r = r.json()
	usd = r['USD']
	eur = r['EUR']
	embed = discord.Embed(color=(0x3c3c3d))
	embed.description=f'**{str(usd)}$ USD**'
	embed.set_author(name='Ethereum', icon_url='https://cdn.discordapp.com/attachments/810358947142697021/821943190906994718/ethicon.png')
	await ctx.send(embed=embed)

@client.command(brief='Restarts the bot.')
@commands.has_permissions(ban_members=True)
async def restart(ctx: commands.Context):
	try:
		await client.close()
	except:
		pass 
	finally:
		os.system('python main.py')

#economy

mainshop = [{"name":"Watch","price":100,"description":"Time"},
			{"name":"Beer","price":500,"description":"Drink"},
            {"name":"Glock","price":1000,"description":"Gun"},
            {"name":"AK47","price":1050,"description":"Gun"},
			{"name":"Weed","price":2000,"description":"Drugs"},
            {"name":"PC","price":10000,"description":"Gaming"},
            {"name":"Supra","price":70000,"description":"Car"}]

@client.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}'s Balance",color = 0xd65c27)
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)

@client.command()
@commands.cooldown(1, 20000, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(5900)
    emb = discord.Embed(description=f"{ctx.author.mention} Got {earnings} coins", color = 0xd65c27)
    await ctx.send(embed=emb)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@client.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        emb = discord.Embed(description=f"{ctx.author.mention} Please specify an amount", color = 0xd65c27)
        await ctx.send(embed=emb)
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        emb = discord.Embed(description=f"{ctx.author.mention} You don't have a sufficient balance", color = 0xd65c27)
        await ctx.send(embed=emb)
        return
    if amount < 0:
        emb = discord.Embed(description=f"{ctx.author.mention} Please specify an amount", color = 0xd65c27)
        await ctx.send(embed=emb)
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    emb = discord.Embed(description=f"{ctx.author.mention} You withdrew {amount} coins", color = 0xd65c27)
    await ctx.send(embed=emb)


@client.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        emb = discord.Embed(description=f"{ctx.author.mention} Please specify an amount", color = 0xd65c27)
        await ctx.send(embed=emb)
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        emb = discord.Embed(description=f"{ctx.author.mention} You don't have a sufficient balance", color = 0xd65c27)
        await ctx.send(embed=emb)
        return
    if amount < 0:
        emb = discord.Embed(description=f"{ctx.author.mention} Please specify an amount", color = 0xd65c27)
        await ctx.send(embed=emb)
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    emb = discord.Embed(description=f"{ctx.author.mention} You deposited {amount} coins", color = 0xd65c27)
    await ctx.send(embed=emb)


@client.command(aliases=['sm'])
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        emb = discord.Embed(description=f"{ctx.author.mention} You don't have a sufficient balance", color = 0xd65c27)
        await ctx.send(embed=emb)
        return
    if amount < 0:
        emb = discord.Embed(description=f"{ctx.author.mention} Please specify an amount", color = 0xd65c27)
        await ctx.send(embed=emb)
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')


@client.command(aliases=['rb'])
async def rob(ctx,member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)


    if bal[0]<100:
        await ctx.send('It is useless to rob him')
        return

    earning = random.randrange(0,bal[0])

    await update_bank(ctx.author,earning)
    await update_bank(member,-1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


@client.command()
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        emb = discord.Embed(description=f"{ctx.author.mention} Please specify an amount", color = 0xd65c27)
        await ctx.send(embed=emb)
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        emb = discord.Embed(description=f"{ctx.author.mention} You don't have a sufficient balance", color = 0xd65c27)
        await ctx.send(embed=emb)
        return
    if amount < 0:
        emb = discord.Embed(description=f"{ctx.author.mention} Please specify an amount", color = 0xd65c27)
        await ctx.send(embed=emb)
        return
    final = []
    for i in range(3):
        a = random.choice([':cherries:',':grapes:',':lemon:', ':gem:'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        emb = discord.Embed(description=f"{ctx.author.mention} Won", color = 0xd65c27)
        await ctx.send(embed=emb)
    else:
        await update_bank(ctx.author,-1*amount)
        emb = discord.Embed(description=f"{ctx.author.mention} Lost", color = 0xd65c27)
        await ctx.send(embed=emb)


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)

#av

@client.command(aliases=['av'])
async def avatar(ctx, *, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(title = f"{member.name}'s avatar", color = member.color , timestamp= ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by : {ctx.author}",icon_url=ctx.author.avatar_url)  
    await ctx.send(embed=embed)

# A simple and small ERROR handler
@client.event 
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f' You must wait {int(s)} seconds to use this command')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command')
        else:
            await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command')
    raise error


@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            emb = discord.Embed(description=f"{ctx.author.mention} Please specify an item", color = 0xd65c27)
            await ctx.send(embed=emb)
            return
        if res[1]==2:
            emb = discord.Embed(description=f"{ctx.author.mention} You don't have enough money in your wallet to buy **{amount}** {item}", color = 0xd65c27)
            await ctx.send(embed=emb)
            return

    emb = discord.Embed(description=f"{ctx.author.mention} You just bought **{amount}** {item}", color = 0xd65c27)
    await ctx.send(embed=emb)


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
    

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            emb = discord.Embed(description=f"{ctx.author.mention} The item isn't available", color = 0xd65c27)
            await ctx.send(embed=emb)
            return
        if res[1]==2:
            emb = discord.Embed(description=f"{ctx.author.mention} You don't have **{amount}** {item} in your bag", color = 0xd65c27)
            await ctx.send(embed=emb)
            return
        if res[1]==3:
            emb = discord.Embed(description=f"{ctx.author.mention} You don't have {item} in your bag", color = 0xd65c27)
            await ctx.send(embed=emb)
            return

    emb = discord.Embed(description=f"{ctx.author.mention} You just sold **{amount}** {item}", color = 0xd65c27)
    await ctx.send(embed=emb)

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xF2684A))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal



@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
            await client.process_commands(msg)





    

@client.event
async def on_message(message):
    if message.content.lower().startswith("idc"):
        await message.channel.send("https://media.discordapp.net/attachments/819272097930412122/819973602195013652/imdeadaf.gif")

    #await client.process_commands(message)



@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, content=1):
    content = int(content)
    
    await ctx.message.delete()
    deleted = await ctx.message.channel.purge(limit=content, before=ctx.message)

    emb = discord.Embed(description=f"<:check:818339901959438346> {ctx.author.mention}: {(len(deleted))} messages cleared", color=0x2ecc71)
    await ctx.send(embed=emb)

@client.command(pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def bc(ctx, max_messages=1000):
    if max_messages > 2000:
        await ctx.send('Please choose a number 1 - 2000')
        return

    def is_bot(m):
        return m.author.bot

    #await ctx.channel.purge(limit=50, check=is_bot)

    deleted = await ctx.message.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: m.author.bot)
    print(len(deleted))
    emb = discord.Embed(description=f"<:check:818339901959438346> {ctx.author.mention}: {(len(deleted))} messages cleared", color=0x2ecc71)
    await ctx.send(embed=emb)

#ban

@client.command(aliases=['yeet', 'deport'])
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def ban(ctx, member: discord.Member, *, reason=None):
        try:
          await member.ban(reason=reason)
          await ctx.send(":thumbsup:")
        except:
              await ctx.send(f"`{ctx.author}` I require `Administrator` to perform that action") 
    
@ban.error
async def ban_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(description=f":warning: {ctx.author.mention}: Please specify a member", color=0xf1c40f)
            await ctx.send(embed=emb)

#toggle

@client.command(aliases=['togglecommand'])
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def toggle(ctx, command):
        command = client.get_command(command)
        

        if command is None:
            emb = discord.Embed(description=f"<:error:867509993884614666> {ctx.author.mention} That command is disabled or doesn't exist", color=0xec6a6a)
            await ctx.send(embed=emb)

        elif ctx.command == command:
            emb = discord.Embed(description=f"<:error:867509993884614666> {ctx.author.mention} You can't disabled this command", color=0xec6a6a)
            await ctx.send(embed=emb)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            emb = discord.Embed(description=f"<:check:818339901959438346> {ctx.author.mention} I have {ternary} the command **{command.qualified_name}**", color=0x2ecc71)
            await ctx.send(embed=emb)

#massunban

@client.command()
@commands.has_permissions(ban_members=True)
async def massunban(ctx):
    banlist = await ctx.guild.bans()
    for users in banlist:
        try:
            await ctx.guild.unban(user=users.user)
        except:
            pass
    emb = discord.Embed(description=f"<:check:818339901959438346> Mass Unbanning", color=0x2ecc71)
    await ctx.send(embed=emb)

@massunban.error
async def massunban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(description=f"<:error:867509993884614666> {ctx.author.mention}: You are missing permissions", color = 0xec6a6a)
            await ctx.send(embed=emb)


#wanted

@client.command()
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    
    wanted = Image.open("wanted.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((190,190))

    wanted.paste(pfp, (135,230))

    wanted.save("profile.jpg")

    await ctx.send(file = discord.File("profile.jpg"))

#hitler

@client.command()
async def hitler(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    
    hitler = Image.open("hitler.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((145,145))

    hitler.paste(pfp, (58,50))

    hitler.save("profile.jpg")

    await ctx.send(file = discord.File("profile.jpg"))




@client.command()
@commands.cooldown(1, 2, commands.BucketType.user) #cooldown
async def hello(ctx):
    await ctx.send("hi :wave:")


#unban

@client.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def unban(ctx, *, user=None):

    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        emb = discord.Embed(description=f"<:error:867509993884614666> user could not be found", color = 0xec6a6a)
        await ctx.send(embed=emb)
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            emb = discord.Embed(description=f"<:error:867509993884614666> User not banned", color = 0xec6a6a)
            await ctx.send(embed=emb)
            return

    except discord.Forbidden:
        await ctx.send("I do not have permission to unban!")
        return

    except:
        await ctx.send("Unbanning failed!")
        return

    await ctx.send("👍")



@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="chat")
    await channel.send(f"**{member.mention}** welcome to germany")
    role = get(member.guild.roles, name=ROLE)
    await member.add_roles(role)

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server!')
    with open('afk.json', 'r') as f:
        afk = json.load(f)

    await update_data(afk, member)

    with open('afk.json', 'w') as f:
        json.dump(afk, f)


async def update_data(afk, user):
    if not f'{user.id}' in afk:
        afk[f'{user.id}'] = {}
        afk[f'{user.id}']['AFK'] = 'False'


@client.event
async def on_message(message):
    with open('afk.json', 'r') as f:
        afk = json.load(f)

    for x in message.mentions:
        if afk[f'{x.id}']['AFK'] == 'True':
            if message.author.bot:
                return
            await message.channel.send(f'{x} is currently AFK')

    if not message.author.bot:
        await update_data(afk, message.author)

        if afk[f'{message.author.id}']['AFK'] == 'True':
            await message.channel.send(f'{message.author.mention} is no longer afk!')
            afk[f'{message.author.id}']['AFK'] = 'False'
            with open('afk.json', 'w') as f:
                json.dump(afk, f)
            await message.author.edit(nick=f'{message.author.display_name[5:]}')

    with open('afk.json', 'w') as f:
        json.dump(afk, f)

    await client.process_commands(message)

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server!')


#giveaway

@client.command()
@commands.has_permissions(manage_roles=True)
async def giveaway(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly

    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = ['Which channel will I host the giveaway in?', 'What is the prize?', 'How long should the giveaway run for (in seconds)?',]
    giveaway_answers = []

    # Checking to be sure the author is the one who answered and in which channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    # Askes the questions from the giveaway_questions list 1 by 1
    # Times out if the host doesn't answer within 30 seconds
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for('message', timeout= 30.0, check= check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time.  Please try again and be sure to send your answer within 30 seconds of the question.')
            return
        else:
            giveaway_answers.append(message.content)

    # Grabbing the channel id from the giveaway_questions list and formatting is properly
    # Displays an exception message if the host fails to mention the channel correctly
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(f'You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}')
        return
    
    # Storing the variables needed to run the rest of the commands
    channel = client.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.send(f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds.')

    # Giveaway embed message
    give = discord.Embed(color = 0x2ecc71)
    give.set_author(name = f'Giveaway')
    give.add_field(name= f'{ctx.author.name} is giving away: {prize}', value = f'React with 🎉 to enter!\n Ends in {round(time/60, 2)} minutes!', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
    give.set_footer(text = f'Giveaway ends at {end} EST')
    my_message = await channel.send(embed = give)
    
    # Reacts to the message
    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the winner
    winning_announcement = discord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'Giveaway has ended', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 Prize: {prize}', value = f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Thanks for entering!')
    await channel.send(embed = winning_announcement)

#reroll

@client.command()
@commands.has_permissions(manage_roles=True)
async def reroll(ctx, channel: discord.TextChannel, id_ : int):
    # Reroll command requires the user to have a "Giveaway Host" role to function properly
    try:
        new_message = await channel.fetch_message(id_)
    except:
        await ctx.send("Invalid ID")
        return
    
    # Picks a new winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the new winner to the server
    reroll_announcement = discord.Embed(color = 0xff2424)
    reroll_announcement.set_author(name = f'The giveaway was re-rolled by the host')
    reroll_announcement.add_field(name = f'New Winner:', value = f'{winner.mention}', inline = False)
    await channel.send(embed = reroll_announcement)

#seticon

@client.command(aliases=['changeicon'])
@commands.has_permissions(manage_roles=True)
async def seticon(ctx, url: str):
    """Set the guild icon."""
    if ctx.message.guild is None:
        return

    permissions = ctx.message.author.permissions_in(ctx.channel)
    if not permissions.administrator:
        print("user is not admin")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.message.guild.edit(icon=data.read())
            embed = discord.Embed(description=f"<:check:818339901959438346> The Server Icon was changed", color = 0x2ecc71)
            await ctx.send(embed=embed)

@seticon.error
async def guild_edit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description=f"<:error:867509993884614666> {ctx.author.mention}: Please send a URL to change to", color = 0xec6a6a)
        await ctx.send(embed=emb)



#afk

@client.command()
async def afk(ctx, reason=None):
    with open('afk.json', 'r') as f:
        afk = json.load(f)

    if not reason:
        reason = 'None'

    afk[f'{ctx.author.id}']['AFK'] = 'True'
    await ctx.send(f'{ctx.author.display_name} is now AFK, Reason: {reason}')

    with open('afk.json', 'w') as f:
        json.dump(afk, f)

    await ctx.author.edit(nick=f'[AFK]{ctx.author.display_name}')


#cogs

cogs = ["music"]

for cog in cogs:
    client.load_extension("music")


#weather

@client.command()
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel	
    if x["cod"] != "404":
        async with channel.typing():	
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]	
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}",
                              color=ctx.guild.me.top_role.color,
                              timestamp=ctx.message.created_at,)
            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send("City not found.")

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)

@client.event
async def on_message_delete(message):
    embed = discord.Embed(title="{} deleted a message".format(message.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message.content, value="This is the message that he has deleted",
                    inline=True)
    channel = client.get_channel(815792270921433128)
    await channel.send(channel, embed=embed)


@client.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title="{} edited a message".format(message_before.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message_before.content, value="This is the message before any edit",
                    inline=True)
    embed.add_field(name=message_after.content, value="This is the message after the edit",
                    inline=True)
    channel = client.get_channel(815792270921433128)
    await channel.send(channel, embed=embed)



@client.command(description="Mutes the specified user.", invoke_without_command=True)
@commands.has_permissions(manage_roles=True)
@commands.cooldown(1, 2, commands.BucketType.user) 
async def jail(ctx, member: discord.Member, *, reason='No reason was specified'):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="jailed")

    if not mutedRole:
        mutedRole = await guild.create_role(name="jailed")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_messages=False)


    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f":thumbsup:")
    retard = discord.Embed(
        title='Jailed',
        description = f"You have been jailed in {ctx.message.guild.name}\n \n Reason: {reason}",
        color= discord.Color.red()
    )
    await member.send(embed=retard)

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 2, commands.BucketType.user) 
async def unjail(ctx, member: discord.Member= None, *, reason='No reason was specified'):
    guild = ctx.guild
    mutedRole = discord.utils.get(ctx.guild.roles, name="jailed")
    unretard = discord.Embed(
        title='Unjailed',
        description = f"You have been unjailed in {ctx.message.guild.name}\n \n Reason: {reason}",
        color= discord.Color.green()
    )
    await member.remove_roles(mutedRole)
    await member.send(embed=unretard)
    await ctx.send(f":thumbsup:")


@client.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_channels=True)
@commands.bot_has_guild_permissions(manage_channels=True)
async def lockdown(ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"I have put **{channel.name}** on lockdown.")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have put **{channel.name}** on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have unlocked **{channel.name}**")



#https://discord.com/developers/applications ,make an app,make a bot,go in OAuth2,select bot,scroll and select admin , then copy the link displayed, paste that into your browser and add it to the server that needs cleaning
channeltodelete = "nuke, nuked, spam, raid" #change to channel name that was mass created
roletodelete = "nuke, spam, rolespam, new role"   #change to role name that was mass created
#space sensitive








@client.command()
async def roleclean(ctx):
    await ctx.message.delete()
    for role in ctx.message.guild.roles:
            if role.name == roletodelete:
                try:
                    await role.delete()
                except discord.HTTPException as e:
                    print(f"Failed to delete role: {role.name}. Likely missing perms")
                    continue
                else:
                    currentDT = datetime.datetime.now()
                    hour = str(currentDT.hour)
                    minute = str(currentDT.minute)
                    second = str(currentDT.second)
                    print(f"{Fore.RED}[{Fore.WHITE}{hour}:{minute}:{second}{Fore.RED}]{Fore.GREEN} Deleted Role: {role.name}")
    print(f"\n\n{Fore.CYAN}Cleared all roles called '{roletodelete}'")


@client.command()
async def channelclean(ctx):
    await ctx.message.delete()
    for channel in ctx.message.guild.channels:
        if channel == "Text Channels":
            continue
        elif channel == "Voice Channels":
            continue
        if channel.name == channeltodelete:
            try:
                await channel.delete()
            except discord.Forbidden as e:
                print(f"Failed to delete channel {channel.name}. Likely missing perms")
                continue
            else:
                currentDT = datetime.datetime.now()
                hour = str(currentDT.hour)
                minute = str(currentDT.minute)
                second = str(currentDT.second)
                print(f"{Fore.RED}[{Fore.WHITE}{hour}:{minute}:{second}{Fore.RED}]{Fore.GREEN} Channel Deleted - {channel.name}")




    print(f"\n\n{Fore.CYAN}Cleared all channels called '{channeltodelete}',be careful when adding unknown bots in the future.\nBe especially careful if the bot is in few servers,requires permissions \nor if the person who requested for it to be added seems desperate.\nAny bot with admin could've easily mass banned and wiped your server,\nthat I have no cure for, so do look out in the future!\n\nGood luck and I'm happy I was able to help!")


client.load_extension('jishaku')

client.run(os.environ['DISCORD_TOKEN'])
