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
    guild = bot.guilds[0]
    await update_diff_channel(channel1)
    await update_height_channel(channel2)
    await update_hash_channel(channel3)
    await update_supply_channel(channel4)
    await update_member_channel(channel5)
    await shut_down()
async def shut_down():
    print("Shutting down...")
    await bot.close()
async def update_member_channel(channel5):
    guild = bot.guilds[0]
    channel = guild.get_channel(channel5)
    member_count = guild.member_count
    bot_count = bot_count = sum(member.bot for member in guild.members)
    print(f"Anzahl der Mitglieder auf dem Server: {member_count}")
    await channel.edit(name="Member: " + str(member_count-bot_count))

async def update_diff_channel(channel1):
    guild = bot.guilds[0]
    channel = guild.get_channel(channel1)
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
        await channel.edit(name="Difficulty: " + str(new_name) + "K")
    else:
        new_name = round(new_name / pow(10, 3), 2)
        await channel.edit(name="Difficulty: " + str(new_name) + "M")
    print(f"Difficulty channel name updated to: {new_name}")


async def update_height_channel(channel2):
    guild = bot.guilds[0]
    channel = guild.get_channel(channel2)
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
    await channel.edit(name="Height: " + new_name)
    print(f"Height channel name updated to: {new_name}")

async def update_hash_channel(channel3):
    guild = bot.guilds[0]
    channel = guild.get_channel(channel3)
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
        await channel.edit(name="Hashrate: " + str(new_name) + " GH/s")
    elif new_name < 999999:
        new_name = round(new_name / pow(10, 3), 1)
        await channel.edit(name="Hashrate: " + str(new_name) + " TH/s")
    else:
        new_name = round(new_name / pow(10, 6), 1)
        await channel.edit(name="Hashrate: " + str(new_name) + " PH/s")
        print(f"Hash channel name updated to: {new_name}")


async def update_supply_channel(channel4):
    guild = bot.guilds[0]
    channel = guild.get_channel(channel4)
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
    await channel.edit(name="Supply: " + str(new_name) + "K PLM")
    print(f"Supply channel name updated to: {new_name}")


async def stop_update(ctx):
    update_hash_channel.stop()
    update_height_channel.stop()
    update_diff_channel.stop()
    update_supply_channel.stop()
    await ctx.send("Updating channel names stopped!")

bot.run(DISCORD_TOKEN)
