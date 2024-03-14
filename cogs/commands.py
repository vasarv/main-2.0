import sys

##############################
sys.dont_write_bytecode = True
##############################
import discord
from discord.ext import commands
from discord.utils import get
import config
from asyncio import sleep
import sqlite3 as sql
from loguru import logger


class commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logger
        self.prefix = config.prefix
        self.log = config.log_channel

    @commands.command()
    async def ping(self, ctx):
        """Пингануть бота"""

        delay: str = str(self.client.latency)

        await ctx.send(
            f":green_circle: - Я в сети. ||Пинг: **{delay[2:4]}{"ms" if delay[0] == "0" else "s"}.**||",
            delete_after=3,
        )

        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount=10**1000):
        """Очистить чат"""

        await self.client.get_channel(config.log_channel).send(
            f"Пользователь {ctx.author.name} чистит чат {ctx.channel.name} на {amount if not amount == 10**1000 else '∞'} сообщений"
        )

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def stats(self, ctx):
        """Получить информацию от участниках сервера"""

        activites: list[list] = [[], [], []] #bots online, users online, users offline
        
        for member in ctx.guild.members:
            if member.bot == True:
                activites[0].append(member.name)
            elif not (member.status is discord.Status.offline) and member.bot == False:
                activites[1].append(member.name)
            else:
                activites[2].append(member.name)

        embed = discord.Embed(color=0x000)
        embed.add_field(name="Всего участников:", value=ctx.guild.member_count)
        embed.add_field(
            name=":green_circle: - Участников онлайн:",
            value=f"{len(activites[1])}",
            inline=True,
        )

        embed.add_field(
            name=":red_circle: - Участников оффлайн:",
            value=f"{len(activites[2])}",
            inline=True,
        )

        embed.add_field(
            name=":robot: - Ботов онлайн:",
            value=f"{len(activites[0])}",
            inline=True,
        )

        await ctx.send(embed=embed, delete_after=5)
        await ctx.message.delete()


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def emojis(self, ctx):
        """Получить id всех emoji сервера"""

        guild = discord.utils.find(lambda g : g.id == ctx.guild.id, self.client.guilds)
        emoji_ids: list = [f"[{self.client.get_emoji(rect.id)}] - {rect.id}" for rect in guild.emojis]

        await ctx.send("\n".join(emoji_ids), delete_after=15)
        await ctx.message.delete()


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def userinfo(
        self, ctx, member: discord.Member = None, guild: discord.Guild = None
    ):
        """Получить сводку о юзере"""

        user = member if not (member == None) else ctx.message.author
        status = user.status
        bot = user.bot
        if status == discord.Status.online:
            status = "🟢 - В сети"
        elif status == discord.Status.offline:
            status = "⚪ - Не в сети"
        elif status == discord.Status.idle:
            status = "🔵 - Не активен"
        elif status == discord.Status.dnd:
            status = "🌙 - Не беспокоить"

        emb = discord.Embed(
            title=f"{user.name} | Информация о {'приложении' if bot else 'аккаунте'}:", color=user.color
        )
        emb.add_field(name="Имя:", value=user.display_name, inline=False)
        emb.add_field(name="Айди пользователя:", value=user.id, inline=False)
        emb.add_field(name="Тип аккаунта:", value=f"{'Бот' if bot else 'Человек'}", inline=False)
        emb.add_field(name="Активность:", value=status, inline=False)
        emb.add_field(
            name="Игровой статус:",
            value=user.activity,
            inline=False,
        )
        emb.add_field(
            name="Высшая роль на сервере:",
            value=f"{user.top_role.mention}",
            inline=False,
        )
        emb.add_field(
            name="Аккаунт был создан:",
            value=user.created_at.strftime(
                "%a, %#d %B %Y, %I:%M %p UTC"
            ),
            inline=False,
        )
        emb.set_thumbnail(url=user.avatar)

        await ctx.send(embed=emb, delete_after = 30)
        await self.log.send(
            f"Юзер: [{ctx.author}] получил информацию о пользователе: [{user.name}]"
        )

        await ctx.message.delete()

async def setup(client):
    await client.add_cog(commands(client))
    
