import discord
from discord.ext import commands

class CogListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command doesn\'t exist')
            await ctx.message.add_reaction('⛔')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('~~You can\'t use commands outside of the server~~')
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description="You don't have the permissions to do that", color=discord.Color.dark_red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        else:
            raise(error)

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        global msgthing
        msgthing = ctx.content
        global authorbruv
        authorbruv = ctx.author
        return

def setup(bot):
    bot.add_cog(CogListener(bot))
