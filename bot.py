import discord, json, os, aiohttp
from discord.ext import commands
from helpcmd import HelpCMD
def config():
    """Loads the token."""
    with open('token.json') as f:
        return json.load(f)['token']

def main():
    token = config()
    client = commands.Bot(command_prefix=["lunar ", 'l!', ';'], intents=discord.Intents.all(),
                          help_command=HelpCMD())

    # makes cogs non cap sensitive
    client._BotBase__cogs = commands.core._CaseInsensitiveDict()

    for cog in os.listdir("./cogs"):
        if cog.endswith('.py'):
            cog = cog[:-3]
            client.load_extension(f'cogs.{cog}')
            print(f"loaded {cog}")

    client.session = aiohttp.ClientSession()

    other_cogs = ["manager", "jishaku"]
    for cog in other_cogs:
        try:
            client.load_extension(cog)
        except:
            pass

    client.run(token)


if __name__ == '__main__':
    main()
