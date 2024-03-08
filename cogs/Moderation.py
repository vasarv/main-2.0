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
        self.banned_users: list

    # kick
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Кикнуть юзера"""

        await ctx.message.delete()

        emb = discord.Embed(title="Kick", colour=discord.Color.orange())

        await member.kick(reason=reason)

        logger.info(
            f"Пользователь {ctx.author.name} кикнул юзера {member.name} по причине {reason}"
        )

        emb.set_author(name=member.name, icon_url=member.avatar.url)
        if reason == None:
            emb.add_field(
                name="Kick user".format(member.mention),
                value="Kicked user : {}".format(member.mention),
            )
        else:
            emb.add_field(
                name=f"Kick user\nПричина кика: {reason}".format(member.mention),
                value="Kicked user : {}".format(member.mention),
            )
        emb.set_footer(
            text="Был кикнут администратором".format(ctx.author.name),
            icon_url=ctx.author.avatar.url,
        )

        await ctx.send(embed=emb, delete_after=15)

    # ban
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, amount_time=None, *, reason=None):
        """Забанить юзера"""

        await ctx.message.delete()

        current_date_time = datetime.datetime.now()
        now_date = current_date_time.time()
        emb = discord.Embed(title="Бан:", color=discord.Color.red())
        
        if "m" in amount_time:
            try:
                await member.ban(reason=reason)
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что бан?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько минут?".format(amount_time[:-1]),
                    value="{} минут".format(amount_time[:-1]),
                )
                emb.set_footer(
                    text=f"{ctx.author} забанил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=emb, delete_after=15)
            except:
                await ctx.send(f"Не возможно забанить пользователя: {member.mention}!")
            await asyncio.sleep(int(amount_time[:-1]) * 60)
            for ban_entry in self.banned_users:
                user = ban_entry.user
                await ctx.guild.unban(user)
            try:
                await member.send(
                    embed=discord.Embed(
                        description=f"""**{member.mention}** Время бана истекло, вы были разбанены.""",
                        delete_after=15,
                    )
                )
            except:
                pass

        elif "h" in amount_time:
            try:
                await member.ban(reason=reason)
                # emb = discord.Embed(title = 'Бан', color = discord.Color.red())
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что бан?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько часов?".format(amount_time[:-1]),
                    value="{} часа(-ов)".format(amount_time[:-1]),
                )
                emb.set_footer(
                    text=f"{ctx.author} забанил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=emb, delete_after=15)
            except:
                await ctx.send(f"Не возможно забанить пользователя: {member.mention}!")
            await asyncio.sleep(int(amount_time[:-1]) * 60 * 60)
            for ban_entry in self.banned_users:
                user = ban_entry.user
                await ctx.guild.unban(user)
            try:
                await member.send(
                    embed=discord.Embed(
                        description=f"""**{member.mention}** Время бана истекло, вы были разбанены.""",
                        delete_after=15,
                    )
                )
            except:
                pass

        elif "d" in amount_time:
            try:
                await member.ban(reason=reason)
                # emb = discord.Embed(title = 'Бан', color = discord.Color.red())
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что бан?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько дней?".format(amount_time[:-1]),
                    value="{} дней".format(amount_time[:-1]),
                )
                emb.set_footer(
                    text=f"{ctx.author} забанил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=emb, delete_after=15)
            except:
                await ctx.send(f"Не возможно забанить пользователя: {member.mention}!")
            await asyncio.sleep(int(amount_time[:-1]) * 60 * 60 * 24)
            for ban_entry in self.banned_users:
                user = ban_entry.user
                await ctx.guild.unban(user)
            try:
                await member.send(
                    embed=discord.Embed(
                        description=f"""**{member.mention}** Время бана истекло, вы были разбанены.""",
                        delete_after=15,
                    )
                )
            except:
                pass

        elif None == amount_time:
            try:
                await member.ban(reason=reason)
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что бан?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько дней?".format(amount_time[:-1]),
                    value="{} дней".format("∞"),
                )
                emb.set_footer(
                    text=f"{ctx.author} забанил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )
                await ctx.send(embed=emb, delete_after=30)
            except:
                await ctx.send(
                    f"Не возможно забанить пользователя: {member.mention}!",
                    delete_after=5,
                )
            await ctx.send(embed=emb, delete_after=30)
        else:
            await ctx.send(f"Что-то пошло не так!", delete_after=5)

        if amount_time == None:
            logger.info(
                f"Пользователь {member.name} забанен. Выдал бан: {ctx.author.name} по причине: {reason}"
            )
        else:
            logger.info(
                f"Пользователь {member.name} забанен. Выдал бан: {ctx.author.name} по причине: {reason} на {amount_time}"
            )
        return

    # Unban
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        """Разбанить юзера"""

        await ctx.message.delete()

        self.banned_users = await ctx.guild.bans()

        for ban_entry in self.banned_users:
            user = ban_entry.user
            await ctx.guild.unban(user)

            emb = discord.Embed(title="Unban", colour=discord.Color.green())

            logger.info(f"Пользователь {ctx.author.name} разбанил юзера {user.name}")

            emb.set_author(name=user.name, icon_url=user.avatar.url)

            emb.add_field(
                name="Unban user".format(user.mention),
                value="Unbaned user : {}".format(user.mention),
            )

            emb.set_footer(
                text="Был разбанен администратором".format(ctx.author.name),
                icon_url=ctx.author.avatar.url,
            )

            await ctx.send(embed=emb, delete_after=15)

            return

        await ctx.send(f"В бане нет юзера!", delete_after=5)
        return

    # mute
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["mute"])
    async def __mute(
        self, ctx, member: discord.Member = None, amount_time=None, *, reason=None
    ):
        """Замьютить юзера"""

        await ctx.message.delete()
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
            current_date_time = datetime.datetime.now()
            if "m" in amount_time:
                emb = discord.Embed(title="Мьют", color=0x000001)
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что мьют?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько минут?".format(amount_time[:-1]),
                    value="{} минут".format(amount_time[:-1]),
                )
                emb.set_footer(
                    text=f"{ctx.author} замьютил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )

                await ctx.send(embed=emb, delete_after=30)

                mute_role = discord.utils.get(ctx.guild.roles, id=config.mute_role_id)
                await member.add_roles(mute_role)
                logger.info(
                    f"Пользователь {member.name} был замьючен. Выдал мьют: {ctx.author.name}] на [{amount_time}] по причине [{reason}]"
                )
                await asyncio.sleep(int(amount_time[:-1]) * 60)

                if mute_role in member.roles:
                    await member.remove_roles(mute_role)
                    await ctx.send(
                        embed=discord.Embed(
                            description=f"""**{member.mention}** Время мута истекло, вы были размьюченыю""",
                            color=0xFFFFFF,
                            delete_after=15,
                        )
                    )
                    return
            elif "h" in amount_time:
                emb = discord.Embed(title="Мьют", color=0x000001)
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что мьют?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько часов?".format(amount_time[:-1]),
                    value="{} часа(-ов)".format(amount_time[:-1]),
                )
                emb.set_footer(
                    text=f"{ctx.author} замьютил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )

                await ctx.send(embed=emb, delete_after=30)

                mute_role = discord.utils.get(ctx.guild.roles, id=config.mute_role_id)
                await member.add_roles(mute_role)
                logger.info(
                    f"Пользователь {member.name} был замьючен. Выдал мьют: {ctx.author.name}] на [{amount_time}] по причине [{reason}]"
                )
                await asyncio.sleep(int(amount_time[:-1]) * 60 * 60)

                if mute_role in member.roles:
                    await member.remove_roles(mute_role)
                    await ctx.send(
                        embed=discord.Embed(
                            description=f"""**{member.mention}** Время мута истекло, вы были размьючены.""",
                            color=0xFFFFFF,
                            delete_after=15,
                        )
                    )
                    return
            elif "d" in amount_time:
                emb = discord.Embed(title="Мьют", color=0x000001)
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что мьют?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько дней?".format(amount_time[:-1]),
                    value="{} дней".format(amount_time[:-1]),
                )
                emb.set_footer(
                    text=f"{ctx.author} замьютил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )

                mute_role = discord.utils.get(ctx.guild, id=config.mute_role_id)
                await member.add_roles(mute_role)
                logger.debug(
                    f"Пользователь [{ctx.author.mention}] выдал мьют пользователю [{member.name}] на [{amount_time}] по причине [{reason}]"
                )
                await asyncio.sleep(int(amount_time[:-1]) * 60 * 60 * 24)

                if mute_role in member.roles:
                    await member.remove_roles(mute_role)
                    await ctx.send(
                        embed=discord.Embed(
                            description=f"""**{member.mention}** Время мута истекло, вы были размьючены.""",
                            color=0xFFFFFF,
                            delete_after=15,
                        )
                    )
                    return
            else:
                emb = discord.Embed(title="Мьют", color=0x000001)
                emb.set_author(name=member.name, icon_url=member.avatar.url)
                emb.add_field(
                    name="За что мьют?".format(reason), value="{}".format(reason)
                )
                emb.add_field(
                    name="На сколько секунд?".format(amount_time[:-1]),
                    value="{} секунд".format(amount_time[:-1]),
                )
                emb.set_footer(
                    text=f"{ctx.author} замьютил. {current_date_time.hour}:{current_date_time.minute}/{current_date_time.day}.{current_date_time.month}.{current_date_time.year}".format(
                        ctx.author.name
                    ),
                    icon_url=ctx.author.avatar.url,
                )

                mute_role = discord.utils.get(ctx.guild.roles, id=config.mute_role_id)
                await member.add_roles(mute_role)
                logger.info(
                    f"Пользователь {member.name} был замьючен. Выдал мьют: {ctx.author.name}] на [{amount_time}] по причине [{reason}]"
                )
                await asyncio.sleep(int(amount_time[:-1]))
                if mute_role in member.roles:
                    await member.remove_roles(mute_role)
                    return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member = None):
        """Размьютить юзера"""

        await ctx.message.delete()
        current_date_time = datetime.datetime.now()
        if member is None:
            await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.mention}, укажите пользователя",
                    description=f"Пример: {command_prefix}unmute **@user**",
                )
            )
        mute_role = discord.utils.get(ctx.guild.roles, id=config.mute_role_id)
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

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = await self.client.fetch_guild(config.serverid)  # You server id
        self.mutedrole = discord.utils.get(
            self.guild.roles, id=config.mute_role_id
        )  # Mute role id
        self.check_mutes.start()


async def setup(client):
    await client.add_cog(Moderation(client))
