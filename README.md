# Discord Blog Bot

A Discord bot that allows authorized users to publish blog posts to a designated channel using a simple slash command.

## Features

- Publish blog posts directly from Discord using the `/new-blog` slash command
- Role-based access control (only users with the Writer role can publish)
- Automatic role pings when new blog posts are published
- Clean, embedded message formatting for blog posts
- Easy configuration through environment variables

## Prerequisites

- Python 3.8 or higher
- A Discord bot token
- A Discord server (guild) where you have administrative permissions

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/discord-blogbot.git
   cd discord-blogbot
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Discord bot:

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Navigate to the "Bot" section and create a bot
   - Copy the bot token

4. Configure the bot:
   - Copy `sample.env` to `.env`:
     ```bash
     cp sample.env .env
     ```
   - Edit `.env` and fill in your values:
     ```
     DISCORD_TOKEN=your_bot_token_here
     GUILD_ID=your_server_id
     TARGET_CHANNEL_ID=channel_id_for_blog_posts
     ROLE_TO_PING_ID=role_to_ping_when_posting
     WRITER_ROLE_ID=role_allowed_to_use_the_bot
     ```

## Configuration Guide

To get the required IDs from Discord:

1. **Enable Developer Mode** in Discord:

   - Settings → Advanced → Developer Mode

2. **Get your Server (Guild) ID**:

   - Right-click your server icon → Copy ID

3. **Get Channel ID**:

   - Right-click the channel where you want blog posts to appear → Copy ID

4. **Get Role IDs**:
   - Right-click roles → Copy ID
   - You need two roles:
     - Writer Role: Who can use the bot
     - Ping Role: Who gets notified of new posts

## Usage

1. Start the bot:

   ```bash
   python main.py
   ```

2. In Discord, use the slash command:
   ```
   /new-blog titel:"Your Blog Title" link:"https://yourblog.com/post"
   ```

Only users with the Writer role can use this command. When executed, the bot will:

- Post an embedded message in the target channel
- Ping the specified role to notify them of the new post
- Confirm success to the command user privately

## Permissions

The bot requires the following permissions:

- Read Messages/View Channels
- Send Messages
- Embed Links
- Use Slash Commands

## Dependencies

- **discord.py** - Discord API wrapper
- **python-dotenv** - Environment variable loader

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on the GitHub repository.
