"""
file: discord_bot.py
author: Jarod Godlewski
date: 7/20/2020
"""

from discord import Client, utils
from dotenv import load_dotenv
from os import getenv

load_dotenv()
DISCORD_TOKEN = getenv('DISCORD_TOKEN')
DISCORD_GUILD = getenv('DISCORD_GUILD')
PLEX_URL = getenv('PLEX_URL')
PLEX_TOKEN = getenv('PLEX_TOKEN')

client = Client()

@client.event
async def on_ready():
    guild = utils.get(client.guilds, name=DISCORD_GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!bog':
        response = "BOG CHURCH"
        await message.channel.send(response)

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(DISCORD_TOKEN)
