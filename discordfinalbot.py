import asyncio
import http.client
import io
import json
import os
import random
import time
from io import BytesIO
from random import choice, randint, randrange
import discord
import requests
from discord import channel
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

intents = discord.Intents().all()
client = commands.Bot(command_prefix = '=', intents=intents)

client.remove_command("help")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        erem = discord.Embed(title = "Command Cooldown", description = "You cant use this command now. Try after **%.0fs**" % error.retry_after)
        await ctx.send(embed = erem)

    elif isinstance(error, commands.CommandNotFound):
        erem1 = discord.Embed(title = "Command Not Found", description = f"{error}")
        await ctx.send(embed = erem1)
        #The bot is under maintenance. Sorry for the inconvenience \n \n *P.S. - The only commands working are the **kill** and **pan** command. You can use these command to pass your time :-)*
    elif isinstance(error, commands.MissingPermissions):
        erem1 = discord.Embed(title = "Missing Permissions", description = f"You dont have permissions to run that command.")
        await ctx.send(embed = erem1)
    else:
        raise error


async def ch_pr():
    await client.wait_until_ready()
    
    statuses =["with your lives", f"on {len(client.guilds)} servers", f"a game in {len(client.guilds)} servers","with my creator, @SakshhamTheGamer", "Guess the Number game with my creator", "with fire", "songs for my creator" ]
    
    while not client.is_closed():
        
        status = random.choice(statuses)
        
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=status))
        
        await asyncio.sleep(3)

def check_stg(ctx):
    return ctx.message.author.id == 423008899302424596


modlog = {}

@client.event
async def on_ready():
    print("Bot is Ready")

@client.command()
async def status(ctx, member:discord.Member=None):
    if member == None:
        member = ctx.author
    await ctx.send(str(member.web_status))

@client.command()
async def ping(ctx):
    embed6 = discord.Embed(
    colour = 0xfff192,
    title = "Check the Ping",
    description = f"The ping is {round(client.latency * 1000)}ms"
    )
    
    await ctx.send (embed=embed6)

@client.command(aliases=['info', 'about','whoareyou'])
async def wru(ctx):
    await ctx.send (f'My name is SABRE Bot. I am a bot for SABRErs, by a SABREr')
    
    
@client.command(aliases=['ques','yn','8ball'])
async def ask(ctx, *,question):
    responses = ['Yes, definitely.',
                 'Nope, never ever',
                 "I love Strawberries",
                 "Taki Taki Rumba!",
                 "See, the complexity of this answer is beyond my reach, but I would like to try and say **YOU ARE AN IDIOT**",
                 "Well, It's the beginning of the end, I guess",
                 "Keep quiet and let me do my work. I am not here to answer such dumb question",
                 "I dont speak with idiots. Get outta here",
                 "I'm gonna stay neutral at it",
                 'Dont ask me this again'] 

    embed = discord.Embed(Title="ANSWER TO YOUR QUESTION", colour=0x6200ff)
    embed.add_field(name=f"You asked: {question}", value= f"The answer: {random.choice(responses)}")
    await ctx.send(embed=embed)



@client.command()
async def invite(ctx):
    embed2 = discord.Embed(
        title = "Invite this Bot to your server",
        color = 0xfee42b,
        description = '[Invite To Server](https://discord.com/api/oauth2/authorize?client_id=765628261413683261&permissions=8&scope=bot) 👈 Click to invite this bot to your server',
    )
    await ctx.send(embed=embed2)



@client.command()
async def embed(ctx,*, msg):
    if ";" in msg:
        msg=msg.split(";")
        await ctx.message.delete()
        embed = discord.Embed(title=msg[0], description = msg[1], colour=0xff4444)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=msg,colour=0xff4444)
        await ctx.message.delete()
        await ctx.send(embed=embed)


@client.command(aliases=['uinfo','usin','ui'])
async def userinfo(ctx, member:discord.Member=None):
    
    member = ctx.author if not member else member
    roles = [role for role in member.roles]
    
    embed = discord.Embed(colour=0xff2424)

    embed.set_author(name = f"Info for {member}")
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name="**NickName:**", value=member.display_name)
    embed.add_field(name="**UserName:**", value=f'{member}')
    embed.add_field(name="**Discord ID:**", value=member.id)
    embed.add_field(name="**Created at:**", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
    embed.add_field(name=f"**Total Roles assigned({len(roles)})**",value=" ".join([role.mention for role in roles]))

    await ctx.send (embed=embed)

@client.command()
async def avatar(ctx, member:discord.Member=None):
    member = ctx.author if not member else member
    
    embed = discord.Embed(colour=0xff2424)

    embed.set_author(name = f"Avatar for {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_image(url=member.avatar_url)

    await ctx.send(embed=embed)

@client.command(aliases=["lock"])
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    if overwrite.send_messages == False:
        await ctx.send(f"{channel.mention} is already locked 🔒")
    else:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f'{channel.mention} successfully locked 🔒')


@lockdown.error
async def clear_error(ctx, error):
    if isinstance (error, commands.MissingPermissions):
        await ctx.send("🛑 You dont have Administrative Permissions, so you can't use that")

@client.command(aliases=["unlockdown"])
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    if overwrite.send_messages == None or overwrite.send_messages == True:
        await ctx.send(f"{channel.mention} is already unlocked 🔓")
    else:
        await channel.set_permissions(ctx.guild.default_role, send_messages=None)
        await ctx.send(f'{channel.mention} successfully unlocked 🔓')

@unlock.error
async def clear_error(ctx, error):
    if isinstance (error, commands.MissingPermissions):
        await ctx.send("🛑 You dont have Administrative Permissions, so you can't use that")


@client.command(aliases=['purge', 'delete'])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=1):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send('{} message(s) cleared by {}'.format(amount, ctx.author), delete_after=3)
 

@client.group(invoke_without_command=True)
async def help(ctx):

    ebd = discord.Embed(title = "Help", description = "Type `=help` <command name> to learn more about a command.\nArguments in <> = Required\nArguments in [] = Optional", colour = 0xff4444)

    ebd.add_field(name = "Moderation", value = "Ban, Clear, Kick, Lock, Mute, Unban, Unlock, Unmute", inline=False)
    ebd.add_field(name = "Fun", value = "8ball, Embed, Kill, Pan, Quote, WhoAreYou", inline=False)
    ebd.add_field(name = "Utility", value = "Avatar, Createinv, Embed, Heist, Invite, Ping, Serverlink, Spotify, Timer, Userinfo", inline=False)
    ebd.add_field(name = "Games", value = "Guess, Typerace", inline=False)
    ebd.add_field(name="Economy", value="Balance, Beg", inline=False)
    ebd.add_field(name="Other", value="apply", inline=False)

    await ctx.send(embed=ebd)

@help.command(aliases=['mod'])
async def moderation(ctx):
    
    emb = discord.Embed(title="Moderation", description="All moderation commands goes here", colour = 0xff4444)
    emb.add_field(name="**Ban**", value = "Bans a user from guild \nUsage --> `=ban <user>`", inline=False)
    emb.add_field(name="**Clear**", value = "Clears specified number of messages in a text channel /[Default Value = 1] \nUsage --> `=clear [number of messages]`", inline=False)
    emb.add_field(name="**Kick**", value = "Kick a user from guild \nUsage --> `=kick <user>`", inline=False)
    emb.add_field(name="**Lock**", value = "Locks a channel to stop sending messages in it /[Default Value = Current Channel] \nUsage --> `=lock [channel]`", inline=False)
    emb.add_field(name="**Mute**", value = "Mutes a user to stop sending messages in guild\nUsage --> `=mute <user>`", inline=False)
    emb.add_field(name="**Unban**", value = "Unbans a user from guild \nUsage --> `=unban <user>`", inline=False)
    emb.add_field(name="**Unlock**", value = "Unlocks a locked channel /[Default Value = Current Channel] \nUsage --> `=unlock [channel]`", inline=False)
    emb.add_field(name="**Unmute**", value = "Unmutes a muted user\nUsage --> `=unmute <user>`", inline=False)

    await ctx.send(embed=emb)

@help.command()
async def fun(ctx):
   
    emb = discord.Embed(title="Fun", description="Fun commands goes here", colour = 0xff4444)
    emb.add_field(name="**8ball**", value = "Ask the magic 8ball about your future!\nUsage --> `=8ball <question>`\nAliases --> ques, yn, ask", inline=False)
    emb.add_field(name="**Embed**", value = "Makes an embed of your message. Seperate Title and Description with a ; \nUsage --> `=embed [title;description]`", inline=False)
    emb.add_field(name="**Kill**", value = "Makes an among us picture for you and your target. \nUsage --> `=kill <target>[killer]`", inline=False)
    emb.add_field(name="**Pan**", value = "Makes a PUBG picture for you and your target. \nUsage --> `=pan <target>[killer]`", inline=False)
    emb.add_field(name="**Quote**", value = "Returns an random quote to motivate you. \nUsage --> `=quote`", inline=False)
    emb.add_field(name="**WhoAreYou**", value = "Gives you basic info about SABRE-Bot. \nUsage --> `=whoareyou`\nAliases --> wru", inline=False)

    await ctx.send(embed=emb)

@help.command(aliases=['utility'])
async def utilities(ctx):
    emb = discord.Embed(title="Utility", description="Utility commands goes here", colour = 0xff4444)
    emb.add_field(name="**Avatar**", value = "Gets the avatar of the target user / Default value = [command user]\nUsage --> `=avatar [user]`", inline=False)
    emb.add_field(name="**Createinv**", value = "Creates an invite of your server and sends it to target user. \nUsage --> `=createinv <user>`", inline=False)
    emb.add_field(name="**Embed**", value = "Makes an embed of your message. Seperate Title and Description with a ; \nUsage --> `=embed [title;description]`", inline=False)
    emb.add_field(name="**Heist**", value = "Makes a good looking Dank Memer Heist alert. \nUsage --> `=heist <host><amount>`", inline=False)
    emb.add_field(name="**Invite**", value = "Gives you link to invite the bot to your server. \nUsage --> `=invite`", inline=False)
    emb.add_field(name="**Ping**", value = "Returns you with the latency of bot. \nUsage --> `=ping`", inline=False)
    emb.add_field(name="**Serverlink**", value = "Post the server invite link in the invoking channel. \nUsage --> `=serverlink`", inline=False)
    emb.add_field(name="**Spotify**", value = "Shows info about the song that target is listening to on spotify. \nUsage --> `=spotify [user]`", inline=False)
    emb.add_field(name="**Timer**", value = "Starts a timer for you to remember the reason to start timer again. \nUsage --> `=timer <time in seconds>`", inline=False)
    emb.add_field(name="**Userinfo**", value = "Shows some basic info about the target user. \nUsage --> `=userinfo [user]`\nAliases --> ui", inline=False)

    await ctx.send(embed=emb)

@help.command(aliases=['game'])
async def games(ctx):
    emb = discord.Embed(title="Games", description="Game commands goes here", colour = 0xff4444)
    emb.add_field(name="**Guess**", value = "Guess the number between 1-50 which the bot has chosen in its mind \nUsage --> `=guess`", inline=False)
    emb.add_field(name="**Typerace**", value = "Type the phrases sent by bot as fast as possible. \nUsage --> `=typerace`", inline=False)

    await ctx.send(embed=emb)

@help.command(aliases=['eco'])
async def economy(ctx):
    emb = discord.Embed(title="Economy", description="Economy commands goes here", colour = 0xff4444)
    emb.add_field(name="**Balance**", value = "Shows the amount of SABRE-CASH in your wallet and bank \nUsage --> `=balance`\nAliases --> bal", inline=False)
    emb.add_field(name="**Beg**", value = "Beg to get some SABRE-CASH from people in the SABRE-WORLD. \nUsage --> `=beg`", inline=False)

    await ctx.send(embed=emb)

@help.command(aliases=['others'])
async def other(ctx):
    emb = discord.Embed(title="Other", description="Other commands goes here", colour = 0xff4444)
    emb.add_field(name="**Apply**", value = "Apply to become a mod in SABRE OFFICIAL. (Limited time only)(Check info in announcement channel) \nUsage --> `=apply`", inline=False)

    await ctx.send(embed=emb)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)

async def kick(ctx, member:discord.Member=None,*, reason="Reason not specified"):

    if member == None or member == ctx.message.author:
        await ctx.send("Idiot, you cannot kick yourself")

    server = ctx.message.guild

    embed3 = discord.Embed(
        title = "**Kick Alert**",
        description = (f"**Alert** : {member.name} has been kicked from this server by {ctx.author.mention}!")
    )

    embed3.add_field(name="**Reason for Kick : **", value=f"{reason}")
    await member.kick(reason=reason)
    await ctx.send(embed=embed3)
    

@kick.error
async def kick_error(ctx, error):
    if isinstance (error, commands.MissingPermissions):
        await ctx.send("🛑 You dont have Administrative Permissions, so you can't use that")


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member:discord.Member=None,*, reason="Reason Not Specified"):
    if member == None or member == ctx.message.author:
        await ctx.send("Idiot, you cannot ban yourself")
    
    server = ctx.message.guild

    embed4 = discord.Embed(
        title = "**Ban Alert**",
        description = (f"**Alert** : {member.name} has been banned from this server by {ctx.author.mention}!")
    )

    embed4.add_field(name="**Reason for Ban : **", value=f"{reason}")
    await member.ban(reason=reason)
    await ctx.send(embed=embed4)
    

@ban.error
async def ban_error(ctx, error):
    if isinstance (error, commands.MissingPermissions):
        await ctx.send("🛑 You dont have Administrative Permissions, so you can't use that")
    
    
@client.command()
async def unban(ctx,*, member):
    
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed5=discord.Embed(
    title = "**Unban Alert**",
    description = f"**Alert** : {user.name} has been unbanned from this server by {ctx.author.mention}!"
    )
    embed5.set_thumbnail(url="https://zeevector.com/wp-content/uploads/Clipart/Welcome-hand-Clipart.png")   
    await ctx.send(embed=embed5)



@unban.error
async def unban_error(ctx, error):
    if isinstance (error, commands.MissingPermissions):
        await ctx.send("🛑 You dont have Administrative Permissions, so you can't use that")


def check(message):
    try:
        int(message.content)
        return True
    except ValueError:
        return False


@client.command()
async def guess(ctx):
    number = random.randint(1,50)
    print(number)

    await ctx.send("I am picking a number in my mind, between 1-50")
    await asyncio.sleep(1)
    await ctx.send("Guess the number by typing the number in the chat. You will get only 5 chances or you are out")
        
    for chnc in range(1,6):
        msg = await client.wait_for('message', check = check)
        
        uguess = int(msg.content)

        if uguess > number:
            await ctx.send("Wrong guess {.author.mention}".format(msg))
            await asyncio.sleep(1)
            await ctx.send((str(chnc)) + " chances used. You have 5 in total")
            await asyncio.sleep(1)
            await ctx.send("Try Going Lower")

        elif uguess < number:
            await ctx.send("Wrong guess {.author.mention}".format(msg))
            await asyncio.sleep(1)
            await ctx.send(str(chnc) + " chances used. You have 5 in total")
            await asyncio.sleep(1)
            await ctx.send("Try Going Higher")

        else:
            await ctx.send("Congo {.author.mention}. Your guess was {}, which was correct answer".format(msg, number))
            break

    else:
        await ctx.send("Bad Luck, {.author.mention}. The answer was {}. Better Luck Next Time".format(msg, number))


@client.command(aliases=["chup"])
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member):
    if member == None:
        await ctx.send("Idiot, you cannot mute yourself")
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="Muted", permissions=perms)
        await member.add_roles(role)
        await ctx.send(f"{member} was muted successfully")
    else:
        await member.add_roles(role) 
        await ctx.send(f"{member} was muted successfully")

@client.command()
@commands.has_permissions(administrator = True)
async def unmute(ctx, member:discord.Member=None):
    if member == None:
        ctx.send("Idiot, you can't mute yourself")
        
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)
    await ctx.send(f"{member} unmuted successfully")

@client.command()
@commands.has_permissions(create_instant_invite=True)
async def myinv(ctx, user:discord.Member=None):
    if user == None:
        user = ctx.author
    myser = client.get_guild(544450528516767764)
    chan1= myser.channels[0]
    invite = await chan1.create_invite(unique=True, max_use=1)
    try:
        await user.send(f"Here's your invite to SABRE BOT support cum my creator's fun server : \n{invite}")
        await ctx.send(f"Invite sent to {user}")
    except:
        await ctx.send("Cant send. Maybe DMs are off")

@client.command()
@commands.has_permissions(create_instant_invite=True)
async def createinv(ctx, user:discord.Member=None):
    if user == None:
        user = ctx.author
    guildc = ctx.guild
    try:
        channelc = guildc.channels[0]
        invite = await channelc.create_invite(unique=True, max_use=1)
    except:
        channelc = guildc.channels[1]
        invite = await channelc.create_invite(unique=True, max_use=1)
    try:
        await user.send(f"Here's your invite: {invite}")
        await ctx.send(f"Invite of {guildc.name} sent to {user}")
    except:
        await ctx.send("Cant send. Maybe DMs are off")


@client.command(aliases=['serverinvite', 'invitelink'])
async def serverlink(ctx):
    guild = ctx.guild
    channel = guild.channels[0]
    invitelink = await channel.create_invite(max_uses=1, unique=True)
    await ctx.send(f"Here is an invite link for the server {guild.name}: {invitelink}")


@client.command()
async def kill(ctx, user2:discord.Member, user1:discord.Member=None):
    if user1 == None:
        user1 = ctx.author


    amkill = Image.open(r"amonguskill.jpg")    

    asset1 = user1.avatar_url_as(size=128)
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((83,83))

    asset2 = user2.avatar_url_as(size=128)
    data2 = BytesIO(await asset2.read())
    pfp2 = Image.open(data2)
    pfp2 = pfp2.resize((83,83))

    amkill.paste(pfp1, (510,333))
    amkill.paste(pfp2, (670,329))

    amkill.save("amkilljpg.jpg")

    await ctx.send(file=discord.File("amkilljpg.jpg"))


@client.command()
async def pan(ctx, user2:discord.Member, user1:discord.Member=None):
    if user1 == None:
        user1 = ctx.author


    panp = Image.open(r"pankill.jpg")    

    asset1 = user1.avatar_url_as(size=128)
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((134,134))

    asset2 = user2.avatar_url_as(size=128)
    data2 = BytesIO(await asset2.read())
    pfp2 = Image.open(data2)
    pfp2 = pfp2.resize((156,156))

    panp.paste(pfp1, (681,107))
    panp.paste(pfp2, (1058,253))

    panp.save("pankilljpg.jpg")

    await ctx.send(file=discord.File("pankilljpg.jpg"))

@client.command(aliases=["photo", "pic"])
async def picture(ctx , link):
    embd = discord.Embed(title = f"Photo requested by {ctx.author.name}")
    embd.set_image(url = link)
    embd.set_thumbnail(url = link)
    await ctx.send(embed=embd)

@client.command(aliases=["typerace"])
async def type(ctx):
    starttime = time.time()
    phrases = ['SABRE Bot the best', 'Grand Theft Auto San Andreas', 'Bro I want 10 bucks', 'Hey bro lets go party']
    answer = random.choice(phrases)
    timer = 10.0
    await ctx.send(f"You have {timer} seconds to type: {answer}")

    def is_correct(msg):
        return msg.author==ctx.author

    try:
        guess = await client.wait_for('message', check=is_correct, timeout=timer)
    except asyncio.TimeoutError:
        return await ctx.send("Time's Up")

    if guess.content == answer:
        await ctx.send("You got it!")
        fintime = time.time()
        total = fintime - starttime
        await ctx.send(f"{round(total)} seconds")

    else:
        await ctx.send("Nope, that wasn't really right")

@client.command()
async def timer(ctx, seconds, *, reason=None):
    if reason == None:
        reason = "Not Provided"
    
    try:
        
        fiembed = discord.Embed(title=f"Timer of {seconds}s by {ctx.author} \nReason: __{reason}__", description=f"**{seconds}**")
        
        
        secondint = int(seconds)
        if secondint > 500:
            await ctx.send("Time should be under 500 seconds")
            raise BaseException
        if secondint <= 0:
            await ctx.send("Time should not be negative")
            raise BaseException
        message = await ctx.send(embed=fiembed)
        while True:
            secondint -= 1
            etembed = discord.Embed(title=f"Timer of {seconds}s by {ctx.author} \nReason: __{reason}__", description=f"**{secondint}**")
            if secondint == 0:
                endembed = discord.Embed(title=f"Timer of {seconds}s by {ctx.author} \nReason: __{reason}__", description=f"**Timer Ended**", colour = 0xff4444)
                
                await message.edit(embed=endembed)
                break
            await message.edit(embed=etembed)
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")


@client.command()
async def heist(ctx, host:discord.Member=None, *, amt=None):
    if host == None:
        await ctx.send("Please specify the heist sponser")
    if amt == None:
        await ctx.send("Please specify the heist amount")
    #if amt < 1000:
    #    await ctx.send("Amount cannot be under 1000")

    embed = discord.Embed(title="Get ready for heist", description="Heist is starting in some time. Please show your presence by reacting to ✅ below", colour= 0xaa42f5)
    embed.add_field(name=f"**Heist on:-**", value=f"{host.mention}", inline=False)
    embed.add_field(name=f"**Amount:-**", value=f"{amt}", inline=False)
    embed.add_field(name="**Important things to note**", value="Keep 1000 coins in your wallet ready \nBuy a lifesaver if you dont have one to avoid losing coins on death \nWhen the channel unlocks, type `Join Heist`, but dont spam please", inline=False)
    embed.set_footer(text=f"Go thank {host} in chat for this heist")
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.message.delete()
    if ctx.guild == client.get_guild(798181625640386600):
        msg1 = await ctx.send(content=discord.utils.get(ctx.guild.roles, name="Heist-Ping").mention, embed=embed)
        await msg1.add_reaction("✅")
        return
    elif ctx.guild == client.get_guild(812073707756584990):
        msg2 = await ctx.send(content=discord.utils.get(ctx.guild.roles, name="Heist Ping").mention, embed=embed)
        return
    msg = await ctx.send(content="No ping role set. Anyways Lets Goooo", embed=embed)
    await msg.add_reaction("✅")

@client.command()
async def spotify(ctx, user: discord.Member = None):
    user = user or ctx.author
    spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if not spot:
        embed2 = discord.Embed(title="User not listening to spotify", description="The target user is either not listening to spotify, or is offline or invisible", color=0x42f575)
        await ctx.send(embed=embed2)
        return
    embed = discord.Embed(title=f"{user.name}'s Spotify", color=0x42f575)
    embed.add_field(name="Song", value=spot.title, inline=False)
    embed.add_field(name="Artist", value=spot.artist, inline=False)
    embed.add_field(name="Album", value=spot.album, inline=False)
    embed.add_field(name="Track Link", value=f"[{spot.title}](https://open.spotify.com/track/{spot.track_id})")
    embed.set_thumbnail(url=spot.album_cover_url)
    await ctx.send(embed=embed)


@client.command()
@commands.check(check_stg)
async def massping(ctx, user:discord.Member=None):
    if user == None:
        await ctx.send("Mention a user please")
    for x in range(10):
        await ctx.send(f"Hello {user.mention}")



@client.command(name='apply', help='Apply for staff!')
@commands.has_role('MODAPP')
async def apply(ctx):
    role = discord.utils.get(ctx.guild.roles, id=814072320187957248)
    if ctx.channel.id == 814065318829096980:
        pass
    else:
        return
    questions = [
        "Why do you want to be a staff member?",
        "Why do you think we should recruit you as a staff member?",
        "What is your level in the server? (Do `>rank` in <#727853962279256086>)",
        "How much experience do you have had a staff member in other servers? `Please give an honest answer, we may ask for proof anytime!`",
        "What should you do when someone is caught DM-Advertising? (They don't have any previous warnings.)",
        "What should you do when someone starts spamming in channel other than <#728892504690393141>? (They don't have any previous warnings.)",
        "What should you do when someone starts abusing repeatedly in the chat?",
        "What should you do when someone posts an NSFW media in the chat?",
        "What should you do when someone argues with you in your DMs regarding a punishment they recieved?",
        "What should you do when an another staff member mocks your skills?",
        "Have you taken all the self roles present in the server?(Yes/No) `If its a no, then remember that you will get all the self roles if you become a mod`"
    ]

    answers = []

    try:
        _ = await ctx.author.send(f"✅ | Staff Applications for **SABRE OFFICIAL**")
        await ctx.send("✅ Aight! Check your DMs")

    except:
        await ctx.send(f'❎ Unable to send a DM message to you, make sure to open your DMs.')

    def check(m):
        return m.author == ctx.author and m.channel == _.channel

    for x in questions:
        await ctx.author.send(embed=discord.Embed(description=f'❓ | {x}', color=randint(0x000000, 0xFFFFFF)))

        try:
            msg = await client.wait_for('message', check=check, timeout=600)

            if msg.content == "cancel":
                await ctx.author.send(f'✅ | Alright, cancelled the applications!')

                break

            else:
                answers.append(msg.content)

        except TimeoutError:
            return await ctx.author.send(f'❎ You didn\'t respond in time!')

    channel = client.get_channel(814056538879557702)

    try:

        embed = discord.Embed(
            title='New Application Recorded!',
            description=f'**Candidate:** {ctx.author} (ID: {ctx.author.id})',
            color=randint(0x000000, 0xFFFFFF)
        )

        for i in range(11):
            embed.add_field(
                name=f'#{i+11} | {questions[i]}', value=f'```\n{answers[i]}\n```', inline=False)
        await channel.send(content="<@!423008899302424596>", embed=embed)

        await ctx.author.send(f'✅ Your responses have been recorded! Thank you for applying!')
        await ctx.author.remove_roles(role)

    except IndexError:
        return

@client.command()
async def quote(ctx):
    headers={"Accept":"application/json"}
    r = requests.get("https://api.quotable.io/random", headers=headers)
    data=r.json()
    embed = discord.Embed(title=data['content'], description="- " + data['author'])
    await ctx.send(embed=embed)

@client.event
async def on_member_join(member):
    if not member.guild.id == 544450528516767764:
        print(f'guild was not sabre, it was {member.guild}')
        return
    embed = discord.Embed(title=f"Welcome {member.name}", description=f"Welcome to SABRE OFFICIAL, {member.mention}.\nMake sure to take roles from <#752467757123108894> to see more channels according to your interests.\nFollow all the rules mentioned in <#777751091047038976>\n\nBy the way you are our {member.guild.member_count} member")
    embed.set_footer(text="ENJOY")
    channel = client.get_channel(544450528516767766)
    await channel.send(content=f"{member.mention}", embed=embed)

@client.event
async def on_guild_join(guild):
    if not guild.id == 544450528516767764:
        print(f"joined {guild.name}. Leaving rn")
        try:
            await guild.text_channels[0].send("I am leaving this server because me and my website are under development and my owner dont want any problems. Dont worry this bot will be available for everyone soon.")
            await guild.leave()
        except:
            await guild.owner.send("I am leaving this server because me and my website are under development and my owner dont want any problems. Dont worry this bot will be available for everyone soon.")
            await guild.leave()

"""################-----------------------ECOBOT CODE STARTS-----------------------------------------------------############
"""

@client.command(aliases=["bal"])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data(user)

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    bb = discord.Embed(title = f"{ctx.author.name}'s balance", colour=ctx.author.color)
    bb.add_field(name="**Wallet:**", value=wallet_amt)
    bb.add_field(name="**Bank:**", value=bank_amt)
    await ctx.send(embed=bb)



@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data(user)
    earnings = random.randrange(150)
    givernames = ["Joe Biden", "Dank Memer Bot", "Akshay Kumar", "Amit Shah", "CarryMinati", "SoulMortal", "Scout", "Narendra Modi", ""]
    giver = random.choice(givernames)
    if earnings > 75:
        await ctx.send(f"OMG!, {ctx.author.mention}. **{giver}** gave you freakin' **{earnings}** SABRE-CASH!! May God Bless Them.")
    if earnings < 75:
        await ctx.send(f"Eh!, {ctx.author.mention}. **{giver}** gave you only **{earnings}** SABRE-CASH! Who gives that less amount of money?")

    if earnings == 0:
        await ctx.send(f"LOL!, {ctx.author.mention}. **{giver}** gave you **nothing** and said that you should earn at your own. BEIZZATI OP.")
    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

async def open_account(user):
    users = await get_bank_data(user)

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True

async def get_bank_data(user):
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

client.loop.create_task(ch_pr())


client.run(TOKEN)
