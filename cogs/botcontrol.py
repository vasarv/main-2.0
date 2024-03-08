import sys
##############################
sys.dont_write_bytecode = True
##############################
from discord.ext import commands
from discord.utils import get
import config
from asyncio import sleep
from loguru import logger


class cogscontrol(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logger
        # self.developers = config.developers
        self.log = self.client.get_channel(config.log_channel)

    def developer(self, id):
        if int(id) in config.developers:
            return True
        else:
            return False

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def load_cog(self, ctx, extension):
        """Reload Cog command"""

        if self.self.developer(ctx.author.id):
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"Ког [{extension}] загружен...")
            await self.log.send(f"Юзер: [{ctx.author}] подгрузил ког: [{extension}]")
            logger.debug(f"User: [{ctx.author}] loaded cog: [{extension}]")
        else:
            await ctx.send("У Вас нет прав разработчика!")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unload_cog(self, ctx, extension):
        """UnLoad Cog command"""
        
        if self.developer(ctx.author.id):
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"Ког [{extension}] выгружен...")
            await self.log.send(f"Юзер: [{ctx.author}] отгрузил ког: [{extension}]")
            logger.debug(f"User: [{ctx.author}] unloaded cog: [{extension}]")
        else:
            await ctx.send("У Вас нет прав разработчика!")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def reload_cog(self, ctx, extension):
        """Reload Cog command"""
        
        if self.developer(ctx.author.id):
            self.client.unload_extension(f"cogs.{extension}")
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"Ког [{extension}] перезагружен...")
            await self.log.send(f"Юзер: [{ctx.author}] перезагрузил ког: [{extension}]")
            logger.debug(f"User: [{ctx.author}] reloaded cog: [{extension}]")
        else:
            await ctx.send("У Вас нет прав разработчика!")


async def setup(client):
    await client.add_cog(cogscontrol(client))
