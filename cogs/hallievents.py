import discord
from discord.ext import commands
import config
from loguru import logger
from random import choice


class halloevents(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logger
        self.log = config.log_channel
        self.server_icon_link: str = (
            "https://cdn.discordapp.com/icons/1214243963012124722/90ba47bfe1401b1edb2bfe1ad666c555.png?size=4096"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Если юзер зашел на сервер: приветствуем и выдаем роль"""

        await discord.utils.get(member.guild.channels, id=self.log).send(
            f"Пользователь [{member.name}] зашёл на сервер"
        )
        try:
            await member.send(
                f"Приветствуем на сервере {member.guild.name}! Пожалуйста, прочтите правила сервера, ведь не знание правил не освобождает от ответственности! И напишите что-нибудь о себе..."
            )
        except:
            pass

        for ch in self.client.get_guild(member.guild.id).channels:
            if ch.id == config.hello_channel:
                hello_messages: list = [
                    f"{member.mention} | Приветствуем на сервере {member.guild.name}",
                    f"Загрузка... | Игрок {member.mention} оказывается на сервере {member.guild.name}",
                    f"{member.name} теперь с нами. Прошу любить и жаловать.",
                    f"{member.name} появился. Как жизнь?",
                    f"{member.name} запрыгивает на сервер. Осматривайся пока тут.",
                    f"{member.name} теперь с нами!",
                    f"У нас новенький! | Знакомьтесь:  {member.name}",
                    f"{member.name} вступает в ряды игроков на сервере {member.guild.name}!",
                ]
                embed = discord.Embed(
                    description=f"""{choice(hello_messages)}""", color=0x985DB3
                )
                embed.set_thumbnail(url=self.server_icon_link)
                embed.set_footer(text="Приветики!")
                sender3 = await self.client.get_channel(ch.id).send(embed=embed)
                await sender3.add_reaction(self.client.get_emoji(1215544437380223027)) #hello emoji
            await member.add_roles(
                discord.utils.get(
                    member.guild.roles,
                    id=config.botrole if member.bot == True else config.default_role,
                )
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Если юзер вышел, то прощаемся"""

        await discord.utils.get(member.guild.channels, id=self.log).send(
            f"Пользователь [{member.name}] вышел с сервера"
        )
        for ch in self.client.get_guild(member.guild.id).channels:
            if ch.id == config.hello_channel:
                goodbye_messages: list = [
                    f"{member.name} покинул нас, скатертью дорожка, пусть его сожрут жабы.",
                    f"{member.name} ушёл за хлебом",
                    f"{member.name} покидает сервер",
                ]
                goodbye_message = str(choice(goodbye_messages))
                if (
                    goodbye_message
                    == f"{member.name} покинул нас, скатертью дорожка, пусть его сожрут жабы."
                ):
                    embed = discord.Embed(
                        description=f"""{member.name} покинул нас, скатертью дорожка, пусть его сожрут жабы""",
                        color=0x985DB3,
                    )
                    embed.set_thumbnail(url=self.server_icon_link)
                    embed.set_footer(text="Пока, пока...")
                    sender1 = await self.client.get_channel(ch.id).send(embed=embed)
                    # await sender1.add_reaction(self.client.get_emoji(config.frog_emoji))
                else:
                    embed = discord.Embed(
                        description=f"""{goodbye_message}""", color=0x985DB3
                    )
                    embed.set_thumbnail(url=self.server_icon_link)
                    embed.set_footer(text="Пока, пока...")
                    sender2 = await self.client.get_channel(ch.id).send(embed=embed)
                    await sender2.add_reaction(self.client.get_emoji(1215546809691152426)) #Press F
                    # await sender2.add_reaction(self.client.get_emoji(config.goldrip_emoji))


async def setup(client):
    await client.add_cog(halloevents(client))
