import discord
from discord.ext import commands

class Manager(commands.Cog, name="Manager",
              description="Extention responsible for handling other extensions.",
              command_attrs=dict(hidden=True)):
    """Manager extension is used for managing other extensions and commands."""
    def __init__(self, client: commands.Bot):
        self.client = client

    hard_commands = ["enable", "disable", "load", "unload", "reload", "refresh", "toggle"]

    def shorten_ext(self, extension):
        if extension == "utils": extension = "utilities"
        """extends the extension's name.
        etc:
            utils = utilities
            mod = moderation
        """
        return extension

    @commands.command(name='load', help="Loads an extension.")
    @commands.is_owner()
    async def load(self, ctx: commands.Context, *, extension: str):
        extension = self.shorten_ext(extension.capitalize())
        try:
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send(f"Loaded {extension}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f"{extension.capitalize()} extension is already loaded.")

    @commands.command(name='unload', help="Unloads an extension.")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, *, extension: str):
        extension = self.shorten_ext(extension)
        try:
            self.client.unload_extension(f'cogs.{extension}')
            await ctx.send(f"Unloaded {extension} extension.")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"{extension.capitalize()} extension is not loaded.")

    @commands.command(name='reload',aliases=['refresh'],
                      help="Reloads an extension.")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, extension: str):
        extension = self.shorten_ext(extension)
        try:
            self.client.reload_extension(f'cogs.{extension}')
            await ctx.send(f"Reloaded {extension} extension.")
        except commands.ExtensionNotLoaded:
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send(f"Reloaded {extension} extension.")

    @commands.command(name='enable', help="Enables a command.")
    @commands.is_owner()
    async def enable(self, ctx: commands.Context, *, command):
        command = self.client.get_command(command)
        if command is None:
            return await ctx.send("This command doesn't exist.")
        if command.qualified_name in self.hard_commands:
            return await ctx.send("You can't enable this command.")
        if not command.enabled:
            command.enabled = True
            await ctx.send(f"Enabled the {command.qualified_name} command.")
        else:
            await ctx.send("This command is already enabled.")

    @commands.command(name='disable', help='Disables a command.')
    @commands.is_owner()
    async def disable(self, ctx: commands.Context, *, command):
        command = self.client.get_command(command)
        if command is None:
            return await ctx.send("This command doesn't exist.")
        if command.qualified_name in self.hard_commands:
            return await ctx.send("You can't enable this command.")
        if command.enabled:
            command.enabled = False
            await ctx.send(f"Disabled the {command.qualified_name} command.")
        else:
            await ctx.send("This command is already disabled.")

    @commands.command(name="toggle", help="Toggles a command.")
    @commands.is_owner()
    async def toggle(self, ctx: commands.Context, *, command):
        command = self.client.get_command(command)
        if command is None:
            return await ctx.send("This command doesn't exist.")
        if command.qualified_name in self.hard_commands:
            return await ctx.send("You can't toggle this command.")
        command.enabled = not command.enabled
        ternary = "Disabled" if not command.enabled else "Enabled"
        await ctx.send(f"{ternary} the {command.qualified_name} command.")

def setup(client: commands.Bot):
    client.add_cog(Manager(client))
