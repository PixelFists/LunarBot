import discord
from discord.ext import commands

class Events(commands.Cog, name="Events",
             description="Extension responsible for handling events, listeneres.",
             command_attrs=dict(hidden=True)):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener(name="on_ready")
    async def on_ready(self):
        await self.client.wait_until_ready()
        print(f"{self.client.user} is ready")

    @commands.Cog.listener(name='on_command_error')
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("You can't use this command.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("You can't use this command in dms.")

def setup(client: commands.Bot):
    client.add_cog(Events(client))