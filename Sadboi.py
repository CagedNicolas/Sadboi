'''
Discord bot that saves and plays playlists.
Save playlists to JSON files.
Make it into docker container to be ran on VPS.
Saves files by typing in "!playlist sadhours add http://youtube/" 
Has to monitor channel to know when to play and what.
'''
import asyncio
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(discord.version_info)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

client.run('NDc4MzE1MzM0MzI4Mzg1NTM3.DlI6jw.GwvzjCSf1kkSWxPzV_zvnl-w7Lc')