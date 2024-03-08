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


class commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logger
        self.prefix = config.prefix
        self.log = config.log_channel
        # self.report = client.get_channel(config.report_channel)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=10**1000):
        """Очистить чат"""

        await self.client.get_channel(config.log_channel).send(
            f"Пользователь {ctx.author.name} чистит чат {ctx.channel.name} на {amount if not amount == 10**1000 else "бесконечность"} сообщений"
        )
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def ping(self, ctx):
        """Пингануть бота"""
        
        delay = str(self.client.latency)
        if delay[0] == "0":
            await ctx.send(
                f":green_circle: - Я в сети. ||Пинг: **{delay[2:4]}ms.**||",
                delete_after=3,
            )
        else:
            await ctx.send(
                f":green_circle: - Я в сети. ||Пинг: **{delay[0]}s.**||",
                delete_after=3,
            )

        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def stats(self, ctx):
        """Получить информацию от участниках сервера"""
        
        await ctx.message.delete()
        
        online_members = []
        offline_members = []
        
        for member in ctx.guild.members:
            if member.status is not discord.Status.offline:
                online_members.append(member.name)
            else:
                offline_members.append(member.name)

        embed = discord.Embed(color=0x000)
        embed.add_field(name="Всего участников:", value=ctx.guild.member_count)
        embed.add_field(
            name=":green_circle: - Участников онлайн:",
            value=f"{len(online_members)}",
            inline=True,
        )
        embed.add_field(
            name=":red_circle: - Участников оффлайн:",
            value=f"{len(offline_members)}",
            inline=True,
        )
        await ctx.send(embed=embed, delete_after=5)
        

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def emojis(self, ctx):
        """Получить id всех emoji сервера"""
        
        await ctx.message.delete()

        guild = discord.utils.find(lambda g : g.id == ctx.guild.id, self.client.guilds)
        out: str = ""
        for rect in guild.emojis:
            out += "\n" + f"[{self.client.get_emoji(rect.id)}] - {rect.id}"

        await ctx.send(out, delete_after=15)
        

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def userinfo(
        self, ctx, member: discord.Member = None, guild: discord.Guild = None
    ):
        """Получить сводку о юзере"""

        if ctx.author.id != member.id:
            author1 = str(ctx.author)
            author2 = author1[:-5]
            if member == None:
                emb = discord.Embed(
                    title=f"{member.mention} | Информация о аккаунте: ",
                    color=ctx.message.author.color,
                )
                emb.add_field(
                    name="Имя:", value=ctx.message.author.display_name, inline=False
                )
                emb.add_field(
                    name="Айди пользователя:", value=ctx.message.author.id, inline=False
                )
                t = ctx.message.author.status
                if t == discord.Status.online:
                    d = "🟢 В сети"

                t = ctx.message.author.status
                if t == discord.Status.offline:
                    d = "⚪ Не в сети"

                t = ctx.message.author.status
                if t == discord.Status.idle:
                    d = "🔵 Не активен"

                t = ctx.message.author.status
                if t == discord.Status.dnd:
                    d = "🌙 Не беспокоить"

                emb.add_field(name="Тип аккаунта:", value=f"Человек", inline=False)

                emb.add_field(name="Активность:", value=d, inline=False)
                emb.add_field(
                    name="Игровой статус:",
                    value=ctx.message.author.activity,
                    inline=False,
                )
                emb.add_field(
                    name="Высшая роль на сервере:",
                    value=f"{ctx.message.author.top_role.mention}",
                    inline=False,
                )
                emb.add_field(
                    name="Аккаунт был создан:",
                    value=ctx.message.author.created_at.strftime(
                        "%a, %#d %B %Y, %I:%M %p UTC"
                    ),
                    inline=False,
                )
                emb.set_thumbnail(url=ctx.message.author.avatar_url)
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(
                    title=f"{member.name} | Информация о аккаунте: ", color=member.color
                )
                emb.add_field(name="Имя:", value=member.display_name, inline=False)
                emb.add_field(name="Айди пользователя:", value=member.id, inline=False)
                t = member.status
                if t == discord.Status.online:
                    d = "🟢 В сети"

                t = member.status
                if t == discord.Status.offline:
                    d = "⚪ Не в сети"

                t = member.status
                if t == discord.Status.idle:
                    d = "🔵 Не активен"

                t = member.status
                if t == discord.Status.dnd:
                    d = "🌙 Не беспокоить"

                emb.add_field(name="Активность:", value=d, inline=False)
                emb.add_field(
                    name="Игровой статус:", value=member.activity, inline=False
                )
                emb.add_field(
                    name="Высшая роль на сервере:",
                    value=f"{member.top_role.mention}",
                    inline=False,
                )
                if member.bot == True:
                    emb.add_field(name="Тип аккаунта:", value=f"Бот", inline=False)
                else:
                    emb.add_field(name="Тип аккаунта:", value=f"Человек", inline=False)
                emb.add_field(
                    name="Аккаунт был создан:",
                    value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                    inline=False,
                )
                await ctx.send(embed=emb, delete_after=10)
                await self.log.send(
                    f"Юзер: [{ctx.author}] получил информацию о пользователе: [{member.name}]"
                )
                await ctx.message.delete()

async def setup(client):
    await client.add_cog(commands(client))
