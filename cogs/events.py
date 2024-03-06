import sys

##############################
sys.dont_write_bytecode = True
##############################
import discord
from discord.ext import commands
from discord.utils import get
from random import choice
import asyncio
import config
from asyncio import sleep
import os
import sqlite3 as sql
from loguru import logger
import requests


class events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logger
        self.all_channel = []
        self.log = client.get_channel(config.log_channel)
        self.mentions = []
        # self.choise() = choise()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = await self.client.fetch_guild(payload.guild_id)
        member = get(guild.members, id=payload.user_id)
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = payload.member
        if user.id == config.mage_id:
            return
        elif channel.id in [1006185581585371248]:
            if user == message.author:
                try:
                    for reaction in message.reactions:
                        await reaction.remove(user)
                except:
                    pass
        elif channel.id == 1008409646744207461:
            if user == message.author:
                await message.add_reaction(payload.emoji)
                for reaction in message.reactions:
                    await reaction.remove(user)
            else:
                for reaction in message.reactions:
                    if reaction.emoji == payload.emoji:
                        if reaction.count > 1:
                            pass
                        else:
                            await reaction.remove(user)

async def setup(client):
    await client.add_cog(events(client))
