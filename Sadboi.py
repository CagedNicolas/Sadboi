'''
Discord bot that saves and plays playlists.
Save playlists to JSON files.
Make it into docker container to be ran on VPS.
Saves files by typing in "!playlist sadhours add http://youtube/" 
Has to monitor channel to know when to play and what.
await client.process_commands(message) # Bot needs this to continue processing the following client.command(s)
'''
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import json

client = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='the crying game'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command(pass_context=True, 
name='join', 
description='Joins VC to allow bots such as Rythm to accept its commands. Used by typing ?join\n**WARNING**: Command user *must* be in VC, otherwise the bot might crash.', 
brief='Joins VC. **WARNING**: Command user *must* be in VC.', 
aliases=['Join', 'JOIN', 'getin'])
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel # Make error checking incase author isn't in VC
    await client.say("Joining VC. Make sure you're in VC already!")
    await client.join_voice_channel(channel)

@client.command(pass_context=True, 
name='leave', 
description='Leaves VC. Used as ?leave', 
brief='Leaves VC.', 
aliases=['Leave', 'LEAVE', 'fuckoff', 'getout'])
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server) # Make error checking incase it isn't in a VC
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
    with open('sbdb.json', 'r+') as f:
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

client.run('NDc4MzE1MzM0MzI4Mzg1NTM3.DnfEiQ._vJy8-IaqWTT3zeEfgU1-SUbArE')