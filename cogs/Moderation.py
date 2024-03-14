from discord.ext import commands
import discord
import datetime
import config
import asyncio
from config import prefix as command_prefix
from loguru import logger


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # kick
    @commands.command(aliases=["кик"])
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Кикнуть юзера"""

        await member.kick(reason=reason)

        emb = discord.Embed(title="Kick", colour=discord.Color.orange())

        emb.set_author(name=member.name, icon_url=member.avatar.url)
        if reason == None:
            emb.add_field(
                name="Kick user",
                value=f"Kicked user : {member.mention}",
            )
        else:
            emb.add_field(
                name=f"Kick user\nПричина кика: {reason}",
                value=f"Kicked user: {member.mention}",
            )
        emb.set_footer(
            text="Был кикнут администратором".format(ctx.author.name),
            icon_url=ctx.author.avatar.url,
        )

        logger.info(
            f"Пользователь {ctx.author.name} кикнул юзера {member.name} по причине {reason}"
        )

        await ctx.send(embed=emb, delete_after=15)

        await ctx.message.delete()

    # ban
    @commands.command(aliases=["бан"])
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Забанить юзера"""

        current_date_time = datetime.datetime.now()
        now_date = current_date_time.time()
        emb = discord.Embed(title="Бан:", color=discord.Color.red())
        ban_time: int

        try:
            await member.ban(reason=reason)
        except:
            await ctx.send(
                f"Не возможно забанить пользователя: {member.mention}!",
                delete_after=5,
            )

        emb.set_author(name=member.name, icon_url=member.avatar.url)
        emb.add_field(name="За что бан?", value=f"{reason}")

        # match amount_time[-1]:
        #     case "s":
        #         ban_time = int(amount_time[:-1])
        #     case "m":
        #         ban_time = int(amount_time[:-1]) * 60
        #     case "h":
        #         ban_time = int(amount_time[:-1]) * 60 * 60
        #     case "d":
        #         ban_time = int(amount_time[:-1]) * 60 * 60 * 24

        # if "s" in amount_time:
        #     emb.add_field(
        #         name="На сколько?",
        #         value=f"{amount_time[:-1]} секунд",
        #     )
        # elif "m" in amount_time:
        #     emb.add_field(
        #         name="На сколько?",
        #         value=f"{amount_time[:-1]} минут",
        #     )
        # elif "h" in amount_time:
        #     emb.add_field(
        #         name="На сколько?",
        #         value=f"{amount_time[:-1]} часа(-ов)",
        #     )
        # elif "d" in amount_time:
        #     emb.add_field(
        #         name="На сколько?",
        #         value=f"{amount_time[:-1]} дней",
        #     )
        # elif amount_time == None:
        #     emb.add_field(
        #         name="На сколько?",
        #         value=f"навсегда",
        #     )
        # else:
        #     emb.add_field(
        #         name="На сколько?",
        #         value=f"навсегда",
        #     )
            # await ctx.send(f"Что-то пошло не так!", delete_after=5)

        emb.set_footer(
            text=f"{ctx.author} забанил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                ctx.author.name
            ),
            icon_url=ctx.author.avatar.url,
        )
        
        await ctx.send(embed=emb, delete_after=15)

        logger.info(
                f"Пользователь {member.name} забанен. Выдал бан: {ctx.author.name} по причине: {reason}"
            )
        
        # await asyncio.sleep(ban_time)

        # for ban_entry in self.banned_users:
        #     user = ban_entry.user
        #     await ctx.guild.unban(user)
        # try:
        #     await member.send(
        #         embed=discord.Embed(
        #             description=f"""**{member.mention}** Время бана истекло, вы были разбанены."""
        #         )
        #     )
        # except:
        #     pass

        await ctx.message.delete()

    # Unban
    @commands.command(aliases=["разбан"])
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        """Разбанить юзера"""

        await ctx.message.delete()

        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            user = ban_entry.user

            if user.id == member.id:
                await ctx.guild.unban(user)

                emb = discord.Embed(title="Unban", colour=discord.Color.green())
                emb.set_author(name=user.name, icon_url=user.avatar.url)
                emb.add_field(
                    name="Unban user",
                    value=f"Unbaned user: {user.mention}",
                )
                emb.set_footer(
                    text="Был разбанен администратором",
                    icon_url=ctx.author.avatar.url,
                )

                await ctx.send(embed=emb, delete_after=15)

                logger.info(
                    f"Пользователь {ctx.author.name} разбанил юзера {user.name}"
                )

                return

        await ctx.send(f"Юзер не забанен!", delete_after=5)

    # mute
    @commands.command(aliases=["мьют"])
    @commands.has_permissions(administrator=True)
    async def mute(
        self, ctx, member: discord.Member = None, amount_time=None, *, reason=None
    ):
        """Замьютить юзера"""

        mute_time: int
        current_date_time = datetime.datetime.now()
        mute_role = discord.utils.get(ctx.guild.roles, id=config.mute_role_id)

        match amount_time[-1]:
            case "s":
                mute_time = int(amount_time[:-1])
            case "m":
                mute_time = int(amount_time[:-1]) * 60
            case "h":
                mute_time = int(amount_time[:-1]) * 60 * 60
            case "d":
                mute_time = int(amount_time[:-1]) * 60 * 60 * 24

        if member is None:
            await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.mention}, укажите пользователя",
                    description=f"Пример: {command_prefix}unmute **@user**",
                )
            )
        elif amount_time is None:
            await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.mention}, **укажите кол-во времени**",
                    description=f"Пример: {command_prefix}mute @user **time** reason",
                )
            )
        elif reason is None:
            await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.mention}, **укажите причину**",
                    description=f"Пример: {command_prefix}mute @user time **reason**",
                )
            )
        else:
            emb = discord.Embed(title="Мьют", color=0x000001)
            emb.set_author(name=member.name, icon_url=member.avatar.url)
            emb.add_field(name="За что мьют?", value=f"{reason}")

            if "s" in amount_time:
                emb.add_field(
                    name="На сколько секунд?",
                    value=f"{amount_time[:-1]} секунд",
                )
            elif "m" in amount_time:
                emb.add_field(
                    name="На сколько минут?",
                    value=f"{amount_time[:-1]} минут",
                )
            elif "h" in amount_time:
                emb.add_field(
                    name="На сколько часов?",
                    value=f"{amount_time[:-1]} часа(-ов)",
                )
            elif "d" in amount_time:
                emb.add_field(
                    name="На сколько дней?",
                    value=f"{amount_time[:-1]} дней",
                )
            else:
                await ctx.send(f"Что-то пошло не так!", delete_after=5)

            emb.set_footer(
                text=f"{ctx.author} замьютил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                    ctx.author.name
                ),
                icon_url=ctx.author.avatar.url,
            )

            await member.add_roles(mute_role)

            await ctx.send(embed=emb, delete_after=30)

            logger.info(
                f"Пользователь {member.name} был замьючен. Выдал мьют: {ctx.author.name}] на [{amount_time}] по причине [{reason}]"
            )

            await asyncio.sleep(mute_time)

            if mute_role in member.roles:
                await member.remove_roles(mute_role)
                return

        await ctx.message.delete()

    @commands.command(aliases=["размьют"])
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member = None):
        """Размьютить юзера"""

        current_date_time = datetime.datetime.now()
        mute_role = discord.utils.get(ctx.guild.roles, id=config.mute_role_id)

        if member is None:
            await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.mention}, укажите пользователя",
                    description=f"Пример: {command_prefix}unmute **@user**",
                )
            )

        await member.remove_roles(mute_role)

        emb = discord.Embed(
            title="Размьют",
            description=f"""**{member.mention}**, вы были размьючены.""",
            color=0xFFFFFF,
        )
        emb.set_author(name=member.name, icon_url=member.avatar.url)
        emb.set_footer(
            text=f"{ctx.author} размьютил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                ctx.author.name
            ),
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=emb, delete_after=15)

        await ctx.message.delete()

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     self.guild = await self.client.fetch_guild(config.serverid)  # You server id
    #     self.mutedrole = discord.utils.get(
    #         self.guild.roles, id=config.mute_role_id
    #     )  # Mute role id
    #     self.check_mutes.start()


async def setup(client):
    await client.add_cog(Moderation(client))
