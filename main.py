import discord
import os
import datetime
from discord import app_commands
from dotenv import load_dotenv

# --- UMWELTVARIABLEN LADEN ---
load_dotenv()

# --- KONFIGURATION ---
# Deine IDs aus der Anfrage
GUILD_ID = 1315414448244002846
TARGET_CHANNEL_ID = 1451309192265601127
ROLE_ID = 1451309602259079410

# Token aus der .env Datei
TOKEN = os.getenv('DISCORD_TOKEN')

# --- BOT SETUP ---


class BlogBot(discord.Client):
    def __init__(self):
        # Intents: Guilds ist für Server-Interaktionen nötig
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        # CommandTree für Slash-Commands
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Synchronisiert die Befehle direkt mit deinem Server (schneller als global)
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
async def new_blog(interaction: discord.Interaction, titel: str, link: str):

    # Den Ziel-Channel anhand der ID suchen
    channel = client.get_channel(TARGET_CHANNEL_ID)

    if channel is None:
        await interaction.response.send_message(
            "Fehler: Der Ziel-Channel wurde nicht gefunden.",
            ephemeral=True
        )
        return

    # --- EMBED DESIGN ---
    # Wir nutzen kein 'title'-Feld, da dort kein '#' (Header) funktioniert.
    # Stattdessen nutzen wir die 'description' für große, fette Schrift mit Link.
    embed = discord.Embed(
        description=f"# **[{titel}]({link})**",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )

    # Die Rolle für den Ping (Format: <@&ID>)
    role_ping = f"<@&{ROLE_ID}>"

    try:
        # Nachricht senden (Ping-Text + Embed)
        await channel.send(content=role_ping, embed=embed)

        # Bestätigung nur für den ausführenden Admin sichtbar
        await interaction.response.send_message(
            "✅ Blog-Post wurde erfolgreich veröffentlicht!",
            ephemeral=True
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Fehler: Fehlende Berechtigungen im Ziel-Channel.",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Ein Fehler ist aufgetreten: {e}",
            ephemeral=True
        )

# --- START EVENT ---


@client.event
async def on_ready():
    print(f'--- Bot ist online ---')
    print(f'Eingeloggt als: {client.user}')
    print(f'Server-ID: {GUILD_ID}')
    print(f'Ziel-Channel: {TARGET_CHANNEL_ID}')
    print('-----------------------')

# --- BOT STARTEN ---
if TOKEN:
    client.run(TOKEN)
else:
    print("FEHLER: DISCORD_TOKEN wurde in der .env Datei nicht gefunden!")
