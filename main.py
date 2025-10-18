# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Palladium Stats Discord Bot
#
# A Discord bot that displays live network statistics from a palladiumd node
# in Discord channel names and provides blockchain info via slash commands.
#
# INSTRUCTIONS:
# 1. Fill in your details in the CONFIGURATION section below.
# 2. Install dependencies: pip install discord.py python-bitcoinrpc
# 3. Run the bot: python3 main.py
# -----------------------------------------------------------------------------

import discord
from discord.ext import commands, tasks
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import socket

# --- CONFIGURATION ---
# IMPORTANT: Fill in your own details below.

DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
GUILD_ID = 123456789012345678  # Right-click your server icon -> Copy Server ID

# --- CHANNEL IDs ---
# Right-click each channel -> Copy Channel ID
CHANNEL_IDS = {
    "difficulty": 123456789012345678,
    "height": 123456789012345678,
    "hashrate": 123456789012345678,
    "supply": 123456789012345678,
    "members": 123456789012345678,
}
MEMBER_ROLE_NAME = "Member"  # The exact, case-sensitive name of the role for the member counter

# --- PALLADIUM RPC CONFIGURATION ---
# These details must match your palladium.conf file
RPC_USER = "your_rpc_username"
RPC_PASSWORD = "your_rpc_password"
RPC_HOST = "127.0.0.1"  # Keep this unless the daemon runs on another machine
RPC_PORT = 2332

# --- BOT INITIALIZATION ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# --- HELPER FUNCTIONS ---

def get_rpc_connection():
    """
    Establishes a NEW, fresh RPC connection.
    Called for every task loop and command.
    """
    return AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}/", timeout=30)

def format_hashrate(hps: float) -> str:
    ghs = hps / 1e9
    if ghs < 1000:
        return f"{ghs:.2f} GH/s"
    ths = ghs / 1000
    if ths < 1000:
        return f"{ths:.2f} TH/s"
    phs = ths / 1000
    return f"{phs:.2f} PH/s"

def calculate_supply(height: int) -> float:
    total_supply = 0
    blocks_remaining = height
    reward = 50.0
    halving_interval = 21_000_000

    while blocks_remaining > 0:
        blocks_in_era = min(blocks_remaining, halving_interval)
        total_supply += blocks_in_era * reward
        blocks_remaining -= blocks_in_era
        reward /= 2
    return total_supply

# --- BOT EVENTS ---

@bot.event
async def on_ready():
    """Called when the bot is successfully connected to Discord."""
    try:
        # Test connection on startup
        get_rpc_connection().getblockcount()
        print("Successfully connected to the Palladium daemon.")
    except Exception as e:
        print(f"FATAL ERROR: Could not connect to Palladium daemon on startup. Check config/daemon. Details: {e}")
        # We don't exit here, the task will keep retrying.
    
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Successfully synced {len(synced)} command(s) for guild {GUILD_ID}.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    update_channels_task.start()

# --- BACKGROUND TASK ---

@tasks.loop(minutes=10)
async def update_channels_task():
    """Main task that runs every 10 minutes to update all stat channels."""
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print(f"Error: Could not find guild with ID {GUILD_ID}. Task will retry.")
        return

    print("Task started: Updating all channels...")
    try:
        # Establish a NEW connection every time
        rpc = get_rpc_connection()
        
        blockchain_info = rpc.getblockchaininfo()
        network_hash_ps = float(rpc.getnetworkhashps())
        height = blockchain_info['blocks']
        difficulty = float(blockchain_info['difficulty'])

        # Update each channel
        await update_channel(guild, "height", f"Height: {height:,} blocks")
        await update_channel(guild, "difficulty", f"Difficulty: {difficulty/1e6:.2f}M")
        await update_channel(guild, "hashrate", f"Hashrate: {format_hashrate(network_hash_ps)}")
        
        supply = calculate_supply(height)
        await update_channel(guild, "supply", f"Supply: {supply/1e6:.2f}M PLM")
        
        await update_member_count_channel(guild)

    except (JSONRPCException, socket.timeout, ConnectionRefusedError) as e:
        # Catches RPC errors, timeouts, or connection failures
        print(f"RPC Error during channel update: {e}")
    except Exception as e:
        # Catches all other errors (e.g., Discord API errors)
        print(f"An unexpected error occurred during channel update: {e}")
    print("Task finished.")

async def update_channel(guild: discord.Guild, key: str, name: str):
    """Generic function to update a channel's name."""
    channel_id = CHANNEL_IDS.get(key)
    if not channel_id: return
    
    channel = guild.get_channel(channel_id)
    if channel and channel.name != name:
        try:
            await channel.edit(name=name)
            print(f"Updated '{key}' channel to: {name}")
        except discord.Forbidden:
            print(f"Error: Missing permissions to edit the '{key}' channel.")
        except Exception as e:
            print(f"Error updating '{key}' channel: {e}")

async def update_member_count_channel(guild: discord.Guild):
    """Updates the member count channel based on a specific role."""
    channel_id = CHANNEL_IDS.get("members")
    if not channel_id: return

    channel = guild.get_channel(channel_id)
    if not channel: return

    member_role = discord.utils.get(guild.roles, name=MEMBER_ROLE_NAME)
    if not member_role:
        print(f"Error: Role '{MEMBER_ROLE_NAME}' not found!")
        if channel.name != "Members: ROLE NOT FOUND":
            await channel.edit(name="Members: ROLE NOT FOUND")
        return

    member_count = sum(1 for member in guild.members if member_role in member.roles)
    new_name = f"Members: {member_count}"
    if channel.name != new_name:
        await channel.edit(name=new_name)
        print(f"Updated member count to: {member_count}")


# --- SLASH COMMANDS ---

@bot.tree.command(name="balance", description="Checks the balance of a Palladium address.", guild=discord.Object(id=GUILD_ID))
async def balance(interaction: discord.Interaction, address: str):
    await interaction.response.defer() 
    try:
        # Establish a fresh connection for the command
        rpc = get_rpc_connection()
        result = rpc.scantxoutset("start", [f"addr({address})"])
        
        if result['success']:
            value = result['total_amount']
            embed = discord.Embed(title="💰 Balance Check", color=discord.Color.gold())
            embed.add_field(name="Address", value=f"`{address}`", inline=False)
            embed.add_field(name="Balance", value=f"**{value:,.8f} PLM**", inline=False)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"❌ The address `{address}` seems to be invalid.")
            
    except (JSONRPCException, ConnectionRefusedError):
        await interaction.followup.send(f"❌ The address `{address}` is not valid or was not found.")
    except Exception as e:
        await interaction.followup.send(f"An unexpected error occurred: {e}")

@bot.tree.command(name="peers", description="Shows the number of connected peers.", guild=discord.Object(id=GUILD_ID))
async def peers(interaction: discord.Interaction):
    try:
        # Establish a fresh connection for the command
        rpc = get_rpc_connection()
        peer_info = rpc.getpeerinfo()
        
        peer_count = len(peer_info)
        embed = discord.Embed(
            title="🌐 Network Connections",
            description=f"The node is currently connected to **{peer_count}** peers.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Error fetching peer information: {e}")


# --- START THE BOT ---
if __name__ == "__main__":
    if DISCORD_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE" or RPC_USER == "your_rpc_username":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: Please fill in your configuration details   !!!")
        print("!!! in the main.py file before running the bot.        !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        bot.run(DISCORD_TOKEN)