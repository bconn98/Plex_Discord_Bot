"""
file: bot.py
author: Jarod Godlewski
date: 7/20/2020
"""

from os import getenv
from random import choice

from dotenv import load_dotenv
from discord.ext import commands
from plex_control import add_to_list, find_by_keyword, same_director, current_sessions
from plexapi.server import PlexServer


load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')
PLEX_URL = getenv('PLEX_URL')
PLEX_TOKEN = getenv('PLEX_TOKEN')

bot = commands.Bot(command_prefix='!')
plex_server = PlexServer(PLEX_URL, PLEX_TOKEN)

list = []

@bot.command(name='bog', help='Responds with a bog moment')
async def bog(ctx):
    bog_moments = ["BOG CHURCH", "Hello? Bog Department?", "bog led theocracy 2020"]
    response = choice(bog_moments)
    await ctx.send(response)

@bot.command(name='queue', help='Queues Movie/TV Show to be put on Plex. If multi-worded, surround with double quotes.')
async def botqueue(ctx, name_of_media):
    if add_to_list(plex_server, list, name_of_media):
        await ctx.send('Media has been added to download queue. \nCurrent Queue: \n'  + display_queue())
    else:
        await ctx.send('Media is already present in download queue or server. \nCurrent Queue: \n'  + display_queue())

@bot.command(name='dequeue', help='Removes media from queue (Admin Only)')
@commands.has_permissions(administrator=True)
async def remove(ctx, name_of_media):
    list.remove(name_of_media)
    await ctx.send(name_of_media + ' removed from Queue.\nCurrent Queue: ' + display_queue())

@bot.command(name='keyword', help='Finds media based on a keyword')
async def keyword(ctx, keyword):
    result = format_results(find_by_keyword(plex_server, keyword))
    await ctx.send('Media associated with \'{}\': \n'.format(keyword) + result)

@bot.command(name='director', help='Displays list of other media with the same director')
async def director(ctx, name_of_media):
    videos, director  = same_director(plex_server, name_of_media)
    result = format_results(videos)
    await ctx.send('Other works by {}: \n'.format(director) + result)

@bot.command(name='sessions', help='Displays what is being watched right now')
async def sessions(ctx):
    result = format_results(current_sessions(plex_server))
    await ctx.send('Currently being watched: \n' + result)
    
def display_queue():
    result = ''
    for a, b in enumerate(list, 1):
        result += '{}. {}\n'.format(a, b)
    return result

def format_results(results):
    result = ''
    for a, b in enumerate(results, 1):
        result += '{}. {}\n'.format(a, b)
    return result

bot.run(TOKEN)