import sys
##############################
sys.dont_write_bytecode = True
##############################
import discord
from discord.ext import commands
from discord.utils import get
import config
from asyncio import sleep
from loguru import logger

class errors(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logger
        self.log = client.get_channel(config.log_channel)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, команда не найдена!', color=0xFF0000), delete_after=3)
            logger.error(f"Unknown command")

async def setup(client):
    await client.add_cog(errors(client))
