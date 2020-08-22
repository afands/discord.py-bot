import discord
from discord.ext import commands
import json
from pathlib import Path
import asyncio
import typing
import logging
import datetime
import os

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('.')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=185604754947178496)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd
bot.version = '1.0'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(platform="Twitch", url="https://www.twitch.tv/asupanwifi", name="games"))

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if f"<@!{bot.user.id}>" in message.content:
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = '-'
        prefixMsg = await message.channel.send(f"My prefix is `{prefix}`")
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(
        f"<@!{bot.user.id}>"
    ):
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = '-'
        prefixMsg = await message.channel.send(f"My prefix is `{prefix}`")
        return

    if message.channel.id == 698069889121779823:
        up = '<:upvote:702855972267360330>'
        down = '<:downvote:702855999819874395>'
        await message.add_reaction(up)
        await message.add_reaction(down)

    await bot.process_commands(message)

if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)
