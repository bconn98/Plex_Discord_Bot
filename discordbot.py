# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from plex_control import add_to_queue
from queue import Queue


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PLEX_URL = os.getenv('PLEX_URL')
PLEX_TOKEN = os.getenv('PLEX_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
plex_server = PlexServer(PLEX_URL, PLEX_TOKEN)

queue = Queue()

@bot.command(name='bog', help='Responds with a bog moment')
async def bog(ctx):
    response = "BOG CHURCH"
    await ctx.send(response)

@bot.command(name='queue', help='Queues a Movie/TV Show to be downloaded if it is not already on the server or queue.\nIf multi-worded use double quotes surrounding it.')
async def botqueue(ctx, name_of_media):
    if add_to_queue(plex_server, queue, name_of_media):
        await ctx.send('Media has been added to download queue.')
    else:
        await ctx.send('Media is already present in download queue or server.')

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
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
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
        
client.run(TOKEN)