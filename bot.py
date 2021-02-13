"""
file: bot.py
author: Jarod Godlewski
date: 7/20/2020
"""

from os import getenv
from random import choice
from time import sleep

from dotenv import load_dotenv
from discord import Client
from discord.ext import commands, tasks
from discord.utils import get
from plex_control import add_to_list, find_by_keyword, same_director, current_sessions, reset_connection, stop_session, check_list
from plexapi.server import PlexServer

import asyncio
from pickle import load, dump

sleep(120)

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')
PLEX_URL = getenv('PLEX_URL')
PLEX_TOKEN = getenv('PLEX_TOKEN')
CHANNEL_ID = getenv('CHANNEL_ID')

bot = commands.Bot(command_prefix='!')
client = Client()
plex_server = PlexServer(PLEX_URL, PLEX_TOKEN)

class Request:
    """
    A request object.
    """
    # The name of the requestor
    requestor:str

    # The title that was requested
    title:str

    def __init__(self, requestor, title):
        self.requestor = requestor
        self.title = title

    def get_requestor(self):
        return self.requestor

    def get_title(self):
        return self.title


# Load the queue from persistant storage
lst = load(open("save.p", "rb" ))


async def my_task():
    """
    Background task that checks for videos in the queue being added to plex.
    Notifies the user that asked for the item if it is found.
    """
    while True:
        channel = bot.get_channel(CHANNEL_ID) 
        video_list = []
        for req in lst:
            video_list.append(req.get_title())

        video = check_list(plex_server, video_list)

        if channel and video:
            for req in lst:
                if video == req.title:
                    await channel.send(f"{req.get_requestor()} {req.get_title()} found in Plex!")
                    lst.remove(req)
        await asyncio.sleep(1)


@bot.command(name='bog', help='Responds with a bog moment')
async def bog(ctx):
    """
    First command written. Responds with an inside joke.
    Params: None
    Returns: message
    """
    bog_moments = ["BOG CHURCH", "Hello? Bog Department?", "bog led theocracy 2020", "legalize bog fights", "Reginald Feather Bottom"]
    response = choice(bog_moments)
    await ctx.send(response)


@bot.command(name='queue', help='Queues Movie/TV Show to be put on Plex. If multi-worded, surround with double quotes.')
async def botqueue(ctx, name_of_media):
    """
    Checks to see if media is already in the queue or server. If not adds it to the queue.
    Params: name_of_media, the Media's name
    Returns: status message
    """
    if add_to_list(plex_server, lst, name_of_media):
        lst.append(Request(ctx.message.author.mention, name_of_media))
        await ctx.send(f'{ctx.message.author.mention} {name_of_media} has been added to download queue. \nCurrent Queue: \n{display_queue()}')
    else:
        await ctx.send(f'{name_of_media} is already present in download queue or server. \nCurrent Queue: \n{display_queue()}')


@bot.command(name='list', help='Shows the current Queue')
async def showqueue(ctx):
    """
    Checks to see if media is already in the queue or server. If not adds it to the queue.
    Params: name_of_media, the Media's name
    Returns: status message
    """
    await ctx.send('Current Queue: \n'  + display_queue())


@bot.command(name='dequeue', help='Removes media from queue (Admin Only)')
@commands.has_permissions(administrator=True)
async def remove(ctx, name_of_media):
    """
    Removes items from queue when adding it to the server.
    Params: name_of_media, the Media's name
    Returns: message
    """
    lst.remove(name_of_media)
    await ctx.send(name_of_media + ' removed from Queue.\nCurrent Queue: ' + display_queue())


@bot.command(name='pineapple', help='Attempts to reset connections to fix streams. (Admin Only)')
@commands.has_permissions(administrator=True)
async def reset(ctx):
    """
    Resets server connections for dianostic purposes.
    Params: None
    Returns: status message
    """
    if reset_connection():
        await ctx.send('Connections reset.')
    else:
        await ctx.send('Connections failed to be reset.')


@bot.command(name='keyword', help='Finds media based on a keyword')
async def keyword(ctx, keyword):
    """
    Searches for media on the server by a keyword.
    Params: keyword, the word to search on
    Returns: list of related Media
    """
    result = format_results(find_by_keyword(plex_server, keyword))
    await ctx.send('Media associated with \'{}\': \n'.format(keyword) + result)


@bot.command(name='director', help='Displays list of other media with the same director')
async def director(ctx, name_of_media):
    """
    Searches for media on the server with a shared director/can be used to find the director's name.
    Params: name_of_media, the Media's name
    Returns: result, list of related Media. director, the director's name
    """
    videos, director  = same_director(plex_server, name_of_media)
    result = format_results(videos)
    await ctx.send('Other works by {}: \n'.format(director) + result)


@bot.command(name='sessions', help='Displays what is being watched right now')
async def sessions(ctx):
    """
    Shows all current media being streamed. "What's being watched" functionality.
    Params: None
    Returns: result, list of Media being watched
    """
    result = format_results(current_sessions(plex_server))
    await ctx.send('Currently being watched: \n' + result)


@bot.command(name='nuke', help='Kill running session (Admin only, ask for help)')
@commands.has_permissions(administrator=True)
async def stop_user_session(ctx, name_of_session):
    """
    Stops the session entered. "Stop a bad session" functionality.
    Params: name_of_session, the session to stop
    Returns: result, true if stopped false otherwise
    """
    if stop_session(plex_server, name_of_session):
        await ctx.send('Session Stopped')
    else:
        await ctx.send('Failed to stop session')


# Close the bot
@bot.command(aliases=["quit"])
@commands.has_permissions(administrator=True)
async def close(ctx):
    await ctx.send('Shutting down and saving state')
    dump(lst, open( "save.p", "wb" ))
    await bot.close()


def display_queue():
    """
    Aux function used to format the queue for returns.
    Params: None
    Return: result, formatted queue
    """
    result = ''
    for a, b in enumerate(lst, 1):
        result += '{}. {}\n'.format(a, b.get_title())
    return result


def format_results(results):
    """
    Aux function used to format the data returned by server.
    Params: None
    Return: result, formatted list
    """
    result = ''
    for a, b in enumerate(results, 1):
        result += '{}. {}\n'.format(a, b)
    return result

bot.run(TOKEN)
client.loop.create_task(my_task())

