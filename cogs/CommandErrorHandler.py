import traceback
import sys
from discord.ext import commands
import discord

class CommandErrorHandler:
    def __init__(self, client):
        self.client = client
    async def on_command_error(self, error: Exception, ctx: commands.Context):
        if hasattr(ctx.command, 'on_error'):
            return
        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.DisabledCommand):
            await self.client.send_message(ctx.message.channel, '{} has been disabled.'.format(ctx.command))
            return
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await self.client.send_message(ctx.message.author, '{} can not be used in Private Messages.'.format(ctx.command))
                return
            except discord.Forbidden:
                pass
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await self.client.send_message(ctx.message.channel, 'I could not find that member. Please try again.')
                return
        elif isinstance(error, commands.MissingRequiredArgument):
            await self.client.send_message(ctx.message.channel, "Missing required arguments. Check `?help`")
            return
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))