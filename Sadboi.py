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

client = commands.Bot(command_prefix='?')

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
    channel = ctx.message.author.voice.voice_channel # Add error checking incase author isn't in VC
    await client.say("Joining VC. Make sure you're in VC already!")
    await client.join_voice_channel(channel)

@client.command(pass_context=True, 
name='leave', 
description='Leaves VC. Used as ?leave', 
brief='Leaves VC.', 
aliases=['Leave', 'LEAVE', 'fuckoff', 'getout'])
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server) # Add error checking incase it isn't in a VC
    await client.say("Leaving VC. Please give me a moment to collect my things ):")
    await voice_client.disconnect()

@client.command(pass_context=True, 
name='playlist', 
description='Plays the specified playlist.\nUsed as ?playlist **PlaylistName**', 
brief='Plays the specified playlist.', 
aliases=['Playlist','PlayList','pl', 'play'])
async def playlist(ctx, pl):
    await client.say('**Now playing**: %s' % pl)
    print("Now loading playlist database...")
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
    for plname in data:
        if pl not in plname['playlist']: # Check if playlist doesn't already exist
            newpl = {}
            newpl['playlist'] = pl
            newpl['songs'] = [songurl]
            data.append(newpl)
            await client.say('Playlist created!')
            with open('sbdb.json', 'r+') as f:
                json.dump(data, f)
            break
        else:
            await client.say('Playlist already exists!') # DOESNT WORK, PLEASE FIX

@client.command(pass_context=True,
name='deleteplaylist',
description='Deletes a playlist. \nUsed as ?deleteplaylist **PlaylistName**',
brief='Deletes an existing playlist.',
aliases=['dpl','delpl','delplaylist','dplaylist'])
async def deleteplaylist(ctx, pl):
    with open('sbdb.json') as f:
        data = json.load(f)
    #to_keep = [plname for plname in data if pl not in plname['playlist']]
    to_keep = []
    for plname in data:
        if pl not in plname['playlist']:
            to_keep.append(plname)
    with open('sbdb.json', 'w') as f:
        json.dump(to_keep, f)
    await client.say('Playlist erased!')

@client.command(pass_context=True, 
name='movup', 
description='Moves a song up in a playlist.\nUsed as ?movup **PlaylistName** **SongURL**', 
brief='Moves a song up in a playlist (Must use song URL)', 
aliases=['mu','moveup','mup'])
async def movup(ctx, pl, songurl):
    print("Now loading playlist database...")
    with open('sbdb.json') as f:
        data = json.load(f)
    for plname in data:
        if pl in plname['playlist']:
            if songurl in plname['songs']:
                old_index = plname['songs'].index(songurl)
                if old_index > 0:
                    del plname['songs'][old_index]
                    new_index = int(old_index) - 1
                    plname['songs'].insert(new_index, songurl)
                    with open('sbdb.json', 'w') as f:
                        json.dump(data, f)
                    await client.say("Song successfully moved!")
                else:
                    await client.say("The song you chose is already at the top of the playlist!")

@client.command(pass_context=True, 
name='movdn', 
description='Moves a song down in a playlist.\nUsed as ?movdn **PlaylistName** **SongURL**', 
brief='Moves a song down in a playlist (Must use song URL)', 
aliases=['md','movedown','mdn'])
async def movdn(ctx, pl, songurl):
    print("Now loading playlist database...")
    with open('sbdb.json') as f:
        data = json.load(f)
    for plname in data:
        if pl in plname['playlist']:
            if songurl in plname['songs']:
                old_index = plname['songs'].index(songurl)
                last_element = plname['songs'][-1]
                last_index = plname['songs'].index(last_element)
                if old_index < last_index:
                    del plname['songs'][old_index]
                    new_index = int(old_index) + 1
                    plname['songs'].insert(new_index, songurl)
                    with open('sbdb.json', 'w') as f:
                        json.dump(data, f)
                    await client.say("Song successfully moved!")
                else:
                    await client.say("The song you chose is already at the bottom of the playlist!")

@client.command(pass_context=True, 
name='addsong', 
description='Adds the specified song URL to the specified playlist.\nUsed as ?addsong **PlaylistName** **SongURL**', 
brief='Adds song URLs to playlists', 
aliases=['add','Addsong','Add','AddSong','addSong'])
async def addsong(ctx, pl, songurl):
    with open('sbdb.json') as f:
        data = json.load(f)
    for plname in data:
        if pl in plname['playlist']:
            plname['songs'].append(songurl)
    await client.say('Song added to %s!' % pl) # Requires error checking
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
    for plname in data:
        if pl in plname['playlist']:
            plname['songs'].remove(songurl)
    await client.say('Song removed from %s!' % pl) # Requires error checking
    with open('sbdb.json', 'w') as f:
        json.dump(data, f)

@client.command(pass_context=True, 
name='view', 
description='View all the songs in a specified playlist.\n Used as ?view **PlaylistName**', 
brief='View songs in a playlist.', 
aliases=['v','View'])
async def view(ctx, pl):
    with open('sbdb.json') as f:
        data = json.load(f)
    for plname in data:
        if pl in plname['playlist']:
            songlist = ''
            for song in plname['songs']:
                songlist += song + '\n'
    await client.say(songlist)
    await asyncio.sleep(1)
    await client.say('**Reached the end of the playlist**')

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
    await client.say(pllist)
    await asyncio.sleep(1)
    await client.say('**Reached the end of the list**')

@client.command(pass_context=True,
name='shuffleplay',
description='Plays shuffles and plays a specified playlist. \nUsed as ?shuffleplay **PlaylistName**',
brief='Shuffles & plays playlists.',
aliases=['sp','shufflep','splay'])
async def shuffleplay(ctx, pl):
    with open('sbdb.json') as f:
        data = json.load(f)
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

client.run('NDc4MzE1MzM0MzI4Mzg1NTM3.Dnp-UQ.QO3ik8MavB1_GRSST3s2tAm9sS8')