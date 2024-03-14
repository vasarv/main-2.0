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
            "https://cdn.discordapp.com/icons/1214243963012124722/675c943410598ea2cdcfba3b8fc53e2c.png?size=4096"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Если юзер зашел на сервер: приветствуем и выдаем роль"""

        hello_messages: list[str] = [
            f"{member.mention} | Приветствуем на сервере {member.guild.name}",
            f"Загрузка... | Юзер {member.mention} оказывается на сервере {member.guild.name}",
            f"{member.name} теперь с нами. Прошу любить и жаловать.",
            f"{member.name} появился. Как жизнь?",
            f"{member.name} запрыгивает на сервер. Осматривайся пока тут.",
            f"{member.name} теперь с нами!",
            f"У нас новенький! | Знакомьтесь:  {member.name}",
            f"{member.name} вступает в ряды участников сервера {member.guild.name}!",
        ]

        await member.add_roles(
            discord.utils.get(
                member.guild.roles,
                id=config.botrole if member.bot else config.default_role,
            )
        )

        try:
            await member.send(
                f"Приветствуем на сервере {member.guild.name}! Пожалуйста, прочтите правила сервера, ведь не знание правил не освобождает от ответственности! И напишите что-нибудь о себе..."
            )
        except:
            pass

        embed = discord.Embed(
            description=f"""{choice(hello_messages)}""", color=0x985DB3
        )
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text="Приветики!")

        message = await self.client.get_channel(config.hello_channel_id).send(embed=embed)

        await message.add_reaction(
            self.client.get_emoji(1215544437380223027)
        )  # hello emoji

        await discord.utils.get(member.guild.channels, id=self.log).send(
            f"Пользователь [{member.name}] зашёл на сервер"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Если юзер вышел, то прощаемся"""
        goodbye_message_texts: list[str] = [
            f"{member.name} покинул нас, скатертью дорожка, пусть его сожрут жабы.",
            f"{member.name} ушёл за хлебом",
            f"{member.name} покидает сервер",
        ]
        goodbye_message_text = choice(goodbye_message_texts)

        embed = discord.Embed(
            description=f"""{goodbye_message_text}""", color=0x985DB3
        )
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text="Пока, пока...")

        message = await self.client.get_channel(config.hello_channel_id).send(embed=embed)

        if (goodbye_message_texts.index(goodbye_message_text)) == 0:
            pass  # Добавить эмодзи жабки
        else:
            await message.add_reaction(
                self.client.get_emoji(1215546809691152426)
            )  # Press F emoji

        await discord.utils.get(member.guild.channels, id=self.log).send(
            f"Пользователь [{member.name}] вышел с сервера"
        )


async def setup(client):
    await client.add_cog(halloevents(client))
