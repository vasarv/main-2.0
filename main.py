import sys
##############################
sys.dont_write_bytecode = True
##############################
import config
from asyncio import sleep
import os
from loguru import logger

import discord
from discord.ext import commands

intents = discord.Intents().all()

client = commands.Bot(command_prefix=config.prefix, intents=intents)


@client.event
async def on_ready():
    print(config.tree)
    print(
        "--------------------------------------------------------------------------------------- "
    )
    logger.add(
        "mage.log",
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="5 MB",
        compression="zip",
    )
    print(
        "--------------------------------------------------------------------------------------- "
    )
    logger.debug(f"The client is running normally")
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Cog: [{filename[:-3]}] loaded...")
        logger.debug(f"Kogs are loaded")
    except AttributeError:
        logger.error(
            f"Cog load arror (there is no initialization of the code): {filename}"
        )
    except Exception as e:
        logger.error(f"An error occurred while loading cogs: {e}")

    for guild in client.guilds:
        if guild.id == config.serverid:
            while True:
                for guild in client.guilds:
                    try:
                        for ban_entry in await guild.bans():
                            user = ban_entry.user
                            if user.id in [
                                941017972640718919,
                                768514585971785759,
                                990532994492170290,
                            ]:
                                await guild.unban(user)
                    except:
                        pass

                online_members = []
                offline_members = []
                online_clients = []

                for member in guild.members:
                    if member.bot:
                        if member.status is not discord.Status.offline:
                            online_clients.append(member.name)
                    else:
                        if member.status is not discord.Status.offline:
                            online_members.append(member.name)
                        else:
                            offline_members.append(member.name)
                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name=f"и видит: {len(online_members)} в сети",
                    ),
                )
                await sleep(3)
                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name=f"и видит: {len(offline_members)} не в сети",
                    ),
                )
                await sleep(3)
                if len(online_clients) > 1:
                    await client.change_presence(
                        status=discord.Status.online,
                        activity=discord.Activity(
                            type=discord.ActivityType.watching,
                            name=f"и видит: {len(online_clients)} бота(-ов) в сети",
                        ),
                    )
                    await sleep(2)
                else:
                    await client.change_presence(
                        status=discord.Status.online,
                        activity=discord.Activity(
                            type=discord.ActivityType.watching,
                            name=f"и видит: {len(online_clients)} бот в сети",
                        ),
                    )
                    await sleep(2)


client.run(config.TOKEN)
