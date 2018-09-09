'''
Discord bot that saves and plays playlists.
Save playlists to JSON files.
Make it into docker container to be ran on VPS.
Saves files by typing in "!playlist sadhours add http://youtube/" 
Has to monitor channel to know when to play and what.
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

@client.event
async def on_message(message):
    print('A user has sent a message.')
    await client.process_commands(message) # Bot needs this to continue processing the following client.command(s)

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel # Make error checking incase author isn't in VC
    await client.say("Joining VC. Make sure you're in VC already!")
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server) # Make error checking incase it isn't in a VC
    await client.say("Leaving VC. Please give me a moment to collect my things ):")
    await voice_client.disconnect()

@client.command(pass_context=True)
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

@client.command(pass_context=True)
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

client.run('NDc4MzE1MzM0MzI4Mzg1NTM3.DlI6jw.GwvzjCSf1kkSWxPzV_zvnl-w7Lc')