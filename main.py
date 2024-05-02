import discord
import requests
from discord.ext import commands, tasks
import math
DISCORD_TOKEN = "YOUR TOKEN"
channel1 = CHANNELID
channel2 = CHANNELID
channel3 = CHANNELID
channel4 = CHANNELID
channel5 = CHANNELID
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
@bot.event
async def on_ready():
    await bot.tree.sync()
    update_channel.start()
@tasks.loop(minutes=30)
async def update_channel():
    await update_diff_channel(channel1)
    await update_height_channel(channel2)
    await update_hash_channel(channel3)
    await update_supply_channel(channel4)
    await update_member_channel(channel5)

@bot.hybrid_command()
async def get_diff(ctx: commands.Context):
    url = 'http://explorer.palladium-coin.com/api/getdifficulty'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = response.text

        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    await ctx.send(str(value))

@bot.hybrid_command()
async def ping(ctx: commands.Context):
    await ctx.send("pong")

@bot.hybrid_command()
async def get_balance(ctx: commands.Context, address: str):
    url = f'https://explorer.palladium-coin.com/ext/getbalance/{address}'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    checkerr = response.text[2:7]
    # Check if the request was successful
    if  not checkerr == "error" and response.status_code == 200:
        # Get the value from the response content
        value = float(response.text)
        # Output the value
        print("The Balance of", address, "is", value, "PLM!")
        await ctx.send("the balance of " + str(address) + " is " + "**" + str(value) + "**" + " PLM!")
    else:
        # Handle the case where the request failed
        print(address + " not valid or found!")
        await ctx.send(address + " **not** valid or found!")
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == MESSAGEID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if payload.emoji.name == '✅':
            role = discord.utils.get(guild.roles, name='Member')
            if role is not None:
                role = discord.utils.get(guild.roles, name='Member')
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                else:
                    print("member not found")
            else:
                print("role not found")
@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == MESSAGEID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if payload.emoji.name == '✅':
            role = discord.utils.get(guild.roles, name='Member')
            if role is not None:
                role = discord.utils.get(guild.roles, name='Member')
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                else:
                    print("member not found")
            else:
                print("role not found")
async def update_member_channel(channel):
    guild = bot.guilds[0]
    channelM = guild.get_channel(channel)
    member_count = guild.member_count
    bot_count = bot_count = sum(member.bot for member in guild.members)
    print(f"Anzahl der Mitglieder auf dem Server: {member_count}")
    await channelM.edit(name="Member: " + str(member_count-bot_count))
@bot.hybrid_command()
async def get_height(ctx: commands.Context):
    url = 'http://explorer.palladium-coin.com/api/getblockcount'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = response.text

        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    await ctx.send(str(value))
@bot.hybrid_command()
async def get_hashrate(ctx: commands.Context):
    url = 'http://explorer.palladium-coin.com/api/getnetworkhashps'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = float(response.text)

        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    value = round(value / pow(10, 9), 1)
    if value < 999:
        await ctx.send(str(value) + " GH/s")
    elif value < 999999:
        value = round(value / pow(10, 3), 1)
        await ctx.send(str(value) + " TH/s")
    else:
        value = round(value / pow(10, 6), 1)
        await ctx.send(str(value) + " PH/s")

@bot.hybrid_command()
async def get_supply(ctx: commands.Context):
    url = 'http://explorer.palladium-coin.com/api/getblockcount'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = float(response.text)
        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    value = (value * 50) / 1000
    await ctx.send(str(value) + "K PLM")
@bot.hybrid_command()
async def give_admin(ctx: commands.Context):
    member = ctx.author
    await member.kick(reason="Knecht haha")
    await ctx.send(f"{member.mention} wurde gekickt.")

async def update_diff_channel(channel):
    guild = bot.guilds[0]
    channelD = guild.get_channel(channel)
    url = 'http://explorer.palladium-coin.com/api/getdifficulty'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = response.text

        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    new_name = float(value)
    new_name = round(new_name / pow(10, 3), 2)
    if new_name <999:
        await channelD.edit(name="Difficulty: " + str(new_name) + "K")
    else:
        new_name = round(new_name / pow(10, 3), 2)
        await channelD.edit(name="Difficulty: " + str(new_name) + "M")
    print(f"Difficulty channel name updated to: {new_name}")

async def update_height_channel(channel):
    guild = bot.guilds[0]
    channelHe = guild.get_channel(channel)
    url = 'http://explorer.palladium-coin.com/api/getblockcount'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = response.text

        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    new_name = value
    await channelHe.edit(name="Height: " + new_name)
    print(f"Height channel name updated to: {new_name}")

async def update_hash_channel(channel):
    guild = bot.guilds[0]
    channelHa = guild.get_channel(channel)
    url = 'http://explorer.palladium-coin.com/api/getnetworkhashps'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = float(response.text)

        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    new_name = round(value / pow(10, 9), 1)
    if new_name < 999:
        await channelHa.edit(name="Hashrate: " + str(new_name) + " GH/s")
    elif new_name < 999999:
        new_name = round(new_name / pow(10, 3), 1)
        await channelHa.edit(name="Hashrate: " + str(new_name) + " TH/s")
    else:
        new_name = round(new_name / pow(10, 6), 1)
        await channelHa.edit(name="Hashrate: " + str(new_name) + " PH/s")
        print(f"Hash channel name updated to: {new_name}")

async def update_supply_channel(channel):
    guild = bot.guilds[0]
    channelS = guild.get_channel(channel)
    url = 'http://explorer.palladium-coin.com/api/getblockcount'  # Replace this URL with the actual URL you want to fetch the value from
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the value from the response content
        value = float(response.text)

        # Output the value
        print("The value is:", value)
    else:
        # Handle the case where the request failed
        print("Failed to fetch the value.")
    new_name = (value * 50) / 1000
    await channelS.edit(name="Supply: " + str(new_name) + "K PLM")
    print(f"Supply channel name updated to: {new_name}")

bot.run(DISCORD_TOKEN)
