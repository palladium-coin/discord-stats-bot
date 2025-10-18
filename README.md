## Palladium Stats Discord Bot

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![discord.py Version](https://img.shields.io/badge/discord.py-2.3.2-7289DA.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A versatile Discord bot designed to display real-time statistics from a Palladium Core (`palladiumd`) node directly on your Discord server. The bot automatically updates channel names with key network data and provides useful slash commands for users to interact with the blockchain.



## Features

- **Live Channel Stats:** Automatically updates the names of designated channels every 10 minutes to show:
  - Current Block Height
  - Network Hashrate
  - Difficulty
  - Total Coin Supply (Calculated with halvings)
  - Member Count (Based on a specific role)
- **Slash Commands:** Interactive commands for all server members:
  - `/balance [address]`: Checks the balance of any PLM address.
  - `/peers`: Shows the number of peers the node is connected to.
- **Robust RPC Connection:** Creates a new, fresh connection for every task, preventing crashes due to stale or timed-out connections.
- **Easy Configuration:** All settings (Tokens, IDs, RPC details) are grouped at the top of the script.

---

## Requirements

Before you begin, ensure you have the following:

- A server running **Ubuntu/Debian** (though other Linux distros will work).
- **Python 3.8** or newer.
- A running and fully synchronized **`palladiumd`** node on the same server.
- Your `palladium.conf` file must include `server=1` and `txindex=1` for all features to work.
- A **Discord Bot Application** with a Token.

---

## Installation & Setup

### Step 1: Clone the Repository
```bash
git clone [https://github.com/palladium-coin/discord-stats-bot.git](https://github.com/palladium-coin/discord-stats-bot.git)
cd discord-stats-bot
````

### Step 2: Create Virtual Environment & Install Dependencies

Using a virtual environment (`venv`) is highly recommended to avoid conflicts.

```bash
# Install venv package if you don't have it
sudo apt install python3-venv

# Create a virtual environment
python3 -m venv bot-env

# Activate the environment
source bot-env/bin/activate

# Install required Python libraries
pip install discord.py python-bitcoinrpc
```

*(You will now see `(bot-env)` at the start of your terminal prompt.)*

### Step 3: Configure the Bot

Open `main.py` with a text editor (e.g., `nano main.py`) and fill in your details in the `--- CONFIGURATION ---` section at the top.

  - `DISCORD_TOKEN`: Your bot's secret token.
  - `GUILD_ID`: The ID of your Discord server (Right-click server icon -\> Copy Server ID).
  - `CHANNEL_IDS`: The IDs for each channel the bot should update (Right-click channel -\> Copy Channel ID).
  - `MEMBER_ROLE_NAME`: The *exact* name of the role for the member counter (e.g., "Member").
  - `RPC_USER` & `RPC_PASSWORD`: Your RPC credentials from your `palladium.conf` file.

### Step 4: Invite the Bot to Your Server

You must use a correctly scoped URL to invite your bot.

1.  Go to the Discord Developer Portal ⟶ **OAuth2** ⟶ **URL Generator**.
2.  Select the scopes **`bot`** AND **`applications.commands`**.
3.  In the "Bot Permissions" box that appears, select **`Manage Channels`** (and `Manage Roles` if you use it for role-based features).
4.  Copy the generated URL and paste it into your browser to invite the bot to your server.

-----

## Running the Bot

You can run the bot manually for testing, but running it as a `systemd` service is the recommended way for it to run 24/7.

### A) For Testing (Manual)

Inside your activated `venv`, just run the script:

```bash
python3 main.py
```

*(Press `CTRL+C` to stop. Leave the venv with `deactivate`.)*

### B) As a System Service (Recommended for 24/7)

This will make your bot automatically start on server boot and restart if it crashes.

**1. Create the Service File:**

```bash
sudo nano /etc/systemd/system/palladium-bot.service
```

**2. Paste the following content.** (Assuming your project is at `/home/arian/discord-stats-bot`. **Adjust the paths if yours are different\!**)

```ini
[Unit]
Description=Palladium Discord Bot
After=network.target palladiumd.service

[Service]
# Replace 'username' with your actual username
User=username
Group=username

# Path to your project directory
WorkingDirectory=/home/username/discord-stats-bot

# Command to start the bot using the venv's python
ExecStart=/home/username/discord-stats-bot/bot-env/bin/python3 /home/username/discord-stats-bot/main.py

# Restart policy
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**3. Enable and Start the Service:**

```bash
# Reload systemd to read the new file
sudo systemctl daemon-reload

# Enable the bot to start on boot
sudo systemctl enable palladium-bot.service

# Start the bot right now
sudo systemctl start palladium-bot.service
```

**4. Check the Status/Logs:**

```bash
# Check if it's "active (running)"
sudo systemctl status palladium-bot.service

# View the live logs
sudo journalctl -u palladium-bot.service -f
```