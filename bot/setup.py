import discord
from decouple import config

discord_token = config('TOKEN')

# ----- discord ----- #
intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)