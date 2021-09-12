import discord
from discord.ext import commands

class Manager(commands.Cog, name="Manager",
              description="Extention responsible for handling other extensions.",
              command_attrs=dict(hidden=True)):
    """Manager extension is used for managing other extensions and commands."""
    def __init__(self, client: commands.Bot):
        self.client = client

    def shorten_ext(self, extension):
        """extends the extension's name.
        etc:
            utils = utilities
            mod = moderation
        """
        return extension

    @commands.command(name='load', help="Loads an extension.")
    @commands.is_owner()
    async def load(self, ctx: commands.Context, extension):
        extension = self.shorten_ext(extension)

    @commands.command(name='unload', help="Unloads an extension.")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, extension):
        extension = self.shorten_ext(extension)

    @commands.command(name='reload',aliases=['refresh'],
                      help="Reloads an extension")
    async def reload(self, ctx: commands.Context, extension):
        extension = self.shorten_ext(extension)

def setup(client: commands.Bot):
    client.add_cog(Manager(client))
