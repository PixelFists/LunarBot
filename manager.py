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
    async def load(self, ctx: commands.Context, extension: str):
        try:
            self.client.load_extension(f'cogs.{self.shorten_ext(extension)}')
            await ctx.send(f"Loaded {extension}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f"{extension.capitalize()} extension is already loaded.")

    @commands.command(name='unload', help="Unloads an extension.")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, extension: str):
        try:
            self.client.unload_extension(f'cogs.{self.shorten_ext(extension)}')
            await ctx.send(f"Unloaded {extension} extension.")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"{extension.capitalize()} extension is not loaded.")

    @commands.command(name='reload',aliases=['refresh'],
                      help="Reloads an extension")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, extension: str):
        try:
            self.client.reload_extension(f'cogs.{self.shorten_ext(extension)}')
        except commands.ExtensionNotLoaded:
            self.client.load_extension(f'cogs.{self.shorten_ext(extension)}')
        finally:
            await ctx.send(f"Reloaded {extension} extension.")

def setup(client: commands.Bot):
    client.add_cog(Manager(client))
