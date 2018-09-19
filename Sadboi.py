'''
await client.process_commands(message) # Bot needs this to continue processing the following client.command(s)
'''
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import json
import random
import traceback, logging, sys
import datetime

logging.basicConfig(filename='output.log', filemode='w', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s') # Logging

client = commands.Bot(command_prefix='?')

startup_extension = ['async_error_handler']

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='the crying game'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('Say hi faggot'):
        await client.send_message(message.channel, "Hey jews.")
    if client.user in message.mentions:
        await client.send_message(message.channel, "Hello! Use the command `?help` to know what my sad ass can do!") # When tagged, will respond.
    if message.content.startswith('PLAY NATIONAL ANTHEM') or message.content.startswith('Play national anthem') or message.content.startswith('bot play national anthem') or message.content.startswith('Bot play national anthem'):
        await client.send_message(message.channel, "https://www.youtube.com/watch?v=9fA9IpeWZUI")
    await client.process_commands(message)

@client.command(pass_context=True, 
name='join', 
description='Joins VC to allow bots such as Rythm to accept its commands. Used by typing ?join\n**WARNING**: Command user *must* be in VC, otherwise the bot might crash.', 
brief='Joins VC. **WARNING**: Command user *must* be in VC.', 
aliases=['Join', 'JOIN', 'getin'])
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    try:
        await client.join_voice_channel(channel)
        await client.say("Joined VC.")
    except:
        await client.say("Please make sure you're in VC then try again!")

@client.command(pass_context=True, 
name='leave', 
description='Leaves VC. Used as ?leave', 
brief='Leaves VC.', 
aliases=['Leave', 'LEAVE', 'fuckoff', 'getout'])
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    try:
        await voice_client.disconnect()
        await client.say("Collected my things and left VC. ):")
    except AttributeError:
        await client.say("I'm not even in VC! ):")

@client.command(pass_context=True, 
name='playlist', 
description='Plays the specified playlist.\nUsed as ?playlist **PlaylistName**', 
brief='Plays the specified playlist.', 
aliases=['Playlist','PlayList','pl', 'play'])
async def playlist(ctx, pl):
    await client.say('**Now playing**: %s' % pl)
    pl = pl.lower()
    with open('sbdb.json') as f:
        data = json.load(f)
    print("Database loaded.")
    for plname in data:
        if pl in plname['playlist']:
            for songname in plname['songs']:
                await client.say('!play ' + songname)
                await asyncio.sleep(3)
    await client.say('**Reached the end of the playlist**')

@client.command(pass_context=True,
name='createplaylist',
description='Create a new playlist. Use command ?addsong to add to the playlist after creation \nUsed as ?createplaylist **PlaylistName** **SongURL**',
brief='Creates a new playlist.',
aliases=['newpl','npl','createpl','cpl','cplaylist'])
async def createplaylist(ctx, pl, songurl):
    with open('sbdb.json') as f:
        data = json.load(f)
    pl = pl.lower()
    if not any(plname.get('playlist') == pl for plname in data):# If doesnt exist
        newpl = {}
        newpl['playlist'] = pl
        newpl['songs'] = [songurl]
        data.append(newpl)
        with open('sbdb.json', 'w') as f:
            json.dump(data, f)
        await client.say('Playlist created!') 
    elif any(plname.get('playlist') == pl for plname in data):
        await client.say('Playlist already exists!')# Else it loops back for some reason

@client.command(pass_context=True,
name='deleteplaylist',
description='Deletes a playlist. \nUsed as ?deleteplaylist **PlaylistName**',
brief='Deletes an existing playlist.',
aliases=['dpl','delpl','delplaylist','dplaylist','rmpl'])
async def deleteplaylist(ctx, pl):
    with open('sbdb.json') as f:
        data = json.load(f)
    #to_keep = [plname for plname in data if pl not in plname['playlist']]
    to_keep = []
    pl = pl.lower()
    for plname in data:
        if pl not in plname['playlist']:
            to_keep.append(plname)
    with open('sbdb.json', 'w') as f:
        json.dump(to_keep, f)
    await client.say('Playlist erased!')

@client.command(pass_context=True,
name='renamepl',
description='Renames a playlist.\nUsed as ?renamepl **OldPlaylistName** **NewPlaylistName**',
brief='Renames a playlist',
aliases=['rnmpl','renameplaylist','rnmplaylist','mvpl','mv'])
async def renamepl(ctx, plo, pln):
    with open('sbdb.json') as f:
        data = json.load(f)
    plo = plo.lower()
    pln = pln.lower()
    for plname in data:
        if plo == plname['playlist']:
            plname['playlist'] = pln
            with open('sbdb.json', 'w') as f:
                json.dump(data, f)
            await client.say("Playlist renamed!")
            break

@client.command(pass_context=True, 
name='move', 
description='Moves a song up/down in a playlist.\nUsed as ?move **PlaylistName** **SongIndex** **NewIndex**', 
brief='Moves a song up/down in a playlist (Must use song number)', 
aliases=['mov','m'])
async def move(ctx, pl, oldindex, newindex):
    with open('sbdb.json') as f:
        data = json.load(f)
    pl = pl.lower()
    oldindex = int(oldindex)
    newindex = int(newindex)
    oldindex -= 1
    newindex -= 1
    for plname in data:
        if pl in plname['playlist']:
            try:
                song = plname['songs'][oldindex]
                last_element = plname['songs'][-1]
                last_index = plname['songs'].index(last_element)
                if oldindex > last_index or oldindex < 0 or newindex > last_index or newindex < 0:
                    await client.say("Incorrect index given! Please try again.")
                    break
                else:
                    del plname['songs'][oldindex]
                    plname['songs'].insert(newindex, song)
                    with open('sbdb.json', 'w') as f:
                        json.dump(data, f)
                    await client.say("Song successfully moved!")
                    break
            except IndexError:
                await client.say("Incorrect index given! Please try again.") # Recycled shit from line 170.
                break

@client.command(pass_context=True, 
name='addsong', 
description='Adds the specified song URL to the specified playlist.\nUsed as ?addsong **PlaylistName** **SongURL**', 
brief='Adds song URLs to playlists', 
aliases=['add','Addsong','Add','AddSong','addSong'])
async def addsong(ctx, pl, songurl):
    with open('sbdb.json') as f:
        data = json.load(f)
    pl = pl.lower()
    for plname in data:
        if pl in plname['playlist']:
            plname['songs'].append(songurl)
    await client.say('Song added to %s!' % pl)
    with open('sbdb.json', 'w') as f:
        json.dump(data, f)

@client.command(pass_context=True, 
name='rmsong', 
description='Removes a song from a specified playlist. \nUsed as ?rmsong **PlaylistName** **SongURL**', 
brief='Removes songs from playlists', 
aliases=['rm','del','delete','erase','delsong'])
async def rmsong(ctx, pl, songurl):
    with open('sbdb.json') as f:
        data = json.load(f)
    pl = pl.lower()
    for plname in data:
        try:
            if pl in plname['playlist']:
                plname['songs'].remove(songurl)
                await client.say('Song removed from %s!' % pl)
            with open('sbdb.json', 'w') as f:
                json.dump(data, f)
        except ValueError:
            await client.say("Song not found!")

@client.command(pass_context=True, 
name='view', 
description='View all the songs in a specified playlist.\n Used as ?view **PlaylistName**', 
brief='View songs in a playlist.', 
aliases=['v','View'])
async def view(ctx, pl):
    with open('sbdb.json') as f:
        data = json.load(f)
    pl = pl.lower()
    for plname in data:
        if pl in plname['playlist']:
            songlist = ''
            counter = 1 # More pythonic pl0x?
            for song in plname['songs']:
                songlist += str(counter) + ". " + song + '\n'
                counter += 1
    await client.say(songlist + "**Reached the end of the playlist**")

@client.command(pass_context=True, 
name='viewpl', 
description='View all the playlists.\n Used as ?viewpl', 
brief='View all playlists.', 
aliases=['vpl','Viewplaylist','plv'])
async def viewpl(ctx):
    with open('sbdb.json') as f:
        data = json.load(f)
    pllist = ''
    for plname in data:
        pllist += plname['playlist'] + '\n'
    await client.say(pllist + '**Reached the end of the list**')

@client.command(pass_context=True,
name='shuffleplay',
description='Plays shuffles and plays a specified playlist. \nUsed as ?shuffleplay **PlaylistName**',
brief='Shuffles & plays playlists.',
aliases=['sp','shufflep','splay'])
async def shuffleplay(ctx, pl):
    with open('sbdb.json') as f:
        data = json.load(f)
    pl = pl.lower()
    for plname in data:
        if pl in plname['playlist']:
            random.shuffle(plname['songs'])
            for songname in plname['songs']:
                await client.say('!play ' + songname)
                await asyncio.sleep(3)

@client.command(pass_context=True, 
name='clear', 
description='Clears messages by typing ?clear **amount**.\nDefault amount is 10 messages. *Requires mod status*.', 
brief='Clears messages.')
async def clear(ctx, amount=10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted.')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

if __name__ == "__main__":
    for extension in startup_extension:
        try:
            print('Loading {}...'.format(extension))
            client.load_extension(extension)
            print("{} loaded.".format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

client.run('NDc4MzE1MzM0MzI4Mzg1NTM3.DoEWeg.XTF4sVr31N1X-m8CFoq3YCj2SzM')