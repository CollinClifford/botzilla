from setup import discord_client, discord_token
from message_handler import handle_message
from keep_alive import keep_alive
import os
import json
import discord

current_script_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_script_directory, '../data/monsters.json')


# Loads json file
with open(json_file_path, 'r') as file:
    original_json = json.load(file)

@discord_client.event
async def on_connect():
    print("Connected")

@discord_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord_client))
    # Set the bot's presence
    await discord_client.change_presence(activity=discord.Game(name="Fallout: New Tokyo"))

@discord_client.event
async def on_message(message):
    await handle_message(message, original_json)

keep_alive()
discord_client.run(discord_token)