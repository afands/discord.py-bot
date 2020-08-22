import discord
from discord.ext import commands
import discord.utils
import datetime
import asyncio
import typing
import platform
import requests
import pendulum
import pathlib
import os
import string
import qrcode
from typing import Optional
from discord import Spotify
import random


import cogs._json

def lineCount():
    code = 0
    comments = 0
    blank = 0
    file_amount = 0
    ENV = "venv"

    for path, _, files in os.walk("."):
        for name in files:
            file_dir = str(pathlib.PurePath(path, name))
            if not name.endswith(".py") or ENV in file_dir:
                continue
            file_amount += 1
            with open(file_dir, "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip().startswith("#"):
                        comments += 1
                    elif not line.strip():
                        blank += 1
                    else:
                        code += 1

    total = comments + blank + code

    return "Code: {}\n" \
           "Commentary: {}\n" \
           "Blank: {}\n" \
           "Total: {}\n" \
           "Files: {}".format(code, comments, blank, total, file_amount)


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def prefix(self, ctx, *, pre='-'):
        data = cogs._json.read_json('prefixes')
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, 'prefixes')
        await ctx.send(f"The guild prefix has been set to `{pre}`. Use `{pre}prefix <prefix>` to change it again!")

    @commands.command()
    async def meme(self, ctx):
        req = requests.get("https://apis.duncte123.me/meme")
        meme = req.json()
        embed = discord.Embed(color=discord.Color.dark_blue(), timestamp=datetime.datetime.utcnow())
        embed.set_image(url=meme['data']['image'])
        embed.add_field(name="Quality Meme", value=f"{meme['data']['title']}")
        embed.set_footer(text=f"{meme['data']['url']}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def spotify(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        for activity in user.activities:
            if isinstance(activity, Spotify):
                em = discord.Embed(color=discord.Color.dark_green())
                em.title = f'{user.name} is listening to: {activity.title}'
                em.set_thumbnail(url=activity.album_cover_url)
                em.description = f"**Song Name**: {activity.title}\n**Song Artist**: {activity.artist}\n**Song Album**: {activity.album}\n**Song Length**: {pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}"
                await ctx.send(embed=em)
                break
        else:
            embed = discord.Embed(description=f"{user.name} isn't listening to Spotify right now", color=discord.Color.dark_red())
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def dm(self, ctx, user:discord.User, *, content):
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="Eternals", value=content, inline=False)
        await user.send(embed=embed)
        await ctx.send(f"{user} has receive the message")

    @commands.command()
    async def avatar(self, ctx, *,  user : discord.Member=None):
        user = user or ctx.author
        await ctx.send(f"Avatar to **{user.name}**\n{user.avatar_url_as(size=1024)}")

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        global msgthing
        msgthing = ctx.content
        global authorbruv
        authorbruv = ctx.author
        return

    @commands.command()
    async def snipe(self, ctx):
            lol1s = discord.Embed(
                title='fuken sniped',
                description=f'`{authorbruv}`  `{msgthing}`')
            await ctx.send(embed=lol1s)

    @commands.command()
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@185604754947178496>")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def user(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author

        show_roles = ', '.join(
            [f"<@&{x.id}>" for x in sorted(user.roles, key=lambda x: x.position, reverse=True) if x.id != ctx.guild.default_role.id]
        ) if len(user.roles) > 1 else 'None'

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="Full name", value=user, inline=True)
        embed.add_field(name="Nickname", value=user.nick if hasattr(user, "nick") else "None", inline=True)
        embed.add_field(name="Account created", value=default.date(user.created_at), inline=True)
        embed.add_field(name="Joined this server", value=default.date(user.joined_at), inline=True)

        embed.add_field(
            name="Roles",
            value=show_roles,
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def codeline(self, ctx):
        await ctx.send(lineCount())

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def echo(self, ctx, user: discord.Member, integer: int ):
        i = 1
        for i in range(integer):
            await ctx.send(f'{user.mention}')
            i += 1
            if i == 10:
                break

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, channel: discord.VoiceChannel):
        channel = self.bot.get_channel(channel.id)
        for x in channel.members:
            await x.edit(mute=True)
        await ctx.send(f'Muted **{channel}**')



    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, channel: discord.VoiceChannel):
        channel = self.bot.get_channel(channel.id)
        for x in channel.members:
            await x.edit(mute=False)
        await ctx.send(f'Unmuted **{channel}**')

def setup(bot):
    bot.add_cog(Commands(bot))
