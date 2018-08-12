'''
Discord bot that saves and plays playlists.
Save playlists to JSON files.
Make it into docker container to be ran on VPS.
Saves files by typing in "!playlist sadhours add http://youtube/" 
Has to monitor channel to know when to play and what.
'''
import discord

client = discord.Client()
