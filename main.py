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
import traceback
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
client = commands.Bot(command_prefix = ';', intents=intents)
client.remove_command('help')
ROLE = "user"


filtered_words = ["nigger", "cp", "child porn", "kkk"]

@client.event
async def on_ready():
    print("Bot is online")
    await client.change_presence(activity=discord.Game(name=f"jew simulator")) # This changes the bots 'activity'


@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = ":beer:  Help ", description = f"``* means the command has a subcommand``",color = 0xf28e1c)

    em.add_field(name = "\n \nModeration", value = "``ban, unban, kick, jail, unjail, bc``", inline=False)
    em.add_field(name = "Economy", value = "``shop, balance*, beg, deposit*, withdraw*, send*, rob*, slots,\nbuy, sell, bag, leaderboard*``", inline=False)
    em.add_field(name = "\n \nFun", value = "``wanted, hitler, ``", inline=False)
    em.add_field(name = "Music", value = "``join*, leave*, play*, pause, resume, np*, queue*, skip,\nvolume*``", inline=False)
    em.add_field(name = "Utility", value = "``snipe, av, btc*``", inline=False)

    await ctx.send(embed = em)

@help.command()
async def jail(ctx):

    em = discord.Embed(title = "Syntax", description = ";jail (user) <reason>",color = 0xf28e1c)


    em.add_field(name = "**Examples**", value = ";jail mp5#4746 dumb")

    await ctx.send(embed = em)




@help.command()
async def unjail(ctx):

    em = discord.Embed(title = "Syntax", description = ";unjail (user) <reason>",color = 0xf28e1c)


    em.add_field(name = "**Examples**", value = ";unjail mp5#4746 good boy")

    await ctx.send(embed = em)


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
		await bot.close()
	except:
		pass 
	finally:
		os.system('python main.py')

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

    em = discord.Embed(title=f"{ctx.author.name}'s Balance",color = 0xf28e1c)
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)

@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@client.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')


@client.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')


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
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
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
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice([':cherries:',':grapes:',':lemon:', ':gem:'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'{ctx.author.mention} Won')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'{ctx.author.mention} Lost')


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)


@client.command(aliases=['av'])
async def avatar(ctx,*, avamember):
    user = client.get_user(avamember)
    await ctx.send(f"{user.avatar_url}")   

# A simple and small ERROR handler
@client.event 
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
        await ctx.send(embed=embed)
    else:
        embed.add_field(name = f':x: Terminal Error', value = f"```{error}```")
        await ctx.send(embed = embed)
        raise error

    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f' You must wait {int(s)} seconds to use this command!')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have permission to use this command")
    raise error


@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


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
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

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

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
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


client.sniped_messages = {}

@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color = 0xf28e1c, timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)


    

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


@client.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def unban(ctx, *, user=None):

    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        emb = discord.Embed(description=f"<:deny:817896473852117034> user could not be found", color = 0xe74c3c)
        await ctx.send(embed=emb)
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            emb = discord.Embed(description=f"<:deny:817896473852117034> User not banned", color = 0xe74c3c)
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

    await ctx.send(f":thumbsup:")
    await member.remove_roles(mutedRole)
    await member.send(embed=unretard)






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




client.run(os.environ['DISCORD_TOKEN'])