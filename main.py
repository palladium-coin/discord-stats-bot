import discord
import requests
from discord.ext import commands, tasks
import math
DISCORD_TOKEN = "Your Token here"
channel1 = ChannelID1
channel2 = ChannelID2
channel3 = ChannelID3
channel4 = ChannelID4
channel5 = ChannelID5
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
@bot.event
async def on_ready():
    await bot.tree.sync()
    await update_channel()
@tasks.loop(minutes = 30)
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
#    address = "plm1qxun2muvj5wh05um50ysslz4vg7pvvej5hwc8r9"
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
async def get_hash(ctx: commands.Context):
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
@bot.hybrid_command()
async def shut_down(ctx: commands.Context):
    member = ctx.author
    await ctx.send("Shutting down...")
    print("Bot wurde von "+ str(member)+" heruntergefahren")
    await bot.close()

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


async def stop_update(ctx):
    update_hash_channel.stop()
    update_height_channel.stop()
    update_diff_channel.stop()
    update_supply_channel.stop()
    await ctx.send("Updating channel names stopped!")

bot.run(DISCORD_TOKEN)
