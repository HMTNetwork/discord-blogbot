import discord
import os
import datetime
from discord import app_commands
from dotenv import load_dotenv

# --- UMWELTVARIABLEN LADEN ---
load_dotenv()

# --- KONFIGURATION AUS .ENV ---
# Wir nutzen int(), da IDs in discord.py Zahlen sein müssen
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))
ROLE_TO_PING_ID = int(os.getenv('ROLE_TO_PING_ID'))
WRITER_ROLE_ID = int(os.getenv('WRITER_ROLE_ID'))

# --- BOT SETUP ---


class BlogBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Synchronisierung für den spezifischen Server
        my_guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=my_guild)
        await self.tree.sync(guild=my_guild)


client = BlogBot()

# --- SLASH COMMAND: /new-blog ---


@client.tree.command(
    name="new-blog",
    description="Veröffentlicht einen neuen Blog-Beitrag."
)
@app_commands.describe(
    titel="Der Titel des Blogeintrags",
    link="Der Link zum Beitrag"
)
@app_commands.checks.has_role(WRITER_ROLE_ID)
async def new_blog(interaction: discord.Interaction, titel: str, link: str):

    channel = client.get_channel(TARGET_CHANNEL_ID)

    if channel is None:
        await interaction.response.send_message("Fehler: Ziel-Channel wurde nicht gefunden.", ephemeral=True)
        return

    # Embed Design
    embed = discord.Embed(
        description=f"# **[{titel}]({link})**",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )

    role_ping = f"<@&{ROLE_TO_PING_ID}>"

    try:
        await channel.send(content=role_ping, embed=embed)
        await interaction.response.send_message("✅ Blog-Post erfolgreich veröffentlicht!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Fehler beim Senden: {e}", ephemeral=True)

# --- FEHLERBEHANDLUNG ---


@new_blog.error
async def new_blog_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(
            f"❌ Keine Berechtigung: Du benötigst die Rolle <@&{WRITER_ROLE_ID}>.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {error}", ephemeral=True)

# --- START EVENT ---


@client.event
async def on_ready():
    print(f'--- Bot online ---')
    print(f'Eingeloggt als: {client.user}')
    print(f'Konfiguration geladen für Guild: {GUILD_ID}')
    print('------------------')

# --- BOT STARTEN ---
if TOKEN:
    client.run(TOKEN)
else:
    print("FEHLER: Kein DISCORD_TOKEN in der .env gefunden!")
