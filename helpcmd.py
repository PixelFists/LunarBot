import discord
from discord.ext import commands

class HelpCMD(commands.MinimalHelpCommand):
    hidden_cog = ["Events", "Manager"]
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help",
                              description=f"Use {self.context.prefix}help [command | category] for more info.")
        for cog, command in mapping.items():
            try:
                cog_name = getattr(cog, "qualified_name")
                cog_desc = getattr(cog, "description", '')
                if str(cog_name).lower() not in [c.lower() for c in self.hidden_cog]:
                    embed.add_field(name=cog_name, value=cog_desc if cog_desc else "🤔")
            except:
                pass

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        embed = discord.Embed(title=cog.qualified_name, description=cog.description if cog.description else "🤔")
        for command in cog.get_commands(): # type: commands.Command
            if command.enabled and not command.hidden:
                embed.add_field(name=command.qualified_name, value=command.help)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = discord.Embed(title=command.qualified_name.capitalize(),
                              description=command.help,
                              # makes the embed color red if the command is not enabled
                              color=discord.Color.green() if command.enabled else discord.Color.red())
        if command.usage:
            embed.add_field(name="Example", value=f"{self.context.prefix}{command.usage}")

        if command.aliases:
            embed.add_field(name="Aliases", value=', '.join(command.aliases))

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        await self.send_bot_help(self.get_bot_mapping())
