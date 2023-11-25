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
        
        # Create an empty description string
        description = ""
        
            # Iterate through key/value pairs in the selected monster
        for key, value in random_monster.items():
        # Skip the 'Name' key in the dynamic description
            if key.lower() != 'name':
                description += f"**{key.capitalize()}:** {value}\n"
        
        if not description:
            description = "No Info Card found"
        
        response = discord.Embed(
            title=random_monster.get('Name', ''),
            description=description,
            color=discord.Color.blue()
        )
        
        response.set_image(url=random_monster.get('img', ''))
        await message.channel.send(embed=response)

    # Lists all monsters in the current database
    elif message.content.lower() == "$botzilla list":
        monster_names = [monster.get('Name', '') for monster in json_data]
        response = 'List of monsters:\n' + '\n'.join(monster_names)
        await message.channel.send(response)
    
    # Returns Menu
    elif message.content.lower() == '$botzilla menu':
        response = discord.Embed(
            title='Menu',
            description=f"**$botzilla:** Returns info card for a random Monster \n"
                        f"**$botzilla list:** Lists all monsters in the current database \n"
                        f"**$botzilla [MonsterName]:** Returns the info card for selected Monster",
            color=discord.Color.blue()
        )
        await message.channel.send(embed=response)

    # Returns info card for selected monster
    elif message.content.lower().startswith('$botzilla'):
        # Extract the monster name from the user's input
        match = re.match(r'\$botzilla\s+(\w+)', message.content, re.IGNORECASE)
        if match:
            monster_name = match.group(1).lower()

            # Find the specified monster in the JSON data
            monster_data = next((monster for monster in json_data if monster.get('Name', '').lower() == monster_name), None)
            if monster_data:
                # Return all available information with an embedded image
                description = ""
                
                    # Iterate through key/value pairs in the selected monster
                for key, value in monster_data.items():
                # Skip the 'Name' key in the dynamic description
                    if key.lower() != 'name':
                        description += f"**{key.capitalize()}:** {value}\n"
                
                if not description:
                    description = "No Info Card found"
                    
                response = discord.Embed(
                    title=monster_data.get('Name', ''),
                    description=description,
                    color=discord.Color.blue()
                )
                
                response.set_image(url=monster_data.get('img', ''))
                await message.channel.send(embed=response)
            else:
                response = f'{monster_name.capitalize()} not found in the data.'
        else:
            response = 'Invalid usage of $botzilla command. Use $botzilla MonsterName.'

        # await message.channel.send(embed=response)
