from setup import discord_client, discord_token
from message_handler import handle_message
from keep_alive import keep_alive
import os
import json

current_script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(current_script_directory, '..', '..'))
json_file_path = os.path.join(project_directory, 'botzilla/data/monsters.json')
json_file_path = os.path.abspath(json_file_path)

# Loads json file
with open(json_file_path, 'r') as file:
    original_json = json.load(file)

@discord_client.event
async def on_connect():
    print("Connected")

@discord_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord_client))

@discord_client.event
async def on_message(message):
    await handle_message(message, original_json)

discord_client.run(discord_token)
keep_alive()