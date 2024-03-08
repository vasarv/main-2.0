import sys
##############################
sys.dont_write_bytecode = True
##############################
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import config
from asyncio import sleep
import os
import sqlite3 as sql
from loguru import logger
import requests
import datetime


class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logger = logger
        self.developers = config.developers
        self.log = client.get_channel(config.log_channel)
        # self.messages_log = client.get_channel(1038775710912876616)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Если сообщение изменено, то логируем до и после изменения"""
        
        if (before.author.id != config.mage_id) and not (before.author.bot == True):
            current_date_time = datetime.datetime.now()
            emb = discord.Embed(title = 'Изменённое сообщение', color=after.author.color)
            emb.set_author(name = f"{before.author.name} изменил(-ла) сообщение", icon_url = before.author.avatar.url)
            emb.add_field(name = 'Канал:'.format(after.channel.name), value = '{}'.format(after.channel.name))
            emb.add_field(name = 'До:'.format(before.content), value = '{}'.format(before.content))
            emb.add_field(name = 'После:'.format(after.content), value = '{}'.format(after.content))
            emb.set_footer(text = f'{before.author} изменяет сообщение. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}'.format(before.author.name), icon_url = before.author.avatar.url)

            await self.log.send(embed = emb)

    # @commands.Cog.listener()
    # async def on_message_delete(self, message):
    #     if message.author.id != config.mage_id:
    #         current_date_time = datetime.datetime.now()
    #         emb = discord.Embed(title = 'Удалённое сообщение', color=message.author.color)
    #         emb.set_author(name = f"{message.author.name} удалил(-ла) сообщение", icon_url = message.author.avatar.url)
    #         emb.add_field(name = 'Канал:'.format(message.channel.name), value = '{}'.format(message.channel.name))
    #         emb.add_field(name = 'Содержание:'.format(message.content), value = '{}'.format(message.content))
    #         emb.set_footer(text = f'{message.author} удаляет сообщение. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}'.format(message.author.name), icon_url = message.author.avatar.url)

    #         await self.log.send(embed = emb)

async def setup(client):
    await client.add_cog(Logs(client))
