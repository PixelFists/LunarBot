import discord
from discord.ext import commands
from typing import Union

class Utilities(commands.Cog,
                name="Utilities",
                description="Extension containing utility commands."):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="whois",
                      aliases=['userinfo'],
                      help="Shows info about a user.",
                      usage='whois PixelFists#5791')
    @commands.guild_only()
    async def whois(self, ctx: commands.Context, user: Union[discord.Member, discord.User]=None):
        user = user or ctx.author
        embed = discord.Embed(title=str(user), color=user.color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Created at", value=user.created_at)
        embed.add_field(name="Joined at", value=user.joined_at)
        embed.add_field(name="Top role", value=user.top_role)
        embed.add_field(name="User ID", value=user.id)
        if user.bot:
            embed.title = user + " (BOT)"
        await ctx.send(embed=embed)

    @commands.command(name='server',
                      aliases=['serverinfo', 'guildinfo', 'guild'],
                      help="Shows info about the guild that the command was used in.")
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.guild
        embed = discord.Embed(title=guild.name)
        if guild.description is not None:
            embed.description = guild.description
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Server ID", value=guild.id)
        embed.add_field(name="Channel count", value=len(guild.channels))
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Voice channels", value=len(guild.voice_channels) + len(guild.stage_channels))
        embed.add_field(name="Member count", value=guild.member_count)
        await ctx.send(embed=embed)

    @commands.command(name="ping",
                      aliases=["latency", 'ms'],
                      help="Shows the bot's latency.")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Current bot latency is around `{round(self.client.latency * 1000)}ms.`")

def setup(client: commands.Bot):
    client.add_cog(Utilities(client))
