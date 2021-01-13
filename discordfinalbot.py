import discord
from discord.ext import commands
import random
from random import choice
from random import randint
from random import randrange
import os
import asyncio
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io
from io import BytesIO
import json
import aiohttp
import http.client
import requests
import time


client = commands.Bot(command_prefix = '=')

client.remove_command("help")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        erem = discord.Embed(title = "Command Cooldown", description = "You cant use this command now. Try after %.2fs" % error.retry_after)
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
	
	statuses =["with your lives", f"on {len(client.guilds)} servers", f"a game in {len(client.guilds)} servers","with my creator, @SakshhamTheGamer","with Hamil's Phone lol", "Guess the Number game with my creator", "with fire", "songs for my creator" ]
	
	while not client.is_closed():
		
		status = random.choice(statuses)
		
		await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=status))
		
		await asyncio.sleep(3)


modlog = {}

@client.event
async def on_ready():
    global modlog
    try:
        with open('modlog.json') as f:
            audit = json.load(f)
    except:
        modlog = {}

    print("Bot is Ready")

@client.command()
async def status(ctx, member:discord.Member=None):
    if member == None:
        member = ctx.author
    await ctx.send(str(member.web_status))
#Answers with a random quote
#@client.command()
#async def quote(ctx):
#    responses = open('quotes.txt').read().splitlines()
#    random.seed(a=None)
#    response = random.choice(responses)
#    await ctx.send(response)


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
    
    
@client.command(aliases=['ques','yn'])
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
        description = '[Invite To Server](inviteURL) 👈 Click to invite this bot to your server',
    )
    await ctx.send(embed=embed2)



@client.command()
async def embed(ctx,*, message):
    embed=discord.Embed(title=message,colour=0xff4444)
    await ctx.channel.purge(limit=1)
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
    await ctx.channel.purge(limit=amount+1)
    await ctx.send('{} message(s) cleared by {}'.format(amount, ctx.author.mention), delete_after=3)
 
"""
@clear.error
async def clear_error(ctx, error):
    if isinstance (error, commands.MissingPermissions):
        await ctx.send("🛑 You dont have Administrative Permissions, so you can't use that")

@client.command()
async def setaudit(ctx, mlog:discord.TextChannel=None):
    if mlog == None:
        await ctx.send("Please type in the channel name")

    modlog[ctx.message.guild.id] = mlog.id

    await ctx.send(f"{mlog.mention} set to audit logging channel")
    
    with open('modlog.json', 'w+') as f:
        json.dump(modlog, f)

    
"""
# """@client.command(aliases=["game", "gamelist", "gameslist"])
# async def games(ctx):
# 	gembed = discord.Embed(colour=0x16e75a, title="Games List:-")
# 	gembed.add_field(name="**1. Guess The Number**", value="A game in which users have to guess the number randomly chosen by the bot. To start the game, type **=guess**. The bot will choose a random number and you have to guess it by typing the number in the chat.")
	
# 	await ctx.send(embed=gembed)
# """

# """@client.command(aliases=['commands'])
# async def cmds(ctx):
#     cembed = discord.Embed(colour=0xff2424)
#     cembed.add_field(name="**Ask**", value=f"Answers your questions with a yes, a no or a neutral response. \nUsage : =ask (Question) \nAliases : ques, yn")
#     cembed.add_field(name="**Avatar**", value=f"Shows avatar of the user mentioned. \nUsage : =avatar (mention user) ")
#     cembed.add_field(name="**Ban**", value=f"Bans a user from this server. \nUsage : =ban (user)")
#     cembed.add_field(name="**Clear**", value=f"Delete messages, media and embeds. \nUsage : =clear (number of messages to be deleted) \nAliases : purge, delete")
#     cembed.add_field(name="**Commands**", value=f"Shows available commands of this bot. \nUsage : =commands \nAliases : cmds")
#     cembed.add_field(name="**Embed**", value=f"Creates embed for a message you have typed. \nUsage : =embed (your message)")
#     cembed.add_field(name="**Invite**", value=f"Gives the invite of this bot to add it in your server. \nUsage : =invite")
#     cembed.add_field(name="**Kick**", value=f"Kicks a user from this server. \nUsage : =kick(user)")
#     cembed.add_field(name="**Ping**", value=f"Shows the latency of this bot. \nUsage : =ping")
#     cembed.add_field(name="**Unban**", value=f"Unbans a user from this server. \nUsage : =unban (username+usertag")
#     cembed.add_field(name="**UserInfo**", value=f"Shows information about a user. \nUsage : =userinfo (mention user) \nAliases : ui, uinfo, usin")
#     cembed.add_field(name="**WhoAreYou**", value=f"Shows information about this bot. \nUsage : =whoareyou \nAliases :wru, info, about")

#     await ctx.send(embed=cembed)
# """

"""@client.group(invoke_without_command=True)
async def help(ctx):

    ebd = discord.Embed(title = "Help", description = "Type `=help` <command name> to learn more about a command", colour = 0xff4444)

    ebd.add_field(name = "Moderation", value = "Ban, Clear, Kick, Unban,")
    ebd.add_field(name = "Fun", value = "Ask, Embed, Kill, Pan, WhoAreYou")
    ebd.add_field(name = "Helpful to Admins", value = "Avatar, Invite, Ping, Userinfo")
    ebd.add_field(name = "Games", value = "Guess")

    await ctx.send(embed=ebd)

@help.command()
async def ban(ctx):
    
    emb = discord.Embed(title="Ban", description="Bans a user from a guild", colour = 0xff4444)
    emb.add_field(name="**Syntax**", value = "=ban <user>")

    await ctx.send(embed=emb)

@help.command()
async def clear(ctx):
   
    emb = discord.Embed(title="Clear", description="Clears specified number of messages in a text channel /[Default Value = 1]", colour = 0xff4444)
    emb.add_field(name="**Syntax**", value = "=clear [number of messages]")

    await ctx.send(embed=emb)
"""
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)

async def kick(ctx, member:discord.Member=None,*, reason="Reason not specified"):

    if member == None or member == ctx.message.author:
        await ctx.send("Idiot, you cannot kick yourself")

#    with open("modlog.json", "r"):
#        modlog = json.load(f)

    server = ctx.message.guild

#    channel1 = modlog[server.id]

    

    embed3 = discord.Embed(
    	title = "**Kick Alert**",
    	description = (f"**Alert** : {member.name} has been kicked from this server by {ctx.author.mention}!")
    )

    embed3.add_field(name="**Reason for Kick : **", value=f"{reason}")

	#embed3.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWA13zKXnZYll0iloe2YRDtHcJVAUg-oB65L8TIGAhXULb9iqHdtB7v_P2&s=10")
    await member.kick(reason=reason)
    await channel1.send(embed=embed3)
	

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
#
#    channel1 = modlog[server.id]

    embed4 = discord.Embed(
    	title = "**Ban Alert**",
    	description = (f"**Alert** : {member.name} has been banned from this server by {ctx.author.mention}!")
    )

    embed4.add_field(name="**Reason for Ban : **", value=f"{reason}")
	#embed4.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWA13zKXnZYll0iloe2YRDtHcJVAUg-oB65L8TIGAhXULb9iqHdtB7v_P2&s=10")
    await member.ban(reason=reason)
    await channel1.send(embed=embed4)
	

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
async def createinv(ctx):
    guildc = ctx.guild
    channelc = guildc.channel[0]
    invite = await channelc.create_invite(unique=True, max_use=1)
    await ctx.send(f"Here's your invite: {invite}")

@client.command(aliases=['serverinvite', 'invitelink'])
async def serverlink(ctx):
    guild = ctx.guild
    channel = guild.channels[0]
    invitelink = await channel.create_invite(max_uses=1, unique=True)
    await ctx.author.send(f"Here is an invite link for the server {guild.name}: {invitelink}")


@client.command()
async def kill(ctx, user2:discord.Member, user1:discord.Member=None):
    if user1 == None:
        user1 = ctx.author


    amkill = Image.open("amonguskill.jpg")    

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


    panp = Image.open("pankill.jpg")    

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


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send("Hello. I am Sabre Bot. My preifx is `=`. Type `=cmds` for more info")

    await client.process_commands(message)


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
        
        fiembed = discord.Embed(title=f"Timer of {seconds}s by {ctx.author} \nReason:__{reason}__", description=f"**{seconds}**")
        
        
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
                endembed = discord.Embed(title=f"Timer of {seconds}s by {ctx.author} \nReason:__{reason}__", description=f"**Timer Ended**", colour = 0xff4444)
                
                await message.edit(embed=endembed)
                break
            await message.edit(embed=etembed)
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")

"""
@client.command(name='canvas')
async def canvas(ctx, text=None):
    #print('\n'.join(dir(ctx)))
    #print('\n'.join(dir(ctx.author)))

    # --- create empty image ---

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 300

    # create empty image 600x300 
    #image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT)) # RGB, RGBA (with alpha), L (grayscale), 1 (black & white)

    # --- load image from local file ---

    # or load existing image
    #image = Image.open('/home/furas/Obrazy/images/lenna.png')

    # --- load image from url ---

    import urllib.request    

    url = 'https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png?download'

    response = urllib.request.urlopen(url)
    image = Image.open(response)  # it doesn't need `io.Bytes` because it `response` has method `read()`
    print('size:', image.size)

    #IMAGE_WIDTH, IMAGE_HEIGHT = image.size
    IMAGE_WIDTH = image.size[0] 

    # --- draw on image ---

    # create object for drawing
    draw = ImageDraw.Draw(image)

    # draw red rectangle with green outline from point (50,50) to point (550,250) #(600-50, 300-50)
    draw.rectangle([50, 50, IMAGE_WIDTH-50, IMAGE_HEIGHT-50], fill=(255,0,0, 128), outline=(0,255,0))

    # draw text in center
    text = f'Hello {ctx.author.name}'

    font = ImageFont.truetype('C:\\Windows\\Fonts\\ariblk.ttf', 30)

    text_width, text_height = draw.textsize(text, font=font)
    x = (IMAGE_WIDTH - text_width)//2
    y = (IMAGE_HEIGHT - text_height)//2

    draw.text( (x, y), text, fill=(0,0,255), font=font)

    # --- avatar ---

    #print('avatar:', ctx.author.avatar_url)
    #print('avatar:', ctx.author.avatar_url_as(format='jpg'))
    #print('avatar:', ctx.author.avatar_url_as(format='png'))

    AVATAR_SIZE = 128

    # get URL to avatar
    # sometimes `size=` doesn't gives me image in expected size so later I use `resize()`
    avatar_asset = ctx.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)

    # read JPG from server to buffer (file-like object)
    buffer_avatar = io.BytesIO()
    await avatar_asset.save(buffer_avatar)
    buffer_avatar.seek(0)

    # read JPG from buffer to Image 
    avatar_image = Image.open(buffer_avatar)

    # resize it 
    avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) # 

    x = 50 + 5
    y = (IMAGE_HEIGHT-AVATAR_SIZE)//2  # center vertically
    image.paste(avatar_image, (x, y))

    # --- sending image ---

    # create buffer
    buffer_output = io.BytesIO()

    # save PNG in buffer
    image.save(buffer_output, format='PNG')    

    # move to beginning of buffer so `send()` it will read from beginning
    buffer_output.seek(0) 

    # send image
    await ctx.send(file=discord.File(buffer_output, 'myimage.png'))
############################
"""
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
        await ctx.send(f"LOL!, {ctx.author.mention}. **{giver}** gave you **nothing** by saying that you should earn at your own. What A Saying.")
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
