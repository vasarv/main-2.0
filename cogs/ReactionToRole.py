# This example requires the 'members' privileged intents
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

class ReactionToRole(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logger = logger
        self.role_message_id = 1214968965957165056
        self.default_channel = 1214255146184220762
        self.all_channel = []
        self.log = client.get_channel(config.log_channel)
        self.mentions = []
        self.ReactsToRoles: dict = {
            "1214991750691823636": 1214253939369840640,
            "1214991725915930714": 1214253443972337675,
            "1214991685822451712": 1214253881798950912
        }

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     guild = await self.client.fetch_guild(payload.guild_id)
    #     member = get(guild.members, id=payload.user_id)
    #     channel = self.client.get_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     user = payload.member
    #     if user.id == config.mage_id:
    #         return
    #     elif channel.id == self.default_channel:
    #         if user == message.author:
    #             await message.add_reaction(payload.emoji)
    #             for reaction in message.reactions:
    #                 await reaction.remove(user)
    #         else:
    #             for reaction in message.reactions:
    #                 if reaction.emoji == payload.emoji:
    #                     if reaction.count > 1:
    #                         pass
    #                     else:
    #                         await reaction.remove(user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Получение роли по реакции"""
        guild = await self.client.fetch_guild(payload.guild_id)
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = payload.member

        if not (user is None) and not (user.id == config.mage_id) and not (guild.get_role(self.ReactsToRoles[str(payload.emoji.id)]) in user.roles):
            if (channel.id == self.default_channel) and (message.id == self.role_message_id) and not (payload.emoji.id == None):
                await payload.member.add_roles(guild.get_role(self.ReactsToRoles[str(payload.emoji.id)]))

        return


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Удаление роли по реакции"""
        message_id = payload.message_id
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)

        if (member is not None) and not (member.id == config.mage_id) and (guild.get_role(self.ReactsToRoles[str(payload.emoji.id)]) in member.roles):
            if (message_id == self.role_message_id) and not (payload.emoji.id == None):
                await member.remove_roles(guild.get_role(self.ReactsToRoles[str(payload.emoji.id)]))

        return







async def setup(client):
    await client.add_cog(ReactionToRole(client))
