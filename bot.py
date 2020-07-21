"""
file: bot.py
author: Jarod Godlewski
date: 7/20/2020
"""

import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from plex_control import add_to_list
from plexapi.server import PlexServer
from queue import Queue


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PLEX_URL = os.getenv('PLEX_URL')
PLEX_TOKEN = os.getenv('PLEX_TOKEN')

bot = commands.Bot(command_prefix='!')
plex_server = PlexServer(PLEX_URL, PLEX_TOKEN)

list = []

@bot.command(name='bog', help='Responds with a bog moment')
async def bog(ctx):
    response = "BOG CHURCH"
    await ctx.send(response)

@bot.command(name='queue', help='Queues a Movie/TV Show to be downloaded if it is not already on the server or queue.\nIf multi-worded use double quotes surrounding it.')
async def botqueue(ctx, name_of_media):
    if add_to_list(plex_server, list, name_of_media):
        await ctx.send('Media has been added to download queue. \nCurrent Queue: \n'  + display_queue())
    else:
        await ctx.send('Media is already present in download queue or server. \nCurrent Queue: \n'  + display_queue())

@bot.command(name='dq', help='Removes media from queue (Admin Only)')
@commands.has_permissions(administrator=True)
async def remove(ctx, name_of_media):
    list.remove(name_of_media)
    await ctx.send(name_of_media + ' removed from Queue.\nCurrent Queue: ' + display_queue())

def display_queue():
    result = ''
    for a, b in enumerate(list, 1):
        result += '{}. {}\n'.format(a, b)
    return result

bot.run(TOKEN)