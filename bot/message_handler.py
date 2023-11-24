import random
from setup import discord_client
import re
import discord

async def handle_message(message, json_data):
    if message.author == discord_client.user:
        return

    # --- COMMANDS --- #

    if message.content.lower() == "$botzilla":
        random_monster = random.choice(json_data)
        response = discord.Embed(
            title=random_monster.get('name', ''),
            description=f"**Ability:** {random_monster.get('ability', 'Ability not available.')}\n"
                        f"**First Appearance:** {random_monster.get('firstAppearance', 'Year not available.')}",
            color=discord.Color.blue()
        )
        response.set_image(url=random_monster.get('img', ''))
        await message.channel.send(embed=response)
    elif message.content.lower() == "$botzilla list":
        monster_names = [monster.get('name', '') for monster in json_data]
        response = 'List of monsters:\n' + '\n'.join(monster_names)
        await message.channel.send(response)
    elif message.content.lower() == '$botzilla commands':
        response = 'List of commands:\nability\nlink\nyear\npicture'
        await message.channel.send(response)
    elif message.content.lower().startswith('$botzilla'):
        # Extract the monster name from the user's input
        match = re.match(r'\$botzilla\s+(\w+)', message.content, re.IGNORECASE)
        if match:
            monster_name = match.group(1).lower()

            # Find the specified monster in the JSON data
            monster_data = next((monster for monster in json_data if monster.get('name', '').lower() == monster_name), None)
            if monster_data:
                # Return all available information with an embedded image
                response = discord.Embed(
                    title=monster_data.get('name', ''),
                    description=f"**Ability:** {monster_data.get('ability', 'Ability not available.')}\n"
                                f"**First Appearance:** {monster_data.get('firstAppearance', 'Year not available.')}",
                    color=discord.Color.blue()
                )
                response.set_image(url=monster_data.get('img', ''))
            else:
                response = f'{monster_name.capitalize()} not found in the data.'
        else:
            response = 'Invalid usage of $botzilla command. Use $botzilla MonsterName.'

        await message.channel.send(embed=response)
