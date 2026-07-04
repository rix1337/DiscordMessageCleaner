#  DiscordMessageCleaner

[![PyPI version](https://badge.fury.io/py/discord-message-cleaner.svg)](https://badge.fury.io/py/discord-message-cleaner)
[![GitHub Sponsorship](https://img.shields.io/badge/support-me-red.svg)](https://github.com/users/rix1337/sponsorship)

Cleans messages from a Discord channel and its threads when they are older than a set time in days.
Threads left empty after cleanup are deleted.

# Setup

`pip install discord-message-cleaner`

## 🚀 Setting Up & Inviting DeleteBot

1. **Create a Discord Application**  
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).  
   - Click **New Application**, give it a name (e.g. “DeleteBot”), and save.

2. **Add a Bot User**  
   - In your application sidebar, select **Bot** → **Add Bot** → **Yes, do it**.  
   - Under **Privileged Gateway Intents**, enable **Message Content Intent**.  

3. **Generate an Invite Link**  
   - In the sidebar, go to **OAuth2** → **URL Generator**.  
   - Under **Scopes**, check: `bot`  
   - Under **Bot Permissions**, check at minimum:  
     - **Read Message History**  
     - **Manage Messages**  
     - **Manage Threads** (required to delete empty threads and access archived private threads)
   - Copy the generated URL at the bottom.

4. **Invite to Your Server**  
   - Paste the URL into your browser, select your server, and authorize.

# Run

```
discord_message_cleaner
  --token=<your_discord_bot_token>
  --channel_id=<your_discord_channel_id>
  --days=<number_of_days>
  ```

# Docker
```
docker run -d \
  --name="DiscordMessageCleaner" \
  -e 'TOKEN=<your_discord_bot_token>'
  -e 'CHANNEL_ID=<your_discord_channel_id>'
  -e 'DAYS=<number_of_days>'
  rix1337/docker-discord-message-cleaner:latest
  ```
